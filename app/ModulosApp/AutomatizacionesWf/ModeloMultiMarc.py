###LIBRERIAS PARA CHROMEDRIVER***********************
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
from ..interaccionChrome import Botinteraccion
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import timer


def FunGuardar(self,ArrayGestion):	
	ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM",ArrayGestion))

def SelectorMDCS(self,idBot,Idactividad):
	#while 1:	
	try:
		self.compuerta=False
		Primera_ot=True
		lista_ejecucion=[]
		driver=self.driver               		
		Bot=Botinteraccion(driver)		
		array_datos=ConectorDbMysql().FuncGetSpr(2,"spr_get_ordptemarc",[Idactividad])		

		for i,data in enumerate(array_datos):						
			print(data)
			ConectorDbMysql().RepActividad(idBot)			

			#driver.find_element(by=By.XPATH, value='//*[@id="action-global-search-icon"]').click()
			
			# refresh wf
			lista_ejecucion.append(1)
			if len(lista_ejecucion)==30:
				driver.refresh()
				time.sleep(10)
				lista_ejecucion=[]

						# funcion de salida, pausa del bot

			try:
				cedulaAsesor = ConectorDbMysql().FunGetProcedure(["spr_get_idaseasi",[data[2]]])[0]				
			except Exception as e:
				time.sleep(2)
				print(e)
				FunGuardar(self,[data[0],"Tecnico sin asignacion de asesor"])
				continue

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
							ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
							try:			
							    driver.refresh()
							    time.sleep(4)
							    driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
							    time.sleep(1)
							    driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
							    time.sleep(5)							    
							except:pass		
							driver.quit()
							return

				elif Dato[0] == "Eliminar":
					ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
					try:			
						driver.refresh()
						time.sleep(4)
						driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
						time.sleep(1)
						driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
						time.sleep(5)							    
					except:pass		
					
					driver.quit()
					return
			else:pass

			try:
				element = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))			
			except:
				driver.refresh()
				driver.quit()
				return
			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))				
			
			lupa=driver.find_element(by=By.XPATH, value='//div[@id="search-bar-container"]')						
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
				#tokens = []
				#tokens.append(["Consultado", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", timer()[0],timer()[1],"OT NO APTA PARA CONSULTA", data[1]])
				#funcion_guardado(self, tokens)
				FunGuardar(self,[data[0],"Marcacion Fallida"])
				#GestorSqlite().TipificarGestion("Marcacion Fallida",data[0],labor)
				self.compuerta = False
				continue

			if driver.find_element(by=By.XPATH, value='//*[@class="toa-search-empty"]').text != "":
				self.compuerta=False
				continue
			else:
				pass				
			_lista_lls=""
			_fecha_hoy=fecha_actual(self)
		
			time.sleep(1)
			element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			_lista_lls=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
			
			if len(_lista_lls)==0:					
				FunGuardar(self,[data[0],"Marcacion Fallida"])
				self.compuerta = False
				continue
			
			for i in range(len(_lista_lls)):					
				gs=0
				while gs<3:
					try:
						fecha_Ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-date"]')[i].text							
						time.sleep(0.5)							
						x=driver.find_elements(by=By.XPATH, value='//*[@class="activity-icon icon"]')[i].get_attribute("style")							
						tipo_ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].text							
						break
					except Exception as e:
						Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
						print(Nomb_error)
						time.sleep(1)
						gs+=1
					
				#seguimiento
				ArrColSeg=["background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);",
				 			"background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);",
				  			"background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);",
							'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);',
						 	'background-color: rgb(30, 133, 37); border: 1px solid rgb(24, 106, 29);']					
				
				ArrColCon=['background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);',
							'background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);',
							'background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);',
							'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);']



				ArrColMor=["background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);",
						"background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);",
				 		"background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);",
						'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);']

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
						
				#if fecha_Ot==_fecha_hoy[0] or fecha_Ot==_fecha_hoy[1] or fecha_Ot==_fecha_hoy[2] or fecha_Ot=="":
				#print("==",tipo_ot)
				if fecha_Ot!="Reprogramada":					
						if "Backlog" not in tipo_ot:
							if "Supervision" not in tipo_ot:
								if "Backoffice" not in tipo_ot:
									driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].click()							
									driver.implicitly_wait(0)
									WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
									print("Ingresar a la orden!")
									self.compuerta=True
									break
								else:
									self.compuerta=False
									continue
							else:
								self.compuerta=False		
								continue
						else:							
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
			while y<2:
				try:
					elemento=driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]')
					elemento.location_once_scrolled_into_view
					driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					break
				except Exception as e:
					print(e)
					time.sleep(1)
					y+=1
			if y>2:
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM", [data[0], "orden no marcable"]))
				continue


			self.ResGestion=""
			driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			for LaborDo in BotMarcar:
				#print(LaborDo)
				if LaborDo=='segimiento':
					#===================================== ingreso al formulario=============================================================
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
					driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Despacho")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

					try:
						element2= WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
					except Exception as e:
						driver.back()
						self.ResGestion+="Marcacion seguimiento Fallida;"
						continue



					def cedAsesor():
						driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').clear()
						driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').send_keys(cedulaAsesor)
					cedAsesor()
					
					tokens=[]
					def CausaSolicitudDespacho():						
						driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Causa Solicitud"]').click()
						x=0
						while x<=5:
							try:
								Resultado=data[4].strip()
								if Resultado=="Apoyo información":									
									driver.find_element(by=By.XPATH, value='//div[@aria-label="Apoyo información"]').click()
								elif Resultado=="Completar visita sistema":									
									driver.find_element(by=By.XPATH, value='//div[@aria-label="Completar visita sistema"]').click()
								elif Resultado=="Llamada cliente":									
									driver.find_element(by=By.XPATH, value='//div[@aria-label="Llamada cliente"]').click()
								elif Resultado=="Seguimiento visita":									
									driver.find_element(by=By.XPATH, value='//div[@aria-label="Seguimiento visita"]').click()
								elif Resultado=="Validación razon" :									
									driver.find_element(by=By.XPATH, value='//div[@aria-label="Seguimiento visita"]').click()
								else:
									driver.find_element(by=By.XPATH, value='//div[@aria-label="Seguimiento visita"]').click()
								break
							except Exception as e:								
								time.sleep(1)
								x+=1
					CausaSolicitudDespacho()

					def NotasCausa():

						x=0						
						while x<=5:
							try:
								element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_DESP_Notas Causa"]')))																												
								driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Notas Causa"]').send_keys(f"\n{data[5]}")
								break
							except Exception as e:								
								x+=1

					NotasCausa()
									
					def Gestion():
						element=driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Detalle Gestion"]')
						actions = ActionChains(driver)
						actions.move_to_element(element)
						actions.perform()
						try:
							x=1
							while x<5:
								try:
									driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Detalle Gestion"]').click()
									break
								except Exception as e:
									x+=1
									time.sleep(1)
									Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
									print("Q",Nomb_error)
							
							gs=0
							while gs<5:
								try:
									Resultado=data[6].strip()
									if Resultado=="Comunicación con cliente":
										driver.find_element(by=By.XPATH, value='//div[@aria-label="Comunicación con cliente"]').click()
									elif Resultado=="Información ok":
										driver.find_element(by=By.XPATH, value='//div[@aria-label="Información ok"]').click()
									elif Resultado=="No Aplica Razon":
										driver.find_element(by=By.XPATH, value='//div[@aria-label="No Aplica Razon"]').click()
									elif Resultado=="Razon validada":
										driver.find_element(by=By.XPATH, value='//div[@aria-label="Razon validada"]').click()
									elif Resultado=="Seguimiento franja":
										driver.find_element(by=By.XPATH, value='//div[@aria-label="Seguimiento franja"]').click()									
									elif Resultado=="Visita completada" or Resultado=="Completar visita sistema":
										driver.find_element(by=By.XPATH, value='//div[@aria-label="Visita completada"]').click()
									else:
										driver.find_element(by=By.XPATH, value='//div[@aria-label="Seguimiento franja"]').click()
									
									break
								except :								
									time.sleep(1)
									gs+=1
						except Exception as e:
							Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
							print("y",Nomb_error)
					Gestion()

					def aliado():
						driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Aliado CGO"]').click()
						gs=0
						while gs<3:
							try:
								element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_DESP_Aliado CGO"]')))							
								driver.find_element(by=By.XPATH, value='//div[@aria-label="GNP"]').click()								
								break
							except Exception as e:
								time.sleep(1)
								gs+=1

					aliado()  # aliado

					def Notas():
						gs=0
						while gs<3:
							try:								
								driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Notas Gestion"]').send_keys(f"\n{data[7]}")								
								break
							except Exception as e:
								print(e)
								gs+=1
								time.sleep(0.5)
						
					Notas()

					salida=0
					while salida<=5:										
						if "Despacho" in driver.title:												
							try:
								driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()
							except Exception as e:
								time.sleep(1)
								salida+=1
						else:
							salida+=1



					self.Primera_ot=True
					self.ResGestion+="Marcacion seguimiento Ok;"
					#GestorSqlite().TipificarGestion("Confirmacion Ok",data[0],labor)
					time.sleep(0.5)
					#lista_data=[]						
										
				elif LaborDo=='confirmacion':
					#===================================== ingreso al formulario=============================================================
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
					driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Confirmación")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(2)
					try:
						element2= WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
					except Exception as e:
						'''try:
													driver.find_element(by=By.XPATH, value='//*[@action_link_label="select_provider"]').click()
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
							if driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').get_attribute("checked")==None:
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').click()
								#tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').get_attribute("checked"))  # AGENTE CONFIRMACION
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
					try:
						confirmacion_agente_ck()
					except:pass
									
					def R_confirmacion():
						driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Resultado"]').click()						
						gs=0
						while gs<2:
							try:																
								EstConf=data[8].strip().upper()
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
									driver.find_element(by=By.XPATH, value='//*[@title="REPROGRAMADA"]').click()
								else:
									driver.find_element(by=By.XPATH, value='//*[@title="CONFIRMADO"]').click()
								break
							except Exception as e:
								print(e)
								time.sleep(1)
								gs+=1
					try:
						R_confirmacion()
					except:
						pass


					def aliado():													
						gs=0
						while gs<2:
							try:
								driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_CONF_Aliado CGO"]').click()						
								element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_CONF_Aliado CGO"]')))
								if driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_CONF_Aliado CGO"]').get_attribute("value")!="GNP":
									driver.find_element(by=By.XPATH, value='//div[@data-value="GNP"]').click()        																	
								break
							except Exception as e:
								print(e)
								time.sleep(1)
								gs+=1
					try:
						aliado()  # aliado
					except:
						pass
					
					def cliente_gestion():
						gs=0
						while gs<2:
							try:
								element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="XA_Agent_Confirmation_Approver"]')))		
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Approver"]').clear()
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Approver"]').send_keys(data[9])								
								break
							except:
								gs+=1
								time.sleep(0.5)
					cliente_gestion()

					def usuario_CGO():
						gs=0
						while gs<2:
							try:
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_User"]').clear()
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_User"]').send_keys(data[10])
								
								break
							except:
								time.sleep(1)
								gs+=1
					usuario_CGO()

					def notas_confirmacion():
						gs=0
						while gs<2:
							try:								
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Notes"]').send_keys(f"\n{data[11]}")								
								break
							except:
								time.sleep(1)
								gs+=1

					notas_confirmacion()
					
					time.sleep(2)
					x=1
					while 'Confirmación' in driver.title and x<=5:
						try:
							element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
							driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()
							time.sleep(1)
						except Exception as e:
							print(driver.title)
							x+=1

					self.ResGestion+='Marcacion confirmacion Ok;'
					WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
									
				elif LaborDo=='demora':
					#===================================== ingreso al formulario=============================================================
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
					driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Despacho")]').click()
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))


					time.sleep(0.5)
					html=driver.find_element(by=By.XPATH, value='//*[@id="content" and @class="content"]').text			
					if "CancelarOK" not in html:
						driver.back()
						time.sleep(2)
						driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
						self.ResGestion+='Marcacion demora Fallida;'
						compuerta=False
						continue

					def cedAsesor():
						driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').clear()
						driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').send_keys(cedulaAsesor)
					cedAsesor()

					tokens=[]
					def ReporteDemora_ck():
						if driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Reporte Demora"]').get_attribute("checked")==None:
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Reporte Demora"]').click()
						else:
							pass
						tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Reporte Demora"]').get_attribute("checked"))  # AGENTE CONFIRMACION
					
					try:
						ReporteDemora_ck()
					except Exception as e:
						print(e)

					def AliadoCGODespacho():
						#Bot.ClicJs('document.querySelector("#id_index_241 > button").click()')
						driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Aliado CGO"]').click()
						driver.find_element(by=By.XPATH, value='//div[@data-value="GNP"]').click()

						tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Aliado CGO"]').get_attribute("value")) # CONFIRMACION AGENTE

					AliadoCGODespacho()
								
					def HoraReporte():
						gs=0
						while gs<5:
							try:								
								if driver.find_element(by=By.XPATH, value='//*[@aria-label="Hora Reporte"]').get_attribute("value")=="":
									driver.find_element(by=By.XPATH, value='//*[@aria-label="Hora Reporte"]').clear()
									driver.find_element(by=By.XPATH, value='//*[@aria-label="Hora Reporte"]').send_keys(timer()[1])
								else:
									pass								
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
								if driver.find_element(by=By.XPATH, value='//*[@aria-label="Persona Reporte"]').get_attribute("value")=="":
									driver.find_element(by=By.XPATH, value='//*[@aria-label="Persona Reporte"]').clear()
									driver.find_element(by=By.XPATH, value='//*[@aria-label="Persona Reporte"]').send_keys("Gestion IVR")     	
								else:
									pass								
								break
							except:
								time.sleep(1)
								gs+=1

					PersonaReporte()  
					
					def HoraMaxEspera():
						try:
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Hora maxima reporte"]').click()									
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Hora maxima reporte"]').clear()													
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Hora maxima reporte"]').send_keys("01")														
							driver.find_element(by=By.XPATH, value='//*[@role="option" and @data-value="01"]').click()
						except Exception as e:
							Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
							print(Nomb_error)
						time.sleep(0.5)
					HoraMaxEspera()

					def MinutoMaxEspera():
						try:
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Minuto max esperra"]').click()
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Minuto max esperra"]').clear()
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Minuto max esperra"]').send_keys('00')
							driver.find_element(by=By.XPATH, value='//*[@role="option" and @data-value="00"]').click()
							#tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Minuto max esperra"]').get_attribute("value"))  # usuario CGO que confirma
						except Exception as e:
							Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
							print(Nomb_error)
					#MinutoMaxEspera()

					def NotasHoraMaxEspera():
						gs=0
						while gs<5:
							try:
								driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Notas Hora Max de Espera"]').send_keys("Confirmación IVR")
								#tokens.append(driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Notas Hora Max de Espera"]').get_attribute("value"))  # notas de confirmacion
								break
							except:
								time.sleep(1)
								gs+=1

					NotasHoraMaxEspera()


					def ListaReporteDemora():
						driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Lista Reporte Demora"]').click()
						x=0
						while x<=5:
							try:
								EstGesDemo=data[12].lower().strip()
								if EstGesDemo.lower()=="acepta demora":
									driver.find_element(by=By.XPATH, value='//*[@aria-label="Acepta Demora"]').click()
								elif EstGesDemo.lower()=="no acepta demora":
									driver.find_element(by=By.XPATH, value='//*[@aria-label="No Acepta Demora"]').click()
								elif EstGesDemo.lower()=="no contacto":
									driver.find_element(by=By.XPATH, value='//*[@aria-label="No contacto"]').click()						
								else:
									driver.find_element(by=By.XPATH, value='//*[@aria-label="Acepta Demora"]').click()
								break
							except Exception as e:
								print(e)
								x+=1


					ListaReporteDemora()
					self.ResGestion+='Marcacion demora Ok;'
					time.sleep(1)
					driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()	
					WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(0.5)
				
							
			time.sleep(1)		
		
			try:
				element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]')))
				driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
			except:# Exception as e:
				pass
				#Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				#print(Nomb_error)

			
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
		    time.sleep(4)
		    driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
		    time.sleep(1)
		    driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
		    time.sleep(5)
		    ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM", [data[0], "Error de marcacion"]))            
		except:pass		
		driver.quit()