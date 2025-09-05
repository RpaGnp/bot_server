from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Ajusta la ruta a tu chromedriver si es necesario
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    # Abrir Google
    driver.get("https://www.google.com")

    # Aceptar cookies si aparece (opcional)
    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "L2AGLb"))
        ).click()
    except:
        pass  # Si no aparece, sigue normal

    # Buscar "parques en Bogotá"
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("parques en Bogotá")
    search_box.send_keys(Keys.RETURN)

    # Esperar a que carguen los resultados
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
    )

    # Hacer clic en el primer resultado
    first_result = driver.find_element(By.CSS_SELECTOR, "h3")
    first_result.click()

    # Esperar 10 segundos en la página
    time.sleep(10)

finally:
    # Cerrar el navegador
    driver.quit()
