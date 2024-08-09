import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver import ActionChains
import time
import csv
import sys
from datetime import date
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import os


class GestionCompletar:
	"""docstring for ClassName"""#
	def __init__(self,driver, ArrayGestion):		
		self.ArrayGestion = ArrayGestion
		self.driver=driver		
		

	def _NotasCompletar(self):		
		self.driver.find_element(By.XPATH,'//div[@class="form-textarea"]//textarea').clear()
		time.sleep(0.5)
		self.driver.find_element(By.XPATH,'//div[@class="form-textarea"]//textarea').send_keys(self.ArrayGestion[2])
		#resultado gestion
		self.driver.find_element(By.XPATH,'//input[@class="form-item dropdown-value"]').click()
		time.sleep(0.5)
		self.driver.find_element(By.XPATH,'//div[@aria-label="Resultado de la Gestión, Requerido"]/div[contains(text(),"%s")]'%self.ArrayGestion[3]).click()
		time.sleep(1)
		self.driver.find_element(By.XPATH,'//button[@type="submit"]').click()

	def _Completar(self):
		c=0
		while c<5:
			try:
				self.driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Completar")]').click()
				break
			except:
				time.sleep(1)
				c+=1
		self.driver.implicitly_wait(0)
		WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
		self._NotasCompletar()
		time.sleep(1)
		
		#self.driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
		try:
			if self.driver.find_element(by=By.XPATH, value='//*[@class="redwood-dialog__content"]').is_displayed():
				self.driver.find_element(by=By.XPATH, value='//*[@class="button submit" and contains(text(),"Continuar")]').click()

		except:
			pass
		self.driver.implicitly_wait(0)
		WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
		return 1

	def _Razonar(self):
		pass


	def NotasBack(self):
		self.driver.find_element(By.XPATH,'//div/div/a[contains(text(),"Notas")]').click()
		while 1:
			if self.driver.title=='Notas - Oracle Field Service':
				break
			else:
				time.sleep(2)

		self.driver.find_element(By.XPATH,'//div[@class="form-textarea"]/textarea').send_keys(self.ArrayGestion[2])
		time.sleep(1)
		self.driver.find_element(By.XPATH,'//button[@type="submit"]').click()
		return True

	def Finalizar(self):
		if self.ArrayGestion[1]=="COMPLETADA":
			self._Completar()