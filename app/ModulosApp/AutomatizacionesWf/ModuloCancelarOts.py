#LIBRERIAS PARA CHROMEDRIVER***********************
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
import sys
import os
from datetime import date
from datetime import datetime
from datetime import timedelta

from ..interaccionChrome import Botinteraccion
from ..ModelDataBase import ConectorDbMysql

from funciones_varias import *
from reloj_casio import *


def FunGuardar(self,ArrayGestion):	
	ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM",ArrayGestion))

def SelectorCanOrden(self,idBot,idActividad):
	driver=self.driver
	try:
		sql="""
				SELECT ACM_NID,ACM_CORDEN,ACM_CMISELANEOS0
				FROM tbl_hactmarcacionbot
				WHERE ACM_NIDBOT='"""+str(idActividad)+"""' AND  ACM_CESTADOOT='Pendiente';
			"""
		array_datos=ConectorDbMysql().FuncGetInfo(0,sql)
		for data in array_datos:
			ConectorDbMysql().RepActividad(idBot)

			try:
				element = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))
			except:pass

			try:					
				driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			except:pass

			# funcion de salida, pausa del bot
			Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idBot]))
			# print(Dato[0])
			if Dato[0] != None:
				if Dato[0] == "Pausar":
					while 1:
						ConectorDbMysql().RepActividad(idBot)
						time.sleep(3)
						Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idBot]))
						if Dato[0] != None:
							if Dato[0] == "Reanudar":
								ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTBOTGES", [idBot]))
								break
						elif Dato[0] == "Eliminar":
							ConectorDbMysql().FuncInsInfoOne(
								("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
							driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
							time.sleep(1)
							while 1:
								BtnSalida = self.driver.find_element(by=By.XPATH, value=
									'//*[@class="item-caption __logout __logout"]')
								if BtnSalida.is_displayed():
									BtnSalida.click()
									time.sleep(3)
									break
								else:
									pass
							driver.quit()
							return

				elif Dato[0] == "Eliminar":
					ConectorDbMysql().FuncInsInfoOne(
						("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
					driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
					time.sleep(1)
					while 1:
						BtnSalida = self.driver.find_element(by=By.XPATH, value=
							'//*[@class="item-caption __logout __logout"]')
						if BtnSalida.is_displayed():
							BtnSalida.click()
							time.sleep(3)
							break
						else:
							pass
					driver.quit()
					return
			else:
				pass


			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))
			lupa=driver.find_element(by=By.XPATH, value='//*[@type="search"]')
			#print(lupa.is_displayed())
			if lupa.is_displayed()==False:
				driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()
			else:
				pass

			driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(data[1])
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)


			try:
				element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))			
			except Exception as e:					
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)
				FunGuardar(self,[data[0],"Cancelacion Fallida"])
				compuerta = False
				continue

			_fecha_hoy=fecha_actual(self)
			_lista_lls=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
			if len(_lista_lls)==0:
				FunGuardar(self,[data[0],"Cancelacion Fallida"])
				compuerta = False
				continue

			FunGuardar(self,[data[0],"Orden consultada"])						
			for i in range(len(_lista_lls)):
				gs=0
				while gs<5:
					try:
						fecha_Ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-date"]')[i].text
						time.sleep(0.5)
						x=driver.find_elements(by=By.XPATH, value='//*[@class="activity-icon icon"]')[i].get_attribute("style")
						tipo_ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].text	
						break
					except:
						time.sleep(1)
						gs+=1

				if x not in ("background-color: rgb(255, 50, 17); border: 1px solid rgb(204, 40, 13);",
						 "background-color: rgb(55, 48, 255); border: 1px solid rgb(44, 38, 204);",
						"background-color: rgb(30, 133, 37); border: 1px solid rgb(24, 106, 29);",
						"background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);",
						"background-color: rgb(111, 55, 135); border: 1px solid rgb(88, 44, 108);"
						):

					if "Backlog" not in  tipo_ot:
						driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].click()							
						driver.implicitly_wait(0)
					else:
						continue
				else:					
					continue

				WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))							
				while 1:
					try:
						driver.find_element(By.XPATH,'//span[@class="app-button-title" and contains(text(),"Cancelar")]').click()						
						break
					except:
						time.sleep(2)
				time.sleep(2)
				driver.find_element(By.XPATH,'//DIV[@class="form-text-field custom-text-field"]').click()
				if driver.find_element(By.XPATH,'//DIV[@aria-label="CANCELADA POR REAGENDACIÓN DE LA ORDEN ORIGINAL"]').is_displayed():
					driver.find_element(By.XPATH,'//DIV[@aria-label="CANCELADA POR REAGENDACIÓN DE LA ORDEN ORIGINAL"]').click()


				driver.find_element(By.XPATH,'//textarea[@aria-label="Cancel notes"]').send_keys(data[2])							
				time.sleep(2)
				driver.find_element(By.XPATH,'//button[@type="submit"]').click()


				sql = ("SPR_UPD_ESTACTM", [data[0], 'Ot cancelada con exito'])
				ConectorDbMysql().FuncInsInfoOne(sql)
				break


		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, idActividad, 'Labor Terminada']))
		try:			
		    driver.refresh()
		    time.sleep(4)
		    driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
		    time.sleep(1)
		    driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
		    time.sleep(5)		    #ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM", [data[0], "Error de marcacion"]))            
		except:pass	
		driver.quit()
	except Exception as e:
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print(Nomb_error)
		try:			
		    driver.refresh()
		    time.sleep(4)
		    driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
		    time.sleep(1)
		    driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
		    time.sleep(5)		    #ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM", [data[0], "Error de marcacion"]))            
		except:pass		
		driver.quit()