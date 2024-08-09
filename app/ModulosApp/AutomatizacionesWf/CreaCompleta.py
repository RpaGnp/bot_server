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


def selector_Completacion(self,idBot,Idactividad,tipo):
		#while 1:
		driver=self.driver		
		try:
			ConectorDbMysql().RepActividad(idBot)
			#iniciar_ruta(self,driver)
			time.sleep(2)
			try:
				element = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toaGantt-tb toaGantt-tb-name"]')))
			except:
				pass
			lista_refresh=[]
			#ContadorReinicio=0
			# ==========verificar si hay ots pendientes==========
			started = driver.find_elements(by=By.XPATH, value='//*[@data-activity-status="started"]')
			l=driver.find_elements(by=By.XPATH, value='//*[@data-activity-status="pending"]')				

			diccionario={}			
			for i in reversed(l):			
				x=i.get_attribute("aid")
				y=i.get_attribute("aria-label")				
				diccionario.update({str(x):str(y)})

			
			time.sleep(2)
			vuelta=0
			compuerta=True
			ContadorRF=0
			for i,j in diccionario.items():								            				
				numero_ot=i
				tipo_ot=j
				print("*"*40,numero_ot," ",tipo_ot,"*"*40)				
				FechaHora = datetime.now()											
				print(FechaHora.strftime('%H:%M:%S'))
				del FechaHora

				ContadorRF+=1
				print(ContadorRF)
				if ContadorRF==50:				
					ContadorRF=0
					driver.refresh()
					time.sleep(10)

				try:					
					driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
				except:pass


				ConectorDbMysql().RepActividad(idBot)
				#FUNCION PARA VER PAUSA O ELIMINACION DEL BOT
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
								driver.quit()
								return

					elif Dato[0] == "Eliminar":
						ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))												
						driver.quit()
						return
				else:pass
				
				element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))
				lupa=driver.find_element(by=By.XPATH, value='//*[@type="search"]')				
				time.sleep(0.5)
				if lupa.is_displayed()==False:					
					driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()							
				else:pass

				time.sleep(0.5)
							
				driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
				ramel=False
				x=0
				while x<3:
					try:
						driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(numero_ot)
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)						
						time.sleep(1)
						break
					except:						
						time.sleep(3)
						x+=1

				#evaluar color y estado de al orden
				if tipo_ot=="pending regular Backoffice activity":
					element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="found-item-activity"]')))
					
					time.sleep(0.5)
					gs=0
					while gs<10:
						try	:				
							_estado=driver.find_elements(by=By.XPATH, value="//*[@aid="+str(numero_ot)+"]")							
							estatus_orden=_estado[1].get_attribute("style")														
							break
						except:
							time.sleep(0.5)
							
							gs+=1
					#x=driver.find_element(by=By.XPATH, value="/html/body/div[15]/div[1]/div[1]/div[2]/div[1]/table/tr/td[1]/div")					
					if estatus_orden=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);":						
						for i in driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]'):
							try:								
								if 'Backoffice' in i.text:
									i.click()
								else:
									print("tipo de orden no admitida: ",i.text )
							except Exception as e:
								print(e)
						driver.implicitly_wait(0)
						WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

						#driver.find_element(by=By.XPATH, value='//*[@class="toa-search-identifier" and contains(text(),"Backoffice")]').click()
						compuerta=True
					else:
						compuerta=False												
						continue
					# dentro de la orden para iniciarla
					element2= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Información Actividad"]')))
					time.sleep(0.5)
					driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Iniciar")]').click()

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(0.5)
					element2= WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and @class="button submit" and contains(text(),"OK")]')))


					driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
					try:						
						if driver.find_element(by=By.XPATH, value='//*[@class="popup-window-slot"]//div[@class="redwood-dialog__content"]').is_displayed():
							driver.find_element(by=By.XPATH, value='//*[@class="button submit" and contains(text(),"Continuar")]').click()

					except:
						pass

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					#salida
					
					
					try:
						driver.find_element(by=By.XPATH, value='//span[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
						break
					except:
						time.sleep(1)
						x+=1
						
					print("completar activity")
					FechaHora = datetime.now()											
					print(FechaHora.strftime('%H:%M:%S'))
					del FechaHora
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					#ENTRARA A LA ORDEN YA INICIADA
					gs=0
					while gs<5:
						try:
							driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()
							driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
							driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(numero_ot)
							driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)
							break
						except Exception as e:
							Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e							
							time.sleep(1)
							gs+=1
					
					print("selecionar orden iniciada")
					for i in driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]'):						
						if 'Backoffice' in i.text:
							i.click()
						else:
							print("tipo de orden no admitida: ",i.text )
					
					print("salida orden iniciada")

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

							
					time.sleep(0.5)
					l=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
					for i in l:
						try:							
							if 'Backoffice' in i.text:
								i.click()
							else:
								print("tipo de orden no admitida: ",i.text )
						except Exception as e:
							print(e)


					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					
					print(driver.title)
					if driver.title!="Detalles de actividad - Oracle Field Service":
						driver.refresh()
						time.sleep(7)
						driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(numero_ot)
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)
						time.sleep(1)
						l=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
						print(l)
						for i in l:							
							if 'Backoffice' in i.text:
								i.click()
							else:
								print("tipo de orden no admitida: ",i.text )
						del l
					else:
						pass
					#driver.find_element(by=By.XPATH, value='//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')


					c=0
					while c<3:
						try:
							driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Completar")]').click()
							break
						except Exception as e:
							time.sleep(1)
							c+=1
						#######################333

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

					

					x=0
					while x<3:
						try:
							driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
							break
						except:
							x+=1
					try:
						if driver.find_element(by=By.XPATH, value='//*[@class="redwood-dialog__content"]').is_displayed():
							driver.find_element(by=By.XPATH, value='//*[@class="button submit" and contains(text(),"Continuar")]').click()

					except:
						pass

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					
					#while driver.title!='Consola de despacho - Oracle Field Service':
					#	time.sleep(1)					


				elif tipo_ot=="started regular Backoffice activity":					
					time.sleep(0.5)									
					element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="found-item-activity"]')))
					time.sleep(0.5)
					gs=0
					while gs<10:
						try	:				
							_estado=driver.find_elements(by=By.XPATH, value="//*[@aid="+str(numero_ot)+"]")
							estatus_orden=_estado[1].get_attribute("style")
							break
						except:
							time.sleep(0.5)
							print("error localizando  ot!!")
							gs+=1
					#x=driver.find_element(by=By.XPATH, value="/html/body/div[15]/div[1]/div[1]/div[2]/div[1]/table/tr/td[1]/div")					
					if estatus_orden=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);" or estatus_orden=="background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);":
						l=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
						for i in l:
							try:									
								if 'Backoffice' in i.text:
									i.click()
								else:
									print("tipo de orden no admitida: ",i.text )
							except Exception as e:
								print(e)
						driver.implicitly_wait(0)
						WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

						#driver.find_element(by=By.XPATH, value='//*[@class="toa-search-identifier" and contains(text(),"Backoffice")]').click()
						compuerta=True
					else:
						compuerta=False												
						continue
					
					element2= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Información Actividad"]')))

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

					c=0
					while c<5:
						try:
							driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Completar")]').click()
							break
						except:
							time.sleep(1)
							c+=1
					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
					try:
						if driver.find_element(by=By.XPATH, value='//*[@class="redwood-dialog__content"]').is_displayed():
							driver.find_element(by=By.XPATH, value='//*[@class="button submit" and contains(text(),"Continuar")]').click()

					except:
						pass
					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

				else:								
					pass
				

				#while driver.title!="Consola de despacho - Oracle Field Service":
				#	time.sleep(1)					
				#	driver.back()
				print("Orden Completada")
				FechaHora = datetime.now()											
				print(FechaHora.strftime('%H:%M:%S'))
				del FechaHora
					
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTGESCOM",[Idactividad,numero_ot,'Ot Completada']))

				x=0
				while x<7:
					try:
						driver.find_element(by=By.XPATH, value='//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')
						break
					except:
						time.sleep(1)
						x+=1

				'''ContadorReinicio+=1
																if ContadorReinicio==100:
																	driver.refresh()
																	time.sleep(3)
																	driver.quit()
																	return'''

			if tipo ==3:
				return
			else:
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))			
				driver.quit()
			
		except Exception as e:
			driver.find_element(by=By.XPATH, value='//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')
			return
			
			