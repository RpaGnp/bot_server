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


def iniciar_ruta(self,driver):		
	print("activando ruta....")	
	element2= WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toaGantt-tb toaGantt-tb-name"]')))
	driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Acciones")]').click()
	time.sleep(1)
	if "Activar ruta" in driver.find_element_by_xpath('/html/body/div[25]').text:
		driver.find_element_by_xpath('//*[@aria-label="Activar ruta"]').click()
		time.sleep(1)
		driver.find_element_by_xpath('//*[@class="button submit" and @type="submit" and contains(text(),"OK")]').click()
		
	else:
		print("ruta activa")

	webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def configurar_busqueda(self,driver):
	print("buscando...")
	driver.find_element_by_xpath('//*[@class="toa-header-search"]').click()
	wait= WebDriverWait(driver, 15)
	element2= wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@name="search_value"]')))
	driver.execute_script('document.querySelector("body > div.ui-tip.ui-widget.ui-corner-all.ui-widget-content.toa-search-activity > div.ui-tip-content > div.toa-search > div.toa-search-form > table > tbody > tr > td.toa-search-form-last-column > div > div").click()')
	wait= WebDriverWait(driver, 15)
	element2= wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Seleccionar y arrastrar categorias para ordenar los resultados de la búsqueda por prioridad")]')))
	for i in range(1,36):
		x=driver.find_element_by_xpath('/html/body/div[15]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li['+str(i)+']/div/div[2]/input')
		y=x.get_property('checked')
		#print("*"*40, y ,"*"*40)
		if i==24 and y==False:
			driver.find_element_by_xpath('/html/body/div[15]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li['+str(i)+']/div/div[2]/input').click()
		elif i!=24 and y==True:
			driver.find_element_by_xpath('/html/body/div[15]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li['+str(i)+']/div/div[2]/input').click()
	'''for i in driver.find_elements_by_xpath('//*[@class="toa-search-preferences-checkbox"]'):
		y=i.get_attribute('checked')
		if y!="checked":
			driver.find_element_by_xpath('//*[@type="checkbox"]').click()
		else:
			print("estado check ok!")'''
		
	driver.find_element_by_xpath('/html/body/div[15]/div[1]/div[2]/div[1]/button').click()
	driver.find_element_by_xpath('//*[@class="toa-header-search"]').click()
	try:
		element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="Buscar"]')))
	except:
		pass

def cambiar_vista(self,driver):
	driver.find_element_by_xpath('//*[@name="popup" and @data-ctrl-id="88"]').click()
	en=driver.find_element_by_xpath('//*[@type="range"]')
	move = ActionChains(driver)
	move.click_and_hold(en).move_by_offset(12, 0).release().perform()
	driver.find_element_by_xpath('//*[@value="apply"]').click()

def selector_Completacion(self,idBot,Idactividad):
		#while 1:
		driver=self.driver
		Bot=Botinteraccion(driver)
		try:
			ConectorDbMysql().RepActividad(idBot)
			iniciar_ruta(self,driver)
			time.sleep(2)
			try:
				element = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toaGantt-tb toaGantt-tb-name"]')))
			except:
				pass
			lista_refresh=[]
			
			# ==========verificar si hay ots pendientes==========
			#verificar ordenes pendientes
			l=[]
			started = driver.find_elements_by_xpath('//*[@data-activity-status="started"]')
			if len(started)!=0:
				l.append(started[0])
			else:
				pass

			sql="""SELECT  ACP_ORDEN
				from tbl_hactcompletarbot
				where ACP_NIDAC='"""+str(Idactividad)+"""' and ACP_CESTGES='Pendiente'
				"""							
			array_datos=list(ConectorDbMysql().FuncGetInfo(0,sql))
			if len(array_datos)==0:
				l=driver.find_elements_by_xpath('//*[@data-activity-status="pending"]')					
				
				ArrayOtsCom=[]				
				for i,dato in enumerate(array_datos):
					ArrayOtsCom.append(dato[0])				
				del array_datos

				diccionario={}			
				for i in reversed(l):			
					x=i.get_attribute("aid")
					y=i.get_attribute("aria-label")				
					diccionario.update({str(x):str(y)})
					if x not in ArrayOtsCom:
						ConectorDbMysql().FuncInsInfoOne(("SPR_INS_ACTCOMP",[Idactividad,x]))	
					else:
						pass
			else:
				pass
				
			diccionario={}
			vuelta=0
			

			
			
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
				lupa=driver.find_element_by_xpath('//*[@type="search"]')				
				time.sleep(0.5)
				if lupa.is_displayed()==False:					
					driver.find_element_by_xpath('//*[@aria-label="GlobalSearch"]').click()							
				else:pass

				time.sleep(0.5)
							
				driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
				ramel=False
				x=0
				while x<3:
					try:
						driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
						driver.find_element_by_xpath('//*[@class="search-bar-input"]').clear()
						driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(numero_ot)
						driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(Keys.ENTER)						
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
							_estado=driver.find_elements_by_xpath("//*[@aid="+str(numero_ot)+"]")							
							estatus_orden=_estado[1].get_attribute("style")														
							break
						except:
							time.sleep(0.5)
							
							gs+=1
					#x=driver.find_element_by_xpath("/html/body/div[15]/div[1]/div[1]/div[2]/div[1]/table/tr/td[1]/div")					
					if estatus_orden=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);":						
						for i in driver.find_elements_by_xpath('//*[@class="found-item-activity"]'):
							try:								
								if 'Backoffice' in i.text:
									i.click()
								else:
									print("tipo de orden no admitida: ",i.text )
							except Exception as e:
								print(e)
						driver.implicitly_wait(0)
						WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

						#driver.find_element_by_xpath('//*[@class="toa-search-identifier" and contains(text(),"Backoffice")]').click()
						compuerta=True
					else:
						compuerta=False												
						continue
					# dentro de la orden para iniciarla
					element2= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Información Actividad"]')))
					time.sleep(0.5)
					driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Iniciar")]').click()

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					time.sleep(0.5)
					element2= WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and @class="button submit" and contains(text(),"OK")]')))


					driver.find_element_by_xpath('//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
					try:						
						if driver.find_element_by_xpath('//*[@class="popup-window-slot"]//div[@class="redwood-dialog__content"]').is_displayed():
							driver.find_element_by_xpath('//*[@class="button submit" and contains(text(),"Continuar")]').click()

					except:
						pass

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					#salida
					
					x=0
					while x<5:
						try:
							driver.find_element_by_xpath('//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')
							break
						except:
							time.sleep(2)
							x+=1
						
					print("completar activity")
					FechaHora = datetime.now()											
					print(FechaHora.strftime('%H:%M:%S'))
					del FechaHora

					#ENTRARA A LA ORDEN YA INICIADA
					gs=0
					while gs<5:
						try:
							driver.find_element_by_xpath('//*[@aria-label="GlobalSearch"]').click()
							driver.find_element_by_xpath('//*[@class="search-bar-input"]').clear()
							driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(numero_ot)
							driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(Keys.ENTER)
							break
						except Exception as e:
							Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e							
							time.sleep(1)
							gs+=1
					
					print("selecionar orden iniciada")
					for i in driver.find_elements_by_xpath('//*[@class="found-item-activity"]'):						
						if 'Backoffice' in i.text:
							i.click()
						else:
							print("tipo de orden no admitida: ",i.text )
					
					print("salida orden iniciada")

					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

							
					time.sleep(0.5)
					l=driver.find_elements_by_xpath('//*[@class="found-item-activity"]')
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
						driver.find_element_by_xpath('//*[@aria-label="GlobalSearch"]').click()
						driver.find_element_by_xpath('//*[@class="search-bar-input"]').clear()
						driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(numero_ot)
						driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(Keys.ENTER)
						time.sleep(1)
						l=driver.find_elements_by_xpath('//*[@class="found-item-activity"]')
						print(l)
						for i in l:							
							if 'Backoffice' in i.text:
								i.click()
							else:
								print("tipo de orden no admitida: ",i.text )
						del l
					else:
						pass
					#driver.find_element_by_xpath('//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')


					c=0
					while c<3:
						try:
							driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Completar")]').click()
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
							driver.find_element_by_xpath('//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
							break
						except:
							x+=1
					try:
						if driver.find_element_by_xpath('//*[@class="redwood-dialog__content"]').is_displayed():
							driver.find_element_by_xpath('//*[@class="button submit" and contains(text(),"Continuar")]').click()

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
							_estado=driver.find_elements_by_xpath("//*[@aid="+str(numero_ot)+"]")
							estatus_orden=_estado[1].get_attribute("style")
							break
						except:
							time.sleep(0.5)
							print("error localizando  ot!!")
							gs+=1
					#x=driver.find_element_by_xpath("/html/body/div[15]/div[1]/div[1]/div[2]/div[1]/table/tr/td[1]/div")					
					if estatus_orden=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);" or estatus_orden=="background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);":
						l=driver.find_elements_by_xpath('//*[@class="found-item-activity"]')
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

						#driver.find_element_by_xpath('//*[@class="toa-search-identifier" and contains(text(),"Backoffice")]').click()
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
							driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Completar")]').click()
							break
						except:
							time.sleep(1)
							c+=1
					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
					driver.find_element_by_xpath('//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
					try:
						if driver.find_element_by_xpath('//*[@class="redwood-dialog__content"]').is_displayed():
							driver.find_element_by_xpath('//*[@class="button submit" and contains(text(),"Continuar")]').click()

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
						driver.find_element_by_xpath('//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')
						break
					except:
						time.sleep(1)
						x+=1

			ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))			
			driver.quit()
			
		except Exception as e:
			Nomb_error='Error on line modulo completar {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)			
			
			driver.refresh()
			time.sleep(3)
			
			driver.quit()
			