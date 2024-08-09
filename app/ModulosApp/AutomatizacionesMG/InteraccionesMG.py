#LIBRERIAS PARA CHROMEDRIVER***********************
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service
import time

from ..ModelDataBase import ConectorDbMysql
import requests



class BotMg:
	def __init__(self,driver):
		self.driver=driver

	def Login(self,url,arraycredenciales,idbot):				
		driver = self.driver
		driver.get(url)

		Usuario = arraycredenciales[0].decode('utf-8')
		Clave = arraycredenciales[1].decode('utf-8')
		driver.implicitly_wait(180)
		myDinamicElement = driver.find_element(by=By.XPATH, value='//*[@class="ico_Candado login_alertas"]')

		driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').clear()
		driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').send_keys(Usuario)
		element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="password"]')))
		time.sleep(1)
		driver.find_element(by=By.XPATH, value='//*[@type="password"]').clear()            
		driver.find_element(by=By.XPATH, value='//*[@type="password"]').send_keys(Clave.strip())
		time.sleep(3)
		element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@name="Submit"]')))
		if driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').is_displayed():
			driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').click()
		time.sleep(2)            

		try:
			element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//nav[@class="ClaroTemplate-nav clearfix desktop-nav"]')))
		except:
			return False            
		
		if driver.current_url==f'{url}/Modificar_password.php':                
			sql=("SPR_INS_ESTBOT",[idbot,"Error login"])
			ConectorDbMysql().FuncInsInfoOne(sql)
			driver.quit()
			del driver                

		if driver.current_url != f'{url}/indexadmin.php':
			if driver.current_url==f'{url}/Login.php':
				driver.get(f'{url}/index.php')
			x=0
			while x<=2:          
				try:
					if driver.current_url==f'{url}/Login.php':
						driver.get(f'{url}/index.php')
					driver.implicitly_wait(18)
					driver.find_element(by=By.XPATH, value='//*[@class="ico_Candado login_alertas"]')

					driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').clear()
					driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').send_keys(Usuario)
					time.sleep(1)
					element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="password"]')))
					driver.find_element(by=By.XPATH, value='//*[@type="password"]').clear()
					driver.find_element(by=By.XPATH, value='//*[@type="password"]').send_keys(Clave)
					time.sleep(2)
					intro = driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').click()
					time.sleep(1)
					if driver.current_url == f'{url}/indexadmin.php':
						break						
					else:
						x+=1
				except:
					driver.refresh()
					time.sleep(5)
					x+=1                
			if x>2:
				sql=("SPR_INS_ESTBOT",[idbot,"Error login"])
				ConectorDbMysql().FuncInsInfoOne(sql)            
				self.driver.quit()        
			else:
				sql=("SPR_INS_ESTBOT",[idbot,"En labor"])
				ConectorDbMysql().FuncInsInfoOne(sql)
			
		else:
			sql=("SPR_INS_ESTBOT",[idbot,"En labor"])
			ConectorDbMysql().FuncInsInfoOne(sql)

		return 1
		

	def ConsultaOts(self,url,orden,tipo):
		self.driver.get(f'{url}/MGW/MGW/Agendamiento/index.php')
		#ingreso consultar orden
		self.driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').click()
		self.driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').clear()
		self.driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').send_keys(orden)
		time.sleep(1)			
		if  "LLS" in tipo.upper():
			self.driver.find_element(By.XPATH,'//input[@type="radio" and @value="L"]').click()
		else:
			self.driver.find_element(By.XPATH,'//input[@type="radio" and @value="O"]').click()
		time.sleep(0.5)
		self.driver.find_element(By.XPATH,'//input[@type="submit"]').click()
		time.sleep(2)


	def Validadorestadoot(self,url):
		# verificar orden
		if self.driver.find_element(By.XPATH,'//body').text=='ningun dato parametrizado': 
		    return 'ningun dato parametrizado'

		# verificar orden agenda pr wfm		
		urlref = '/MGW/MGW/Agendamiento/agendamiento.php'		
		if  urlref not in self.driver.current_url:            
		    return 'Orden no cancelada, Redirige a modulo agendamiento antiguo!'

		#dentro de la orden
		try:
		    element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]')))
		except Exception as e:
		    return e
		    
		time.sleep(2)
		if 'Esta orden no se puede agendar en workforce' in self.driver.find_element(By.XPATH,'//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]').text:
		    return 'Orden no cancelada, Esta orden no se puede cancelar en workforce'
		    

		return 1

	def clickone(self,xpath):
		self.driver.find_element(By.XPATH,xpath).click