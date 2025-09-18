from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver.opera.options import Options as OperaOptions
import time
import os
import sys

def configurar_chrome_options():
    """Configura las opciones de Chrome para WhatsApp Web"""
    chrome_options = Options()
    
    # Detectar sistema operativo y configurar ruta del perfil
    if sys.platform.startswith('win'):
        # Windows
        user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
    elif sys.platform.startswith('darwin'):
        # macOS
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    else:
        # Linux
        user_data_dir = os.path.expanduser("~/.config/google-chrome")
    
    # Configurar perfil para mantener cookies
    chrome_options.add_argument("--user-data-dir={}".format(user_data_dir))
    chrome_options.add_argument("--profile-directory=Default")
    
    # Opciones para evitar detección de bot
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Configurar user agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    return chrome_options

def abrir_whatsapp_web():
    """Abre WhatsApp Web manteniendo la sesión guardada"""
    
    # Configurar opciones
    chrome_options = configurar_chrome_options()
    
    try:
        print("🚀 Iniciando navegador...")
        
        opera_options = OperaOptions()
        opera_options.binary_location = r'%s\AppData\Local\Programs\Opera\opera.exe' % os.path.expanduser('~')
        opera_options.add_argument('--start-maximized')
        driver = webdriver.Opera(executable_path=r'C:\dchrome\operadriver.exe', options=opera_options)

        print("✅ Navegador iniciado correctamente")
        
        # Configurar para evitar detección (compatible con versiones antiguas)
        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception:
            pass  # Si no funciona, continuamos sin problema
        
        print("📱 Abriendo WhatsApp Web...")
        driver.get("https://web.whatsapp.com/")
        
        # Esperar a que la página cargue
        print("⏳ Esperando a que cargue WhatsApp Web...")
        time.sleep(5)
        
        try:
            # Esperar hasta 60 segundos para que cargue completamente
            wait = WebDriverWait(driver, 60)
            
            print("🔍 Verificando estado de la sesión...")
            
            # Esperar a que aparezca alguno de estos elementos
            elemento_encontrado = None
            timeout = time.time() + 60  # 60 segundos de timeout
            
            while time.time() < timeout:
                try:
                    # Buscar código QR (necesita login)
                    qr_canvas = driver.find_elements(By.CSS_SELECTOR, "canvas[aria-label*='scan']")
                    if qr_canvas and qr_canvas[0].is_displayed():
                        print("📱 Código QR detectado - Escanea desde tu teléfono")
                        elemento_encontrado = "qr"
                        break
                    
                    # Buscar lista de chats (ya logueado)
                    chat_list = driver.find_elements(By.CSS_SELECTOR, "[data-testid='chat-list']")
                    if chat_list and chat_list[0].is_displayed():
                        print("✅ ¡Sesión activa detectada!")
                        elemento_encontrado = "logueado"
                        break
                    
                    # Buscar área principal de WhatsApp
                    main_area = driver.find_elements(By.CSS_SELECTOR, "#main")
                    if main_area:
                        print("✅ WhatsApp Web cargado correctamente")
                        elemento_encontrado = "cargado"
                        break
                        
                    # Buscar cualquier indicador de WhatsApp cargado
                    whatsapp_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid*='whatsapp']")
                    if whatsapp_elements:
                        elemento_encontrado = "parcial"
                        break
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print("⏳ Esperando que cargue... ({})".format(str(e)[:50]))
                    time.sleep(3)
            
            if elemento_encontrado == "qr":
                print("\n" + "="*50)
                print("📱 ESCANEA EL CÓDIGO QR DESDE TU TELÉFONO")
                print("="*50)
                print("1. Abre WhatsApp en tu teléfono")
                print("2. Ve a Configuración > Dispositivos vinculados")
                print("3. Toca 'Vincular un dispositivo'")
                print("4. Escanea el código QR que aparece en el navegador")
                print("="*50)
                
                # Esperar hasta que se complete el login
                login_timeout = time.time() + 120  # 2 minutos para escanear
                while time.time() < login_timeout:
                    try:
                        chat_list = driver.find_elements(By.CSS_SELECTOR, "[data-testid='chat-list']")
                        if chat_list and chat_list[0].is_displayed():
                            print("✅ ¡Login completado exitosamente!")
                            break
                    except Exception:
                        pass
                    time.sleep(2)
            
            elif elemento_encontrado in ["logueado", "cargado"]:
                print("✅ WhatsApp Web está listo para usar!")
            else:
                print("⚠️  WhatsApp Web cargó pero con estado desconocido")
            
        except Exception as e:
            print("❌ Error al verificar el estado: {}".format(str(e)))
            print("💡 Intenta refrescar la página manualmente")
        
        print("\n" + "="*50)
        print("🎉 WHATSAPP WEB ESTÁ FUNCIONANDO")
        print("="*50)
        print("• El navegador permanecerá abierto")
        print("• Puedes usar WhatsApp normalmente")
        print("• Las cookies se guardarán automáticamente")
        print("• Presiona Enter en la consola para cerrar")
        print("="*50)
        
        # Mantener el navegador abierto
        input("\n👆 Presiona Enter para cerrar el navegador...")
        
        return driver
        
    except Exception as e:
        print("❌ Error al iniciar el navegador: {}".format(str(e)))
        print("\n🔧 POSIBLES SOLUCIONES:")
        print("1. Asegúrate de tener Chrome instalado")
        print("2. Descarga chromedriver desde: https://chromedriver.chromium.org/")
        print("3. Coloca chromedriver.exe en la misma carpeta que este script")
        print("4. O agrega chromedriver a tu PATH del sistema")
        return None

def enviar_mensaje_simple(driver, nombre_contacto, mensaje):
    """
    Función simple para enviar un mensaje
    Compatible con Python 3.8.9 y versiones antiguas de Selenium
    """
    try:
        print("🔍 Buscando contacto: {}".format(nombre_contacto))
        
        # Buscar la caja de búsqueda
        search_elements = [
            "div[contenteditable='true'][data-testid='chat-list-search']",
            "div[contenteditable='true']",
            "[data-testid='chat-list-search']"
        ]
        
        search_box = None
        for selector in search_elements:
            try:
                search_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                break
            except Exception:
                continue
        
        if not search_box:
            print("❌ No se pudo encontrar la caja de búsqueda")
            return False
        
        # Limpiar y escribir el nombre del contacto
        search_box.clear()
        search_box.send_keys(nombre_contacto)
        time.sleep(3)
        
        # Hacer clic en el primer resultado
        try:
            first_result = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='cell-frame-container']"))
            )
            first_result.click()
            time.sleep(2)
        except Exception:
            print("❌ No se encontró el contacto")
            return False
        
        # Buscar la caja de mensaje
        message_selectors = [
            "div[contenteditable='true'][data-testid='conversation-compose-box-input']",
            "div[contenteditable='true']",
            "[data-testid='conversation-compose-box-input']"
        ]
        
        message_box = None
        for selector in message_selectors:
            try:
                message_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                break
            except Exception:
                continue
        
        if not message_box:
            print("❌ No se pudo encontrar la caja de mensaje")
            return False
        
        # Escribir el mensaje
        message_box.send_keys(mensaje)
        time.sleep(1)
        
        # Buscar y hacer clic en el botón de enviar
        send_selectors = [
            "button[data-testid='compose-btn-send']",
            "span[data-testid='send']",
            "button[aria-label='Enviar']"
        ]
        
        for selector in send_selectors:
            try:
                send_button = driver.find_element(By.CSS_SELECTOR, selector)
                send_button.click()
                print("✅ Mensaje enviado a {}: {}".format(nombre_contacto, mensaje))
                return True
            except Exception:
                continue
        
        print("❌ No se pudo enviar el mensaje")
        return False
        
    except Exception as e:
        print("❌ Error al enviar mensaje: {}".format(str(e)))
        return False

if __name__ == "__main__":
    print("🚀 WhatsApp Web Bot - Python 3.8.9")
    print("="*50)
    
    driver = abrir_whatsapp_web()
    
    if driver:
        try:
            # Ejemplo de uso para enviar mensaje (opcional)
            usar_bot = input("\n¿Quieres enviar un mensaje automático? (s/n): ").lower()
            if usar_bot == 's':
                contacto = input("Nombre del contacto: ")
                mensaje = input("Mensaje a enviar: ")
                enviar_mensaje_simple(driver, contacto, mensaje)
            
        except KeyboardInterrupt:
            print("\n👋 Cerrando por interrupción del usuario")
        finally:
            driver.quit()
            print("✅ Navegador cerrado")
    else:
        print("❌ No se pudo iniciar WhatsApp Web")
        print("\n🔧 Verifica que tengas:")
        print("• Google Chrome instalado")
        print("• ChromeDriver descargado y en PATH")
        print("• Selenium instalado: pip install selenium")