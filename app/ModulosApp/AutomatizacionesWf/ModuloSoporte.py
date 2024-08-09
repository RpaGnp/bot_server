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


from ..interaccionChrome import Botinteraccion
from ..ModelDataBase import ConectorDbMysql


from funciones_varias import *
from reloj_casio import *

def FunGuardar(self,ArrayGestion):	
	ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM",ArrayGestion))


def selector_Soporte(self,idBot,Idactividad):
	driver=self.driver
	Bot=Botinteraccion(driver)
	try:
		compuerta=False
		Primera_ot=True
		lista_ejecucion=[]

		array_datos=ConectorDbMysql().FuncGetSpr(2,"spr_get_ordptemarc",[Idactividad])
		acciones = ActionChains(driver)					
		for i,data in enumerate(array_datos):						
			print(data)
			ConectorDbMysql().RepActividad(idBot)
			try:
				element = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))
			except:pass
			#driver.find_element(by=By.XPATH, value='//*[@id="action-global-search-icon"]').click()

			# refresh wf
			lista_ejecucion.append(1)
			if len(lista_ejecucion)==30:
				driver.refresh()
				time.sleep(10)
				lista_ejecucion=[]

			ConectorDbMysql().RepActividad(idBot)

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
				element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta = False
				continue

			if driver.find_element(by=By.XPATH, value='//*[@class="toa-search-empty"]').text != "":
				compuerta=False
				continue
			else:
				pass


			_fecha_hoy=fecha_actual(self)

			time.sleep(1)
			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			_lista_lls=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
			print("="*40,len(_lista_lls),"="*40)
			if len(_lista_lls)==0:
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta = False
				continue

			for i in range(len(_lista_lls)):
				gs=0
				while gs<5:
					try:
						fecha_Ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-date"]')[i].text
						time.sleep(0.5)
						x=driver.find_elements(by=By.XPATH, value='//*[@class="activity-icon icon"]')[i].get_attribute("style")
						break
					except:
						time.sleep(1)
						gs+=1

				#if x=="background-color: rgb(30, 133, 37); border: 1px solid rgb(24, 106, 29);":
				if fecha_Ot==_fecha_hoy[0] or fecha_Ot=="":
					driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].click()
					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					compuerta=True
					break
				else:
					compuerta=False
					continue
				'''else:
																	compuerta=False
																	continue'''

			if compuerta==False:
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta=False
				continue
			else:
				pass

			if Primera_ot:
				try:
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="column-container"]')))
				except:
					pass

			else:
				pass
			

			driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			#===================================== ingreso al formulario=============================================================
			element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
			driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"CGE")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			#

			time.sleep(0.5)
			html=driver.find_element(by=By.XPATH, value='//*[@id="content" and @class="content"]').text			
			if "CancelarOK" not in html:
				driver.back()
				time.sleep(2)
				driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta=False
				continue
			
			def cedAsesor():
				driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').clear()
				driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').send_keys(data[4])
			#cedAsesor()

			tokens=[]
			def AliadoVentasTecnicas():								
				xpath='//input[@data-label="BACK_CGE_ALIADO_SOP"]'
				acciones.move_to_element(driver.find_element(By.XPATH,xpath)).perform()
				driver.find_element(by=By.XPATH, value=xpath).click()
				try:									
					driver.find_element(by=By.XPATH, value='//*[@aria-label="GNP"]').click()
				except:
					pass



			def CausaSoporteInterno():				
				elemento=driver.find_element(By.XPATH,'//input[@data-label="BACK_CGE_Causa Soporte In"]')
				acciones.move_to_element(elemento).perform()

				driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_CGE_Causa Soporte In"]').click()
				#if driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_CGE_Causa Soporte In"]').get_attribute("value")!="CSIN02":
				driver.find_element(by=By.XPATH, value='//*[@data-value="CSIN02" and contains(text(),"Seguimiento VIP")]').click()
				#else:
				#	pass
			
			
			AliadoVentasTecnicas()
			time.sleep(1)
			CausaSoporteInterno()

			def AliadoCGOCGE():
				elemento=driver.find_element(By.XPATH,'//input[@data-label="BACK_CGE_Aliado CGO"]')
				acciones.move_to_element(elemento).perform()
				driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_CGE_Aliado CGO"]').click()				
				driver.find_element(by=By.XPATH, value='//div[@data-value="GNP"]').click()

			AliadoCGOCGE()

			def Notas():
				driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_CGE_Notas Causa Soporte In"]').send_keys('\nok')
				
			Notas()


			def GestionSopoInterno():
				driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_CGE_Gestion Soporte In"]').click()
				try:
					
					driver.find_element(by=By.XPATH, value='//*[@title="Recomendación OK"]').click()
					
				except:
					time.sleep(1)
					

			GestionSopoInterno()  # aliado

			def NotasFin():				
				try:
					driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_CGE_Notas Gestion Soporte In"]').send_keys('\nok')
					
				except:					
					time.sleep(0.5)
			NotasFin()

			time.sleep(1)
			driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()			
			WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			
	
			time.sleep(1)
		
		
			try:
				element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]')))
				driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
			except Exception as e:
				driver.back()
				driver.back()
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)
					
			


			Primera_ot=True

			sql = ("SPR_UPD_ESTACTM", [data[0], 'Ot marcada con exito'])
			ConectorDbMysql().FuncInsInfoOne(sql)
			# si aparece la ventana de confirmacion darle continuar********************************************
			time.sleep(0.5)
		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))
		driver.quit()
		
	except Exception as e:
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print(Nomb_error)		
		try:
			driver.refresh()
			time.sleep(3)
			driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
			time.sleep(1)
			while 1:
				BtnSalida = self.driver.find_element(by=By.XPATH, value='//*[@class="item-caption __logout __logout"]')
				if BtnSalida.is_displayed():
					BtnSalida.click()
					time.sleep(3)
					break
				else:
					pass
		except:pass
		try:
			driver.quit()
		except:pass