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
#
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import timer


def FunGuardar(self,ArrayGestion):	
	ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM",ArrayGestion))

def SelectorMulMarcMYP(self,idBot,Idactividad,ciudad):
	#while 1:
	self.Ciudad=ciudad
	try:
		self.compuerta=False
		Primera_ot=True
		lista_ejecucion=[]
		driver=self.driver               		
		#expander_adelantos(driver)
		sql="""
			SELECT MYP_NID,MYP_CORDEN,MYP_CCUENTA 
			from tbl_hmarcapymintic
			where MYP_NIDBOT='"""+str(Idactividad)+"""' and MYP_CESTADOOT='Pendiente'
			"""
		#print(sql)
		array_datos=ConectorDbMysql().FuncGetInfo(0,sql)
		
		for i,dato in enumerate(array_datos):			
			data=[dato[0],dato[1],dato[2]]
			print(data)									

			ConectorDbMysql().RepActividad(idBot)

			try:
				element = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))			
			except:
				driver.refresh()
				driver.quit()
				return
			#driver.find_element_by_xpath('//*[@id="action-global-search-icon"]').click()
			
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
			else:pass

			
			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))				
			lupa=driver.find_element_by_xpath('//*[@type="search"]')
					
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
				#tokens = []
				#tokens.append(["Consultado", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", timer()[0],timer()[1],"OT NO APTA PARA CONSULTA", data[1]])
				#funcion_guardado(self, tokens)
				FunGuardar(self,[data[0],"Marcacion Fallida"])
				#GestorSqlite().TipificarGestion("Marcacion Fallida",data[0],labor)
				self.compuerta = False
				continue

			if driver.find_element_by_xpath('//*[@class="toa-search-empty"]').text != "":
				self.compuerta=False
				continue
			else:
				pass				
			_lista_lls=""
			_fecha_hoy=fecha_actual(self)
		
			time.sleep(1)
			element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			_lista_lls=driver.find_elements_by_xpath('//*[@class="found-item-activity"]')
			
			if len(_lista_lls)==0:					
				FunGuardar(self,[data[0],"Marcacion Fallida"])
				self.compuerta = False
				continue
			
			for i in range(len(_lista_lls)):					
				gs=0
				while gs<3:
					try:
						fecha_Ot=driver.find_elements_by_xpath('//*[@class="activity-date"]')[i].text							
						time.sleep(0.5)							
						x=driver.find_elements_by_xpath('//*[@class="activity-icon icon"]')[i].get_attribute("style")							
						tipo_ot=driver.find_elements_by_xpath('//*[@class="activity-title"]')[i].text							
						break
					except Exception as e:
						Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
						print(Nomb_error)
						time.sleep(1)
						gs+=1
					
				#seguimiento
				'''ArrColconf=["background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);",
																 			"background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);",
																  			"background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);",
																			'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);',
																		 	]					
																ArrColCon=["background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);",
																			"background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);",
																			"background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);",
																			'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);']					
																
																ArrColMor=["background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);",
																		"background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);",
																 		"background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);",
																		'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);']'''

				ArrColTam=['background-color: rgb(30, 133, 37); border: 1px solid rgb(24, 106, 29);']
				

				#verificar si es optima para marcar
				#1 verificar optima para segimiento					
				MarcarSeg= x in ArrColSeg
				#2 verificar optima para Confirmacion					
				MarcarCon= x in ArrColCon
				#2 verificar optima para demora					
				MarcarMor=  x in ArrColMor

				BotMarcar=[]
				if MarcarSeg==1 and MarcarCon==1 and MarcarMor==1:
					BotMarcar=['segimiento','confirmacion','demora' ]
				elif MarcarSeg==1 and MarcarCon==1 and MarcarMor==0:
					BotMarcar=['segimiento','confirmacion' ]
				elif MarcarSeg==1 and MarcarCon==0 and MarcarMor==0:
					BotMarcar=['segimiento']
				
				elif MarcarSeg==1 and MarcarCon==1 and MarcarMor==0:
					BotMarcar=['segimiento','confirmacion']					
				elif MarcarSeg==0 and MarcarCon==1 and MarcarMor==1:
					BotMarcar=['confirmacion','demora']
				elif MarcarSeg==0 and MarcarCon==1 and MarcarMor==0:
					BotMarcar=['confirmacion']
				
				
				elif MarcarSeg==0 and MarcarCon==1 and MarcarMor==1:
					BotMarcar=['confirmacion','demora']
				elif MarcarSeg==1 and MarcarCon==0 and MarcarMor==1:
					BotMarcar=['segimiento','demora']
				elif MarcarSeg==0 and MarcarCon==0 and MarcarMor==1:
					BotMarcar=['demora']
				else:
					continue

				print("!",BotMarcar)					
				#if fecha_Ot==_fecha_hoy[0] or fecha_Ot==_fecha_hoy[1] or fecha_Ot==_fecha_hoy[2] or fecha_Ot=="":
				#print("==",tipo_ot)
				if fecha_Ot!="Reprogramada":
					if "Backlog" not in  tipo_ot:
						if"Supervision"  not in  tipo_ot:
							driver.find_elements_by_xpath('//*[@class="activity-title"]')[i].click()							
							driver.implicitly_wait(0)
							WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
							time.sleep(1)
							self.compuerta=True
							break
						else:
							print("Tipo ot no apta","="*10)
							self.compuerta=False
							continue
					else:
						print("Tipo ot no apta","="*10)
						self.compuerta=False
						continue
				else:
					print("fecha no apta","="*10)
					self.compuerta=False				
					continue
			

			if self.compuerta==False:					
				tokens=[]
				FunGuardar(self,[data[0],"Marcacion Fallida"])
				#saltar
				self.compuerta=False
				continue
			else:
				pass
			# entrara a backoffice
			                  
			y=0
			while y<3:
				try:
					elemento=driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Backoffice")]')
					elemento.location_once_scrolled_into_view
					driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Backoffice")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					break
				except Exception as e:
					print(e)
					time.sleep(1)
					y+=1

			self.ResGestion=""
			BotMarcar=["CGE","DESPACHO","TAM","ENRRUTAMIENTO","CONFIRMACION"]
			for LaborDo in BotMarcar:
				#print(LaborDo)
				if LaborDo=='CGE':
					#===================================== ingreso al formulario=============================================================
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"CGE")]')))
					driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"CGE")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

					try:
						element2= WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
					except Exception as e:
						driver.back()
						self.ResGestion+="Marcacion CGE Fallida;"
						continue


					tokens=[]
					def AliadoCgoCGE():
						driver.find_element_by_xpath('//*[@value="CSIN04"]').click()						
					AliadoCgoCGE()

					def CausaSoporteIn():
						driver.find_element_by_xpath('//*[@value="CSIN04"').click()

					CausaSoporteIn()
					

					def GestionSoporteInterno():
						driver.find_element_by_xpath('//*[@value="DSIN02"').click()

					GestionSoporteInterno()  # aliado

					def Notas():
						gs=0
						while gs<3:
							try:
								if self.Ciudad=="Bogota":							
									driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Notas Gestion"]').send_keys("\nSeguimiento visita GNP")
								else:
									driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Notas Gestion"]').send_keys(f"\n{data[5]}")
								tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Notas Gestion"]').get_attribute("value"))  # nombre de con quien se realizo la gestion
								break
							except Exception as e:
								print(e)
								gs+=1
								time.sleep(0.5)
						
					Notas()

					WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					driver.find_element_by_xpath('//*[@type="submit" and contains(text(),"OK")]').click()



					self.Primera_ot=True
					self.ResGestion+="Marcacion seguimiento Ok;"
					#GestorSqlite().TipificarGestion("Confirmacion Ok",data[0],labor)
					time.sleep(0.5)
					#lista_data=[]						
										
				elif LaborDo=='confirmacion':
					#===================================== ingreso al formulario=============================================================
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
					driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Confirmación")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

					try:
						element2= WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
					except Exception as e:
						'''try:
													driver.find_element_by_xpath('//*[@action_link_label="select_provider"]').click()
												except:
													salida_noApt(driver)
												Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e'''
						#tokens=[]
						#tokens.append(["Consultado","N/A","N/A","N/A","N/A","N/A","N/A","N/A",timer()[0],timer()[1],"OT NO APTA PARA CONSULTA",data[1]])
						#funcion_guardado(self,tokens)
						
						#GestorSqlite().TipificarGestion("Confirmacion Fallida",data[0],labor)
						#compuerta=False
						self.ResGestion+="Marcacion confirmacion Fallida;"
						driver.back()
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
								if data[4]=="ADELANTO":
									driver.find_element_by_xpath('//*[@value="3" and contains(text(),"ADELANTO")]').click()							
								elif data[4]=="CANCELADA":
									driver.find_element_by_xpath('//*[@value="5" and contains(text(),"CANCELADA")]').click()							
								elif data[4]=="CONFIRMADO":
									driver.find_element_by_xpath('//*[@value="1" and contains(text(),"CONFIRMADO")]').click()
								elif data[4]=="NO CONTACTO":
									driver.find_element_by_xpath('//*[@value="2" and contains(text(),"NO CONTACTO")]').click()							
								elif data[4]=="NUMERO ERRADO":
									driver.find_element_by_xpath('//*[@value="6" and contains(text(),"NUMERO ERRADO")]').click()							
								elif data[4]=="REPROGRAMADA":
									driver.find_element_by_xpath('//*[@value="4" and contains(text(),"REPROGRAMADA")]').click()

								tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_Resultado"]').get_attribute("value")) # resultado confirmacion
								break

							except:
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

					self.ResGestion+='Marcacion confirmacion Ok;'
					driver.find_element_by_xpath('//*[@type="submit" and contains(text(),"OK")]').click()
					WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
									
				elif LaborDo=='demora':
					#===================================== ingreso al formulario=============================================================
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
					driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Despacho")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))


					time.sleep(0.5)
					html=driver.find_element_by_xpath('//*[@id="content" and @class="content"]').text			
					if "CancelarOK" not in html:
						driver.back()
						time.sleep(2)
						driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
						self.ResGestion+='Marcacion demora Fallida;'
						compuerta=False
						continue

					tokens=[]
					def ReporteDemora_ck():
						if driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Reporte Demora"]').get_attribute("checked")==None:
							driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Reporte Demora"]').click()
						else:
							pass
						tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Reporte Demora"]').get_attribute("checked"))  # AGENTE CONFIRMACION
					try:
						ReporteDemora_ck()
					except Exception as e:
						print(e)

					def AliadoCGODespacho():
						if driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Aliado CGO"]').get_attribute("value")!="GNP":
							driver.find_elements_by_xpath('//*[contains(text(),"GNP")]')[2].click()
						else:
							pass
						tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_DESP_Aliado CGO"]').get_attribute("value")) # CONFIRMACION AGENTE

					AliadoCGODespacho()
								
					def HoraReporte():
						gs=0
						while gs<5:
							try:
								if driver.find_element_by_xpath('//*[@aria-label="Hora Reporte"]').get_attribute("value")=="":
									driver.find_element_by_xpath('//*[@aria-label="Hora Reporte"]').clear()
									driver.find_element_by_xpath('//*[@aria-label="Hora Reporte"]').send_keys(timer()[1])
								else:
									pass
								tokens.append(driver.find_element_by_xpath('//*[@aria-label="Hora Reporte"]').get_attribute("value")) # resultado confirmacion
								break

							except:
								time.sleep(1)
								gs+=1

					HoraReporte()


					def PersonaReporte():
						gs=0
						while gs<5:
							try:
								element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Persona Reporte"]')))
								if driver.find_element_by_xpath('//*[@aria-label="Persona Reporte"]').get_attribute("value")=="":
									driver.find_element_by_xpath('//*[@aria-label="Persona Reporte"]').clear()
									driver.find_element_by_xpath('//*[@aria-label="Persona Reporte"]').send_keys("Gestion IVR")     	
								else:
									pass
								tokens.append(driver.find_element_by_xpath('//*[@aria-label="Persona Reporte"]').get_attribute("value"))
								break
							except:
								time.sleep(1)
								gs+=1

					PersonaReporte()  
					
					def HoraMaxEspera():
						gs=0
						while gs<5:
							try:
								element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_Hora maxima reporte"]')))
								driver.find_element_by_xpath('//*[@data-label="BACK_Hora maxima reporte"]').send_keys("01")
								tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_Hora maxima reporte"]').get_attribute("value"))  # nombre de con quien se realizo la gestion
								break
							except:
								gs+=1
								time.sleep(0.5)
					HoraMaxEspera()

					def MinutoMaxEspera():
						gs=0
						while gs<5:
							try:
								driver.find_element_by_xpath('//*[@data-label="BACK_Minuto max esperra"]').send_keys("0")
								tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_Minuto max esperra"]').get_attribute("value"))  # usuario CGO que confirma
								break
							except:
								time.sleep(1)
								gs+=1
					MinutoMaxEspera()

					def NotasHoraMaxEspera():
						gs=0
						while gs<5:
							try:
								driver.find_element_by_xpath('//*[@data-label="BACK_Notas Hora Max de Espera"]').send_keys("Confirmación IVR")
								tokens.append(driver.find_element_by_xpath('//*[@data-label="BACK_Notas Hora Max de Espera"]').get_attribute("value"))  # notas de confirmacion
								break
							except:
								time.sleep(1)
								gs+=1

					NotasHoraMaxEspera()


					def ListaReporteDemora():				
						if data[5]=="Acepta Demora":
							driver.find_element_by_xpath('//*[@value="ADE"]').click()
						elif data[5]=="No Acepta Demora":
							driver.find_element_by_xpath('//*[@value="NAD"]').click()
						elif data[5]=="No contacto":
							driver.find_element_by_xpath('//*[@value="NC"]').click()
						else:
							driver.find_element_by_xpath('//*[@value="ADE"]').click()

					ListaReporteDemora()
					self.ResGestion+='Marcacion demora Ok;'
					
					driver.find_element_by_xpath('//*[@type="submit" and contains(text(),"OK")]').click()	
					WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(0.5)
				
			try:
				error1=driver.find_element_by_xpath('//*[contains(text(),"No se pudo procesar la solicitud. Siga trabajando o póngase en contacto con el administrador para obtener ayuda.")]')
				if error1.is_displayed()==True:
					driver.find_element_by_xpath('//*[@id="notification-clear"]').click()
					driver.find_elements_by_xpath('//*[@class="button dismiss"]')[1].click()
			except:
				pass

			try:
				time.sleep(0.5)
				error2=driver.find_element_by_xpath('//*[contains(text(),"Los cambios no se han enviado. ¿Desea guardar un borrador de las actualizaciones?")]')
				if error2.is_displayed()==True:
					driver.find_element_by_xpath('//*[@class="button submit" and contains(text(),"Sí")]').click()
			except:
				pass
				
			time.sleep(1)
		
		
			try:
				driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
			except Exception as e:
				driver.back()
				driver.back()
				print(e)
				#salida_ot_marcada(driver)
			
			self.Primera_ot=True
			
			ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM", [data[0], self.ResGestion]))
			#GestorSqlite().TipificarGestion(self.ResGestion,data[0],"Marcacion Multiple")
		
		time.sleep(0.5)
		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))
		driver.quit()

	except Exception as e:
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print(Nomb_error)
		try:
			driver.refresh()
			time.sleep(1)
			driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
			time.sleep(1)
			x=1
			while x<5:
				BtnSalida=self.driver.find_element_by_xpath('//*[@class="item-caption __logout __logout"]')
				if BtnSalida.is_displayed():
					BtnSalida.click()
					time.sleep(3)
					break
				else:
					x+=1
					pass
		except:pass			
		driver.quit()