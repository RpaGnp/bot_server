import requests


class TokenApiModulo():
    
    def __init__(self, driver):
        self.driver = driver
        self.api_url = "https://crm.gnpsa.co/cookie_modulo"

    def convertir_cookies_a_string(self, cookies):
        """
        Convierte el array de cookies de Selenium al formato de Cookie Header
        Ejemplo: PHPSESSID=abc123; PERMISOS=xyz789; TIPO_RED=RES
        """
        cookie_strings = []
        for cookie in cookies:
            cookie_strings.append("{}={}".format(cookie['name'], cookie['value']))
        
        return "; ".join(cookie_strings)

    def enviar_cookie_a_api(self, cookie_string):
        """
        Envía la cookie en formato string a la API
        """
        try:
            response = requests.get(self.api_url, params={'cookie': cookie_string})
            
            if response.status_code == 200:
                return True
            else:
                return False
                
        except Exception as e:
            print("\n✗ Error al conectar con la API: {}".format(e))
            return False

    def extraer_cookie_permisos(self):
        """
        Extrae y retorna la cookie de permisos del navegador
        """
        try:
            # Obtener todas las cookies
            cookies = self.driver.get_cookies()
            if not cookies:
                print("\n--- No se encontraron cookies ---")
                return None
            
            cookie_string = self.convertir_cookies_a_string(cookies)
            print("\n--- Cookie String Generada ---")
            print(cookie_string)
            print("-" * 50)
            self.enviar_cookie_a_api(cookie_string)
        except Exception as e:
            print("Error al extraer cookies: {}".format(e))
            return None
