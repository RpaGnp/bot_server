import time
import csv
import sys
import os
from datetime import date
from datetime import datetime
import tempfile



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



class BotChrome():
	"""docstring for BotChrome"""
	def __init__(self, driver):
		super(BotChrome, self).__init__()		
		self.driver=driver
		
	
	def ClickElemento(self,xpath):		
		
		element = WebDriverWait(self.driver, 250).until(EC.element_to_be_clickable((By.XPATH, xpath)))
			
		self.driver.find_element(by=By.XPATH, value=xpath).click()
		self.driver.implicitly_wait(60)                    
		del xpath

	def ClickElementos(self,xpath,indice):		
		element = WebDriverWait(self.driver, 155).until(EC.element_to_be_clickable((By.XPATH, xpath)))
		self.driver.find_elements(by=By.XPATH, value=xpath)[indice].click()
		self.driver.implicitly_wait(60)                    
		del xpath
	
	def DiligenciarTexbox(self,xpath,Text):
		element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
		self.driver.find_element(by=By.XPATH, value=xpath).clear()
		self.driver.find_element(by=By.XPATH, value=xpath).send_keys(Text)

class ExtractorEstadoOrden():
	"""RECORRER LA ORDEN Y EXTRAER SERVICIOS ACTIVOS DEL CLIENTE Y SU ESTADO"""
	def __init__(self, driver):
		super(ExtractorEstadoOrden, self).__init__()
		self.driver=driver

	def ExtraerServicios(self):
		array_datos=self.driver.find_elements(by=By.XPATH, value='//*[@class="valor_validar"]')
		lista_estados=[]
		for i in range(len(array_datos)):			
			lista_estados.append(str(array_datos[i].text))
			#


		#if len(lista_estados)<14:
		#	return 0




		'''ArrayDatosUsuario=[]
								dataUser=self.driver.find_elements(by=By.XPATH, value='//*[@class="valor_validar"]')
								if len(dataUser[1].text)==0 and len(dataUser[3].text)==0 and len(dataUser[4].text)==0 and len(dataUser[5].text)==0 and len(dataUser[6].text)==0 and len(dataUser[7].text)==0:
									return 0
						
								tabla=self.driver.find_element(by=By.XPATH, value='//*[@id="CTA_SUSCRIPTOR"]/fieldset/table').text
								x=tabla.split("\n")
								for i, dato in enumerate(x):
									if i%2!=0:
										ArrayDatosUsuario.append(dato)	
							'''
		return lista_estados


		