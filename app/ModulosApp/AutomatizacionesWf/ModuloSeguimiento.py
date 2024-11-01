#LIBRERIAS PARA CHROMEDRIVER***********************
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import sys
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *


def FunGuardar(self,ArrayGestion):	
	#print(sql)
	sql=("SPR_UPD_ESTACTM",ArrayGestion)
	ConectorDbMysql().FuncInsInfoOne(sql)	
	#print("Actualizado")

def selector_Seguimiento(self,idBot,Idactividad):
		#while 1:
		try:			
			array_datos=ConectorDbMysql().FuncGetSpr(2,"spr_get_ordptemarc",[Idactividad])					
			compuerta=False
			Primera_ot=True
			lista_ejecucion=[]
			self.lista_contador_eventos=[]	
			driver=self.driver

			for i,data in enumerate(array_datos):								
				IdRow=data[0]
				Orden=data[1]
				print(data)
				try:
					# print(' spr_get_idaseasi : ',[data[2]])
					cedulaAsesor = ConectorDbMysql().FunGetProcedure(["spr_get_idaseasi",[data[2]]])[0]
					print(cedulaAsesor)
				except Exception as e:
					print(e)
					FunGuardar(self,[data[0],"Tecnico sin asignacion de asesor"])
					continue

				ConectorDbMysql().RepActividad(idBot)
				self.lista_contador_eventos.append(1)
				

				# funcion de salida, pausa del bot
				Dato=ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES",[idBot]))
				#print(Dato[0])
				if Dato[0]!=None:					
					if Dato[0]=="Eliminar":						
						ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT",[idBot,Idactividad,'Detenido por usuario']))
						driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
						time.sleep(1)						
						driver.quit()
						return
				else:
					pass
				try:
					element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))			
				except:
					driver.back()

				#driver.find_element(by=By.XPATH, value='//*[@id="action-global-search-icon"]').click()
				time.sleep(0.5)
				# refresh wf
				lista_ejecucion.append(1)
				if len(lista_ejecucion)==30:
					driver.refresh()
					time.sleep(10)
					lista_ejecucion=[]

				
				element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))				
				lupa=driver.find_element(by=By.XPATH, value='//div[@id="search-bar-container"]')						
				if lupa.is_displayed()==False:
					driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()				
				else:
					pass					
				
				time.sleep(0.50)
				driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
				driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
				driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Orden)
				driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)
				
				try:
					element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
				except Exception as e:
					Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
					#print(Nomb_error)					
					FunGuardar(self, [IdRow,'Ot no apta consulta,'])
					compuerta = False
					continue

				if driver.find_element(by=By.XPATH, value='//*[@class="toa-search-empty"]').text != "":
					compuerta=False
					continue
				else:
					pass
				
				
				self._fecha_hoy=fecha_actual(self)
				#print("*",_fecha_hoy)
				time.sleep(1)
				element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
				_lista_lls=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
				#print("="*40,len(_lista_lls),"="*40)
				if len(_lista_lls)==0:					
					FunGuardar(self, [IdRow,'Ot no apta para marcar'])
					compuerta = False
					continue

				for i in range(len(_lista_lls)):
					gs=0
					while gs<5:
						try:
							#print(i)
							#fecha_Ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].text
							fecha_Ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-date"]')[i].text
							#print("fecha lls: ",fecha_Ot)
							time.sleep(0.5)
							#x=driver.find_elements(by=By.XPATH, value='//div[starts-with(@style,"background-color: #")]')[i].get_attribute("style")
							x=driver.find_elements(by=By.XPATH, value='//*[@class="activity-icon icon"]')[i].get_attribute("style")
							#print(x)
							tipo_ot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].text
							#print(tipo_ot)
							
							break
						except:
							time.sleep(1)
							gs+=1
					#amarillo gris claro naranja verde claro
					if x=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);"\
					 or x=="background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);"\
					  or x=="background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);"\
							or x=='background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);'\
							 or x=='background-color: rgb(30, 133, 37); border: 1px solid rgb(24, 106, 29);':

						#print(fecha_Ot,"=",_fecha_hoy[0])
						if fecha_Ot==self._fecha_hoy[0] or fecha_Ot==self._fecha_hoy[1] or fecha_Ot==self._fecha_hoy[2] or fecha_Ot=="":
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
								else:								
									compuerta=False
							else:								
								compuerta=False
						else:							
							compuerta=False				
							continue
					else:						
						compuerta=False				
						continue

				if compuerta==False:					
					FunGuardar(self,[IdRow,'Ot no apta consulta'])
					compuerta=False
					continue
				else:
					pass

				if Primera_ot:
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="column-container"]')))

				else:
					pass
				
				WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@class="button inline" and contains(text(),"Backoffice")]')))
				driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]').click()
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
				#===================================== ingreso al formulario=============================================================
				element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
				driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Despacho")]').click()
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))


				try:
					element2= WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
				except Exception as e:
					try:
						driver.find_element(by=By.XPATH, value='//*[@action_link_label="select_provider"]').click()
					except:
						salida_noApt(driver)
					Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
					FunGuardar(self, [IdRow,'Ot no apta consulta,'])
					compuerta=False
					continue

				#print("="*30,"formulario activo","="*30)####
				def cedAsesor():
					driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').clear()
					driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').send_keys(cedulaAsesor)
				cedAsesor()
				
				
				def CausaSolicitudDespacho():
					driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Causa Solicitud"]').click()
					while 1:
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
							print(e)
							time.sleep(1)
				CausaSolicitudDespacho()

				def NotasCausa():					
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_DESP_Notas Causa"]')))					
					driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Notas Causa"]').send_keys(f"\n{data[5]}")					
							
						

				NotasCausa()
								
				def Gestion():
					for i in range(3):
						try:
						    element=driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Detalle Gestion"]')
						    actions = ActionChains(driver)
						    actions.move_to_element(element)
						    actions.perform()                        
						    break
						except:pass
					
					gs=0
					while gs<5:
						try:		
							driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Detalle Gestion"]').click()					
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
						except Exception as e:
							print(e)
							time.sleep(1)
							gs+=1
				Gestion()


				def aliado():
					driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Aliado CGO"]').click()
					gs=0
					while gs<3:
						try:							
							driver.find_element(by=By.XPATH, value='//div[@aria-label="GNP"]').click()							
							break
						except Exception as e:
							time.sleep(1)
							gs+=1

				aliado()  # aliado

				try:                    
				    driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
				except:pass
				
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

				#WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class=""loading-animated-icon big jbf-init-loading-indicator""]')))
				for x in range(1,3):
					try:
						driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()
						break
					except:
						pass

				WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
				
				
				
					
				time.sleep(1)
				x=0
				while x<2:
					try:
						driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
						break
					except:
						x+=1
						driver.back()
				
				
				Primera_ot=True
				
				sql=("SPR_UPD_ESTACTM",[IdRow,'Ot marcada con exito'])
				ConectorDbMysql().FuncInsInfoOne(sql)
				#ConectorDbMysql().FuncInsInfoOne("SPR_UPD_ESTACTM",[IdRow,'Ot marcada con exito'])						
				time.sleep(0.5)

			#salida_adelantos(driver)
			driver.refresh()
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
			#messagebox.showinfo(message="Ots Gstion seguimiento gestionadas con exito!", title="Bot Gestion Wf")
			#break
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