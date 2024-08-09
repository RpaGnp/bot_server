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


def selector_Confirmacion(self,idBot,Idactividad):
	driver=self.driver
	Bot=Botinteraccion(driver)
	try:
		compuerta=False
		Primera_ot=True
		lista_ejecucion=[]


		sql="""
			SELECT ACM_NID,ACM_CORDEN,ACM_CCUENTA,ACM_CMISELANEOS0,ACM_CCEDUSU
			FROM tbl_hactmarcacionbot
			WHERE ACM_NIDBOT='"""+str(Idactividad)+"""' AND  ACM_CESTADOOT='Pendiente';
		"""
		#print(sql)
		array_datos=ConectorDbMysql().FuncGetInfo(0,sql)
		for i,dato in enumerate(array_datos):
			data=[dato[0],dato[1],dato[3],dato[2]]
			del dato
			print(data)
			ConectorDbMysql().RepActividad(idBot)
			try:
				element = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))
			except:pass

			try:					
				driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			except:pass
			#driver.find_element(by=By.XPATH, value='//*[@id="action-global-search-icon"]').click()

			# refresh wf
			lista_ejecucion.append(1)
			if len(lista_ejecucion)==30:
				driver.refresh()
				time.sleep(10)
				lista_ejecucion=[]

			
			# funcion de salida, pausa del bot
			Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idBot]))
			# print(Dato[0])
			if Dato[0] != None:
				if Dato[0] == "Eliminar":
					ConectorDbMysql().FuncInsInfoOne(
						("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
					driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
					time.sleep(1)					
					driver.quit()
					return
			else:
				pass

			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))
			lupa=driver.find_element(by=By.XPATH, value='//*[@type="search"]')
			#print(lupa.is_displayed())
			if lupa.is_displayed()==False:
				try:				
					driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()
				except:
					pass
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
						tipo_ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].text	
						print(tipo_ot)						
						break
					except:
						time.sleep(1)
						gs+=1
				#amarillo,gris,naranja,verde claro
				if x in ("background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);",
					"background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);",
					"background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);",
					'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);'):

					if fecha_Ot==_fecha_hoy[0] or fecha_Ot==_fecha_hoy[1] or fecha_Ot==_fecha_hoy[2] or fecha_Ot=="" :
						if "Backlog" not in  tipo_ot:
							if "Supervision"  not in  tipo_ot:
								if "Backoffice" not in  tipo_ot:												 
									driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].click()							
									driver.implicitly_wait(0)
									WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
									time.sleep(1)
									compuerta=True
									break
								else:							
									compuerta=False
									continue
							else:							
								compuerta=False
								continue
						else:							
							compuerta=False
							continue

					else:
						compuerta=False
						continue
				else:
					compuerta=False
					continue

			if compuerta==False:
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta=False
				continue
			else:
				pass
			

			if Primera_ot:				
				element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Backoffice")]')))
			else:
				pass
			
			driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]').click()			
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			#===================================== ingreso al formulario=============================================================
			element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
			driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Confirmación")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))


			time.sleep(2)
			html= driver.find_element(By.XPATH, '//*[@id="content" and @class="content"]').text			
			if "\nCancelar\nOK" not in html:
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
			def agente_confirmacion_ck():
				try:
					if driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').get_attribute("checked")==None:
						driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').click()
						tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').get_attribute("checked"))  # AGENTE CONFIRMACION
					else:
						pass
				except:
					tokens.append("Elemento NO disponible")

			agente_confirmacion_ck()

			def confirmacion_agente_ck():
				if driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Confirmation_IVR"]').get_attribute("checked")==None:
					driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Confirmation_IVR"]').click()
				else:
					pass
				tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Confirmation_IVR"]').get_attribute("checked")) # CONFIRMACION AGENTE
			try:
				confirmacion_agente_ck()
			except:
				pass

			def R_confirmacion():
				driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Resultado"]').click()
				gs=0
				while gs<2:
					try:
						EstConf=data[2].strip()
						if EstConf=="ADELANTO":
							driver.find_element(by=By.XPATH, value='//*[@title="ADELANTO"]').click()
						elif EstConf=="CANCELADA":
							driver.find_element(by=By.XPATH, value='//*[@title="CANCELADA"]').click()
						elif EstConf=="CONFIRMADO":
							driver.find_element(by=By.XPATH, value='//*[@title="CONFIRMADO"]').click()
						elif EstConf=="NO CONTACTO":
							driver.find_element(by=By.XPATH, value='//*[@title="NO CONTACTO"]').click()
						elif EstConf=="NUMERO ERRADO":
							driver.find_element(by=By.XPATH, value='//*[@title="NUMERO ERRADO"]').click()
						elif EstConf=="REPROGRAMADA":
							driver.find_element(by=By.XPATH, value='//*[@atitle="REPROGRAMADA")]').click()
						else:
							driver.find_element(by=By.XPATH, value='//*[@title="CONFIRMADO"]').click()
						tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Resultado"]').get_attribute("value")) # resultado confirmacion
						break

					except Exception as e:
						print(e)
						time.sleep(1)
						gs+=1
			try:
				R_confirmacion()
			except:pass



			def aliado():				
				driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_CONF_Aliado CGO"]').click()
				gs=0
				while gs<2:
					try:
						element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_CONF_Aliado CGO"]')))
						if driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_CONF_Aliado CGO"]').get_attribute("value")!="GNP":
							driver.find_element(by=By.XPATH, value='//div[@data-value="GNP"]').click()        	
						else:
							pass						
						break
					except Exception as e:
						print(e)
						time.sleep(1)
						gs+=1

			
			aliado()  # aliado


			def cliente_gestion():
				gs=0
				while gs<2:
					try:
						element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="XA_Agent_Confirmation_Approver"]')))
						driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Approver"]').clear()
						driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Approver"]').send_keys("Gestion IVR")
						tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Approver"]').get_attribute("value"))  # nombre de con quien se realizo la gestion
						break
					except:
						gs+=1
						time.sleep(0.5)
			cliente_gestion()

			def usuario_CGO():
				gs=0
				while gs<2:
					try:
						#driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_User"]').clear()
						driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_User"]').send_keys("Gestion IVR")
						tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_User"]').get_attribute("value"))  # usuario CGO que confirma
						break
					except:
						time.sleep(1)
						gs+=1
			usuario_CGO()

			def notas_confirmacion():
				gs=0
				while gs<2:
					try:

						driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Notes"]').send_keys("\nGestion IVR")
						tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Notes"]').get_attribute("value"))  # notas de confirmacion
						break
					except:
						time.sleep(1)
						gs+=1

			notas_confirmacion()
			x=0
			while 'Confirmación.' in driver.title and x <3:
				try:
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
					driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()
					time.sleep(2)
				except Exception as e:
					x+=1
					time.sleep(2)
					print(driver.title)			
				
			time.sleep(1)
		
			
			try:
				element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]')))
				driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
			except Exception as e:
				driver.back()
				time.sleep(2)
				driver.back()
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)

			while 'Backoffice' in driver.title:
				driver.back()
			else:pass
			

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
			time.sleep(4)
			driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
			time.sleep(1)
			driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
			time.sleep(5)
			ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM", [data[0], "Error de marcacion"]))                        
		except:pass
		try:
			driver.quit()
		except:pass