import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from ..interaccionChrome import Botinteraccion
from ..ModelDataBase import ConectorDbMysql
from ..GestorError import ErrorHandle
from funciones_varias import *
from reloj_casio import *

def FunGuardar(self,ArrayGestion):
	sql=("SPR_UPD_ESTACTM",ArrayGestion)
	ConectorDbMysql().FuncInsInfoOne(sql)


def selector_Demora(self,idBot,Idactividad):
	#while 1:
	driver=self.driver
	Bot=Botinteraccion(driver)
	try:
		array_datos=ConectorDbMysql().FuncGetSpr(2,"spr_get_ordptemarc",[Idactividad])		
		lista_refresh=[]
		for i,data in enumerate(array_datos):							         									
			print(data)
			try:
				cedulaAsesor = ConectorDbMysql().FunGetProcedure(["spr_get_idaseasi",[data[2]]])[0]				
			except Exception as e:
				ErrorHandle(e).ShowError()
				FunGuardar(self,[data[0],"Tecnico sin asignacion de asesor"])
				continue
			
			lista_refresh.append(data[1])
			if len(lista_refresh)==30:
				driver.refresh()
				lista_refresh=[]

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

			busqueda_global = driver.find_element(by=By.CSS_SELECTOR, value='.jbf-icon-button.action-global-search-icon[role="button"]')
			
			try:
				driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			except Exception as e:
				ErrorHandle(e).ShowError()

			try:
				# Buscar el botón de búsqueda global por su clase y atributos
				busqueda_global = driver.find_element(by=By.CSS_SELECTOR, value='.jbf-icon-button.action-global-search-icon[role="button"]')
				busqueda_global.click()
			except:
				pass

			time.sleep(0.50)
			driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(data[1])
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)

			driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			
			try:
				element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			except Exception as e:
				ErrorHandle(e).ShowError()
				FunGuardar(self,[data[0],'Marcacion Demora Fallida'])				
				compuerta = False
				continue

			if driver.find_element(by=By.XPATH, value='//*[@class="toa-search-empty"]').text != "":
				compuerta=False
				continue
			else:
				pass
			
			_lista_lls=""
			_fecha_hoy=fecha_actual(self)
			#print("*",_fecha_hoy)
			
			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			_lista_lls=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
			
			if len(_lista_lls)==0:				
				tokens = []				
				FunGuardar(self,[data[0],'Marcacion Demora Fallida'])
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
						break
					except:
						time.sleep(1)
						gs+=1
				#amarillo, verde claro, naranjado, otro verde,
				if x=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);"\
				 or x=="background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);"\
						or x=='background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);':
					#print(fecha_Ot,"=",_fecha_hoy[0])
					if fecha_Ot==_fecha_hoy[0] or fecha_Ot==_fecha_hoy[1] or fecha_Ot==_fecha_hoy[2]or fecha_Ot=="":
						if "Backlog" not in  tipo_ot:
							if "Supervision"  not in  tipo_ot:
								if "Backoffice" not in  tipo_ot:												 
									driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].click()
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
				tokens=[]
				#tokens.append(["Consultado","N/A","N/A","N/A","N/A","N/A","N/A","N/A",timer()[0],timer()[1],"OT NO APTA PARA CONSULTA",data[0]])
				#funcion_guardado(self,tokens)
				FunGuardar(self,[data[0],'Marcacion Demora Fallida'])
				compuerta=False
				continue
			else:
				pass

			
			
			driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			#===================================== ingreso al formulario=============================================================
			element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
			driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Despacho")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

			
			#print("ingreso al formulario")
			try:                    
			    driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			except:pass
			
			try:
				element2= WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
			except Exception as e:
				salida_noApt(driver)
				ErrorHandle(e).ShowError()				
				FunGuardar(self,[data[0],'Marcacion Demora Fallida'])
				compuerta=False
				continue

			def cedAsesor():
				try:
					driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').clear()
					driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').send_keys(cedulaAsesor)
				except Exception as e:
					ErrorHandle(e).ShowError()

			cedAsesor()		

			
			def ReporteDemora_ck():
				if driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Reporte Demora"]').get_attribute("checked")==None:
					driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Reporte Demora"]').click()
				else:
					pass				
			try:
				ReporteDemora_ck()
			except Exception as e:
				print(e)

			def AliadoCGODespacho():
				x=0
				while x<5:
					try:
						driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Aliado CGO"]').click()
						time.sleep(0.5)
						driver.find_element(by=By.XPATH, value='//*[@data-value="GNP"]').click()
						break
					except Exception as e:
						ErrorHandle(e).ShowError()
						x+=1				

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

			#PersonaReporte()  
			
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
					driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Minuto max espera"]').click()
					driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Minuto max espera"]').clear()
					driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Minuto max espera"]').send_keys('00')
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

			try:                    
			    driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			except:pass
			
			def ListaReporteDemora():
				Resultado= data[4].lower().strip()				
				x=0
				while x<5:
					try:						
						driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Lista Reporte Demora"]').click()
						if Resultado=="acepta demora":
							driver.find_element(by=By.XPATH, value='//*[@aria-label="Acepta Demora"]').click()
						elif Resultado=="no acepta demora":
							driver.find_element(by=By.XPATH, value='//*[@aria-label="No Acepta Demora"]').click()
						elif Resultado=="no contacto":
							driver.find_element(by=By.XPATH, value='//*[@aria-label="No contacto"]').click()						
						else:
							driver.find_element(by=By.XPATH, value='//*[@aria-label="Acepta Demora"]').click()
						break
					except Exception as e:
						print(e)
						x+=1

			ListaReporteDemora()
			time.sleep(1)
			
			driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()
			try:
				WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class=""loading-animated-icon big jbf-init-loading-indicator""]')))
			except Exception as e:
				pass
			
			
			try:
				error1=driver.find_element(by=By.XPATH, value='//*[contains(text(),"No se pudo procesar la solicitud. Siga trabajando o póngase en contacto con el administrador para obtener ayuda.")]')
				if error1.is_displayed()==True:
					driver.find_element(by=By.XPATH, value='//*[@id="notification-clear"]').click()
					driver.find_elements(by=By.XPATH, value='//*[@class="button dismiss"]')[1].click()
			except:
				pass

			try:
				time.sleep(0.5)
				error2=driver.find_element(by=By.XPATH, value='//*[contains(text(),"Los cambios no se han enviado. ¿Desea guardar un borrador de las actualizaciones?")]')
				if error2.is_displayed()==True:
					driver.find_element(by=By.XPATH, value='//*[@class="button submit" and contains(text(),"Sí")]').click()
			except:
				pass
				
			time.sleep(1)
			
			try:
				driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()				
			except:				
				driver.back()


			Primera_ot=True
			
			sql = ("SPR_UPD_ESTACTM", [data[0], 'Demora marcada con exito'])			
			ConectorDbMysql().FuncInsInfoOne(sql)
			# si aparece la ventana de confirmacion darle continuar********************************************
			time.sleep(0.5)
			#salida_adelantos(driver)
		
		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))
		try:			
		    driver.refresh()
		    time.sleep(4)
		    driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
		    time.sleep(1)
		    driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
		    time.sleep(5)		    
		except:pass
		driver.quit()

	except Exception as e:
		ErrorHandle(e).ShowError()	
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
		except:	pass
		
