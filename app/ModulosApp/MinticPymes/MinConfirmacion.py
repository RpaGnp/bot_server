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


from ..ModelDataBase import ConectorDbMysql

from funciones_varias import *
from reloj_casio import *

def FunGuardar(self,ArrayGestion):	
	ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM",ArrayGestion))


def selector_Confirmacion(self,idBot,Idactividad):
	driver=self.driver
	try:
		compuerta=False
		Primera_ot=True
		lista_ejecucion=[]


		sql="""
			SELECT ACM_NID,ACM_CORDEN,ACM_CCUENTA,ACM_CMISELANEOS0
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
			#driver.find_element_by_xpath('//*[@id="action-global-search-icon"]').click()

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
							driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
							time.sleep(1)
							while 1:
								BtnSalida = self.driver.find_element_by_xpath(
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
					driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
					time.sleep(1)
					while 1:
						BtnSalida = self.driver.find_element_by_xpath(
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
			lupa=driver.find_element_by_xpath('//*[@type="search"]')
			#print(lupa.is_displayed())
			if lupa.is_displayed()==False:
				driver.find_element_by_xpath('//*[@aria-label="GlobalSearch"]').click()
			else:
				pass

			driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
			driver.find_element_by_xpath('//*[@class="search-bar-input"]').clear()
			driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(data[1])
			driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(Keys.ENTER)

			try:
				element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta = False
				continue

			if driver.find_element_by_xpath('//*[@class="toa-search-empty"]').text != "":
				compuerta=False
				continue
			else:
				pass


			_fecha_hoy=fecha_actual(self)

			time.sleep(1)
			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			_lista_lls=driver.find_elements_by_xpath('//*[@class="found-item-activity"]')
			print("="*40,len(_lista_lls),"="*40)
			if len(_lista_lls)==0:
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta = False
				continue

			for i in range(len(_lista_lls)):
				gs=0
				while gs<5:
					try:
						fecha_Ot=driver.find_elements_by_xpath('//*[@class="activity-date"]')[i].text
						time.sleep(0.5)
						x=driver.find_elements_by_xpath('//*[@class="activity-icon icon"]')[i].get_attribute("style")
						break
					except:
						time.sleep(1)
						gs+=1

				if x=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);" or x=="background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);" or x=="background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);"\
						or x=='background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);':

					if fecha_Ot==_fecha_hoy[0] or fecha_Ot==_fecha_hoy[1] or fecha_Ot==_fecha_hoy[2] or fecha_Ot=="":
						driver.find_elements_by_xpath('//*[@class="activity-title"]')[i].click()
						driver.implicitly_wait(0)
						WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
						compuerta=True
						break
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
				try:
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="context-layout"]/div/div[1]/div[1]/div[1]/div/div[1]/header/span')))
				except:
					pass

			else:
				pass
			driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Backoffice")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			#===================================== ingreso al formulario=============================================================
			element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
			driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Confirmación")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))


			time.sleep(0.5)
			html=driver.find_element_by_xpath('//*[@id="content" and @class="content"]').text			
			if "CancelarOK" not in html:
				driver.back()
				time.sleep(2)
				driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta=False
				continue
				

			tokens=[]
			def agente_confirmacion_ck():
				try:
					if driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation"]').get_attribute("checked")==None:
						driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation"]').click()
						tokens.append(driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation"]').get_attribute("checked"))  # AGENTE CONFIRMACION
					else:
						pass
				except:
					tokens.append("Elemento NO disponible")

			agente_confirmacion_ck()

			def confirmacion_agente_ck():
				if driver.find_element_by_xpath('//*[@data-label="XA_Confirmation_IVR"]').get_attribute("checked")==None:
					driver.find_element_by_xpath('//*[@data-label="XA_Confirmation_IVR"]').click()
				else:
					pass
				tokens.append(driver.find_element_by_xpath('//*[@data-label="XA_Confirmation_IVR"]').get_attribute("checked")) # CONFIRMACION AGENTE

			confirmacion_agente_ck()

			def R_confirmacion():
				gs=0

				while gs<2:
					try:
						#print(data[3])
						if data[3]=="ADELANTO":
							driver.find_element_by_xpath('//*[@value="3" and contains(text(),"ADELANTO")]').click()
						elif data[3]=="CANCELADA":
							driver.find_element_by_xpath('//*[@value="5" and contains(text(),"CANCELADA")]').click()
						elif data[3]=="CONFIRMADO":
							driver.find_element_by_xpath('//*[@value="1" and contains(text(),"CONFIRMADO")]').click()
						elif data[3]=="NO CONTACTO":
							driver.find_element_by_xpath('//*[@value="2" and contains(text(),"NO CONTACTO")]').click()
						elif data[3]=="NUMERO ERRADO":
							driver.find_element_by_xpath('//*[@value="6" and contains(text(),"NUMERO ERRADO")]').click()
						elif data[3]=="REPROGRAMADA":
							driver.find_element_by_xpath('//*[@value="4" and contains(text(),"REPROGRAMADA")]').click()

						tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_Resultado"]').get_attribute("value")) # resultado confirmacion
						break

					except Exception as e:
						print(e)
						time.sleep(1)
						gs+=1

			R_confirmacion()


			def aliado():
				gs=0
				while gs<2:
					try:
						element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_CONF_Aliado CGO"]')))
						if driver.find_element_by_xpath('//*[@data-label="BACK_CONF_Aliado CGO"]').get_attribute("value")!="4":
							driver.find_elements_by_xpath('//*[contains(text(),"GNP")]')[2].click()
						else:
							pass
						tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_CONF_Aliado CGO"]').get_attribute("value"))
						break
					except:
						time.sleep(1)
						gs+=1

			aliado()  # aliado

			def cliente_gestion():
				gs=0
				while gs<2:
					try:
						element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="XA_Agent_Confirmation_Approver"]')))
						driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_Approver"]').clear()
						driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_Approver"]').send_keys("Gestion IVR")
						tokens.append(driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_Approver"]').get_attribute("value"))  # nombre de con quien se realizo la gestion
						break
					except:
						gs+=1
						time.sleep(0.5)
			cliente_gestion()

			def usuario_CGO():
				gs=0
				while gs<2:
					try:
						#driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_User"]').clear()
						driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_User"]').send_keys("Gestion IVR")
						tokens.append(driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_User"]').get_attribute("value"))  # usuario CGO que confirma
						break
					except:
						time.sleep(1)
						gs+=1
			usuario_CGO()

			def notas_confirmacion():
				gs=0
				while gs<2:
					try:

						driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_Notes"]').send_keys("\nGestion IVR")
						tokens.append(driver.find_element_by_xpath('//*[@data-label="XA_Agent_Confirmation_Notes"]').get_attribute("value"))  # notas de confirmacion
						break
					except:
						time.sleep(1)
						gs+=1

			notas_confirmacion()


			driver.find_element_by_xpath('//*[@type="submit" and contains(text(),"OK")]').click()
			try:
				WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class=""loading-animated-icon big jbf-init-loading-indicator""]')))
			except:
				pass


			try:
				driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
			except:
				salida_ot_marcada(driver)

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
			driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
			time.sleep(1)
			while 1:
				BtnSalida = self.driver.find_element_by_xpath('//*[@class="item-caption __logout __logout"]')
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