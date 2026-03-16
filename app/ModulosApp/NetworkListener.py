"""
Listener de eventos de red para Selenium/Opera.
Escucha requests XHR/Fetch, los imprime y guarda en archivo para análisis.
"""
import json
import os
import sys
import time
import base64
import threading
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def _get_capture_dir():
    """Obtiene la ruta para guardar capturas. Usa env var o rutas por defecto."""
    env_path = os.getenv("NETWORK_CAPTURE_DIR")
    if env_path:
        return Path(env_path)
    # Proyecto: docker_bot/app/ModulosApp/NetworkListener.py -> docker_bot/logs/network_captures
    try:
        base = Path(__file__).resolve().parent.parent.parent
        if (base / "app").is_dir() or (base / "ModulosApp").is_dir():
            return base / "logs" / "network_captures"
    except Exception:
        pass
    # Fallback: si se ejecuta como exe, usar directorio del ejecutable
    try:
        if getattr(sys, "frozen", False):
            exe_dir = Path(sys.executable).parent
            return exe_dir / "logs" / "network_captures"
    except Exception:
        pass
    # Fallback: directorio actual de trabajo
    return Path.cwd() / "logs" / "network_captures"


CAPTURE_DIR = _get_capture_dir()

EXCLUDED_EXTENSIONS = (
    '.js', '.ico', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg',
    '.woff', '.woff2', '.ttf', '.eot', '.map', '.webp', '.bmp', '.bin',
    '.dll', '.exe', '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
    '.iso', '.dmg', '.pkg', '.deb', '.rpm', '.msi', '.cab', '.appx',
    '.appxbundle', '.msix', '.msixbundle', '.msixupload'
)


def _es_archivo_estatico(url):
    path = url.split('?')[0].lower()
    return any(path.endswith(ext) for ext in EXCLUDED_EXTENSIONS)


def _obtener_response_body(driver, request_id):
    try:
        time.sleep(0.1)
        if hasattr(driver, 'execute_cdp_cmd'):
            result = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            body = result.get("body", "")
            if result.get("base64Encoded"):
                body = base64.b64decode(body).decode('utf-8', errors='replace')
            return body
    except Exception:
        pass
    return None


def _extraer_payload(req_data):
    payloads = []
    url = req_data.get("url", "")
    if "?" in url:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if params:
            params_flat = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
            payloads.append(("Query params", params_flat))
    post_data = req_data.get("postData") or req_data.get("postDataEntries")
    if post_data:
        payloads.append(("Body", post_data))
    return payloads


def _construir_registro(req_data, status, headers, body, req_num):
    """Construye un dict con todos los datos para guardar en log."""
    payloads = _extraer_payload(req_data)
    payload_dict = {}
    for nombre, datos in payloads:
        key = "query_params" if "Query" in nombre else "body"
        payload_dict[key] = datos

    resp_headers = None
    if headers:
        try:
            resp_headers = json.loads(headers) if isinstance(headers, str) else headers
        except (json.JSONDecodeError, TypeError):
            resp_headers = headers

    return {
        "request_num": req_num,
        "timestamp": datetime.now().isoformat(),
        "method": req_data.get("method", "N/A"),
        "type": req_data.get("type", "N/A"),
        "url": req_data.get("url", "N/A"),
        "payload": payload_dict if payload_dict else None,
        "status": status,
        "response_headers": resp_headers,
        "response_body": body,
    }


def _guardar_en_archivo(registro, log_file, file_lock):
    """Guarda un registro en el archivo JSONL (append)."""
    try:
        CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
        with file_lock:
            with open(log_file, "a", encoding="utf-8") as f:
                line = json.dumps(registro, ensure_ascii=False) + "\n"
                f.write(line)
    except Exception as e:
        print(f"[NetworkListener] Error guardando log en {log_file}: {e}")


def _imprimir_request(req_data, status, headers, body, req_num):
    print(f"[NETWORK REQUEST #{req_num}]")
    print(f"  Método  : {req_data.get('method', 'N/A')}")
    print(f"  Tipo    : {req_data.get('type', 'N/A')}")
    print(f"  URL     : {req_data.get('url', 'N/A')}")
    payloads = _extraer_payload(req_data)
    if payloads:
        for nombre, datos in payloads:
            if isinstance(datos, (dict, list)):
                datos_str = json.dumps(datos, indent=2, ensure_ascii=False)
            elif isinstance(datos, str):
                try:
                    parsed = json.loads(datos)
                    datos_str = json.dumps(parsed, indent=2, ensure_ascii=False)
                except (json.JSONDecodeError, TypeError):
                    datos_str = datos
            else:
                datos_str = str(datos)
            print(f"  Payload ({nombre}):\n{datos_str}")
    print(f"  Status  : {status}")
    if headers:
        print(f"  Headers : {headers}")
    if body:
        body_str = body[:2000] + "..." if len(body) > 2000 else body
        print(f"  Response:\n{body_str}")
    print()


def _run_listener(driver, stop_event):
    """Bucle principal del listener. Corre en un hilo separado."""
    request_ids_seen = set()
    pending_requests = {}
    request_count = 0
    file_lock = threading.Lock()
    get_log_errors = 0

    # Archivo de log con timestamp por sesión
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = CAPTURE_DIR / f"network_capture_{timestamp}.jsonl"

    # Crear directorio y verificar que se puede escribir
    try:
        CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
        test_file = CAPTURE_DIR / "_test_write.tmp"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink()
    except Exception as e:
        print(f"[NetworkListener] ADVERTENCIA: No se pudo crear {CAPTURE_DIR}: {e}")
        print(f"[NetworkListener] Los logs NO se guardarán en archivo.")

    print(f"\n{'='*60}")
    print("[NetworkListener] Escuchando eventos de red en Opera...")
    print(f"[NetworkListener] Guardando en: {log_file.absolute()}")
    print(f"{'='*60}\n")

    while not stop_event.is_set():
        try:
            logs = driver.get_log("performance")
            get_log_errors = 0  # Reset on success

            for entry in logs:
                try:
                    message = json.loads(entry["message"])["message"]
                    method = message.get("method", "")

                    if method == "Network.requestWillBeSent":
                        params = message.get("params", {})
                        request_id = params.get("requestId", "")

                        if request_id and request_id not in request_ids_seen:
                            request = params.get("request", {})
                            url = request.get("url", "N/A")

                            if _es_archivo_estatico(url):
                                request_ids_seen.add(request_id)
                                continue

                            pending_requests[request_id] = {
                                "url": url,
                                "method": request.get("method", "N/A"),
                                "type": params.get("type", "N/A"),
                                "postData": request.get("postData"),
                                "postDataEntries": request.get("postDataEntries"),
                            }

                    elif method == "Network.responseReceived":
                        params = message.get("params", {})
                        request_id = params.get("requestId", "")

                        if request_id in pending_requests:
                            req_data = pending_requests.pop(request_id)
                            request_ids_seen.add(request_id)
                            request_count += 1

                            response = params.get("response", {})
                            status = response.get("status", "N/A")
                            resp_headers = response.get("headers") or {}
                            if isinstance(resp_headers, list):
                                resp_headers = {h.get("name", ""): h.get("value", "") for h in resp_headers}
                            headers_str = json.dumps(resp_headers, indent=4, ensure_ascii=False) if resp_headers else ""

                            body = _obtener_response_body(driver, request_id)

                            _imprimir_request(req_data, status, headers_str, body, request_count)

                            # Guardar en archivo para análisis posterior
                            registro = _construir_registro(req_data, status, headers_str, body, request_count)
                            _guardar_en_archivo(registro, log_file, file_lock)
                            if request_count == 1:
                                print(f"[NetworkListener] Primer request guardado en: {log_file.absolute()}")
                except (json.JSONDecodeError, KeyError):
                    continue

        except Exception as e:
            if not stop_event.is_set():
                get_log_errors += 1
                err_str = str(e).lower()
                if "invalid" not in err_str and "session" not in err_str and "closed" not in err_str:
                    if get_log_errors <= 3:
                        print(f"[NetworkListener] Error: {e}")
                    elif get_log_errors == 4:
                        print("[NetworkListener] Opera puede no soportar performance logs. Verifica goog:loggingPrefs.")
        time.sleep(0.5)

    print("[NetworkListener] Detenido.")


def iniciar_network_listener(driver):
    """
    Inicia un hilo que escucha eventos de red del driver.
    Retorna (thread, stop_event) para poder detenerlo luego.
    """
    stop_event = threading.Event()
    thread = threading.Thread(
        target=_run_listener,
        args=(driver, stop_event),
        daemon=True,
        name="NetworkListener"
    )
    thread.start()
    return thread, stop_event
