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

import time
import csv
import sys
import os
from datetime import date
from datetime import datetime
from datetime import timedelta

import threading



def salida_segura_act(driver):
	if driver.title != "Oracle Field Service":		
		if driver.find_element(by=By.XPATH, value='//*[@id="screen-title"]').text == "Agregar actividad":
			driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()
			time.sleep(7)

		WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

		driver.find_element(by=By.XPATH, value='//*[@class="user-menu" and @role="button"]').click()
		time.sleep(1)
		driver.find_element(by=By.XPATH, value='//*[@class="item-caption __logout __logout"]').click()
		time.sleep(5)
		WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
		time.sleep(1)
	driver.quit()

def salida_Can(driver):
	if driver.title != "Oracle Field Service":
		driver.back()
		time.sleep(1)
		driver.back()
		time.sleep(5)
		WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
		driver.find_elements(by=By.XPATH, value='//*[@data-bind="text: initials"]')[1].click()
		time.sleep(1)
		driver.find_element(by=By.XPATH, value='//*[@class="item-caption __logout"]').click()
		time.sleep(7)
		WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
	driver.quit()

def salida_adelantos(driver):
	x=0
	while x<3:
		try:
			if driver.title != "Oracle Field Service":
				if driver.title=="Confirmación - Oracle Field Service":
					driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(5)

				if driver.title=="'Backoffice - Oracle Field Service'":
					driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(7)

				if driver.title=='Detalles de actividad - Oracle Field Service':
					driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(7)


				WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
				driver.find_elements(by=By.XPATH, value='//*[@data-bind="text: initials"]')[1].click()
				time.sleep(1)
				driver.find_element(by=By.XPATH, value='//*[@class="item-caption __logout"]').click()
				time.sleep(7)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

			break
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)
			driver.refresh()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			x+=1
		finally:
			driver.quit()

def salida_ot_marcada(driver):
	x=0
	while x<5:	
		try:
			try:
				botondos = driver.find_element(by=By.XPATH, value='//*[@id="slot-panel-title" and contains(text(),"Los cambios no se han enviado. ¿Desea guardar un borrador de las actualizaciones?")]')
				if botondos.is_displayed() == True:
				    time.sleep(0.5)
				    botondos.click()
			except:
				pass
			print("1",driver.title)

			WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"Confirmación")]')))
			driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()				
			driver.implicitly_wait(20)
			print("2",driver.title)


			#WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"Información de la Actividad")]')))

			WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="context-layout"]/div/div[1]/div[1]/div[1]/div/div[1]/header')))
			driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			break
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			time.sleep(3)
			x+=1

def salida_noApt(driver):
	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@title="Confirmación"]')))
	driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()				
	driver.implicitly_wait(20)
	
	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@class="button inline"]')))
	driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()				
	driver.implicitly_wait(20)


	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="context-layout"]/div/div[1]/div[1]/div[1]/div/div[1]/header')))			
	driver.find_element(by=By.XPATH, value='//*[@class="title-flex-item-left"]').click()
	WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

def salida_Cancelar(driver):
	pass

def fecha_actual(self):	
	FechaHora = datetime.now()
	dia_semana = {"Sunday": "Dom", "Monday": "Lun", "Tuesday": "Mar", "Wednesday": "Mie", "Thursday": "Jue",
				  "Friday": "Vie", "Saturday": "Sab"}
	nombre_dia = FechaHora.strftime('%A')
	dia_actual = dia_semana[str(nombre_dia)] + ","
	_dia = FechaHora.strftime('%d')
	hoy = int(_dia)
	dic_mes = {"January": "Ene", "February": "Feb", "March": "Mar", "April": "Abr", "May": "May", "June": "Jun",
			   "July": "Jul", "August": "Ago", "September": "Sep", "October": "Oct", "November": "Nov",
			   "December": "Dic"}
	_mes = dic_mes[str(FechaHora.strftime('%B'))]
	data_fecha = dia_actual + " " + str(hoy) + " " + _mes

	# fecha del dia siguiente
	ahora = datetime.now()
	tomorrow = ahora + timedelta(days=1)
	x = tomorrow.strftime('%d')
	x = int(x)
	nombre_dia = tomorrow.strftime('%A')
	dia_mañana = dia_semana[str(nombre_dia)] + ","
	_mes = dic_mes[str(tomorrow.strftime('%B'))]
	data_fecha_tomorrow = dia_mañana + " " + str(x) + " " + _mes
	# fecha del pasado mañana

	ahora = datetime.now()
	tomorrow = ahora + timedelta(days=2)
	x = tomorrow.strftime('%d')
	x = int(x)
	nombre_dia = tomorrow.strftime('%A')
	dia_pasado = dia_semana[str(nombre_dia)] + ","
	_mes = dic_mes[str(tomorrow.strftime('%B'))]
	data_fecha_pasado = dia_pasado + " " + str(x) + " " + _mes
	
	return data_fecha, data_fecha_tomorrow, data_fecha_pasado

def fecha_acteng(self):
	FechaHora = datetime.now()
	dia_semana = {"Sunday": "Sun", "Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed", "Thursday": "Thu",
				  "Friday": "Fri", "Saturday": "Sat"}
	nombre_dia = FechaHora.strftime('%A')
	dia_actual = dia_semana[str(nombre_dia)] + ","
	_dia = FechaHora.strftime('%d')
	hoy = int(_dia)
	dic_mes = {"January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr", "May": "May", "June": "Jun",
			   "July": "Jul", "August": "Ago", "September": "Sep", "October": "Oct", "November": "Nov",
			   "December": "Dec"}
	_mes = dic_mes[str(FechaHora.strftime('%B'))]
	data_fecha = dia_actual + " " + str(hoy) + " " + _mes

	# fecha del dia siguiente
	ahora = datetime.now()
	tomorrow = ahora + timedelta(days=1)
	x = tomorrow.strftime('%d')
	x = int(x)
	nombre_dia = tomorrow.strftime('%A')
	dia_mañana = dia_semana[str(nombre_dia)] + ","
	_mes = dic_mes[str(tomorrow.strftime('%B'))]
	data_fecha_tomorrow = dia_mañana + " " + str(x) + " " + _mes
	# fecha del pasado mañana

	ahora = datetime.now()
	tomorrow = ahora + timedelta(days=2)
	x = tomorrow.strftime('%d')
	x = int(x)
	nombre_dia = tomorrow.strftime('%A')
	dia_pasado = dia_semana[str(nombre_dia)] + ","
	_mes = dic_mes[str(tomorrow.strftime('%B'))]
	data_fecha_pasado = dia_pasado + " " + str(x) + " " + _mes


	return data_fecha, data_fecha_tomorrow, data_fecha_pasado

def validador_numerico(dato):
	if dato in ["0","1","2","3","4","5","6","7","8","9"]:
		escalar=f"0{dato}"
	else:
		escalar=dato
	return escalar.strip()

