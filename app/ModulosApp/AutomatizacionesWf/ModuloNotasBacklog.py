
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


from reloj_casio import timer

import time
import csv
import sys
import os
import secrets
from datetime import date
from datetime import datetime
from datetime import time as tmr
from datetime import timedelta
import json

from ..ModelDataBase import ConectorDbMysql
from ..ModeloCarpetas import CreadorCarpetas
from ..interaccionChrome import BotGestionWF
from ..AutomatizacionRR.ConsultorMongo import Handledbmongo

from platform import platform

class SelectorNotas:
	def __init__(self,driver,idbot,idlabor,ciudad):
		self.driver = driver
		self.idbot=idbot
		self.idlabor=idlabor
		self.ciudad=ciudad
		if 'Windows' in platform():
			self.PathImagenes = CreadorCarpetas("C://DBGestionBot//BotcndRazones/")
		else:
			self.PathImagenes = CreadorCarpetas("/DBGestionBot/BotcndRazones/")

	def main(self):
		BotWfm=BotGestionWF(self.driver)
		contadorReinicio=0		
		LimiteContador=10
		limite_hora = tmr(22, 0, 0)
		driver=self.driver

		try:
			while datetime.now().time() < limite_hora:
				# reporta actividad del bot
				ConectorDbMysql().RepActividad(self.idbot)
				# funcion de saliday  pausa del bot
				time.sleep(2)
				Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [self.idbot]))			
				if Dato[0] != None:				
					if Dato[0] == "Eliminar":
						ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [self.idbot, self.idlabor, 'Detenido por usuario']))
						#driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
						time.sleep(1)														
						self.driver.quit()
						return



				data = ConectorDbMysql().FuncGetUpdSpr(1,"spr_get_otsptsgeswf",Arraydatos=[self.ciudad])				

				if data !=None:
					print("*", data)
					contadorReinicio+=1
					if contadorReinicio == LimiteContador:
						self.driver.refresh()
						time.sleep(10)
						contadorReinicio=0					

					ahora = timer()
					DicionarioDatos = json.loads(data[7])				
					DicionarioDatos['Fecha']=ahora[0]
					DicionarioDatos['Hora']=ahora[1]
					

					BotWfm.EsperaSearch()
					EstadoConsulta = BotWfm.FillBusquedaBacklog(data[3])
					time.sleep(1)
					if EstadoConsulta[0]:
						# ingreso a confirmacion
						self.driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]').click()			
						WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
						#===================================== ingreso al formulario=============================================================
						element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
						self.driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Confirmación")]').click()
						WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

						#====generar las notas desde la consulta
						
						def agente_confirmacion_ck():
							try:
								if driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').get_attribute("checked")==None:
									driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation"]').click()								
								else:
									pass
							except Exception as e:
								print(e)
								

						agente_confirmacion_ck()

						def confirmacion_agente_ck():
							if driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Confirmation_IVR"]').get_attribute("checked")==None:
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Confirmation_IVR"]').click()
							else:
								pass
						
						try:
							confirmacion_agente_ck()
						except:
							pass

						EstConf=data[5].upper().strip()
						def R_confirmacion():
							driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Resultado"]').click()
							gs=0
							while gs<2:
								try:							
									if EstConf=="ADELANTO":
										driver.find_element(by=By.XPATH, value='//*[@title="ADELANTO"]').click()
									elif EstConf=="CANCELADA":
										driver.find_element(by=By.XPATH, value='//*[@title="CANCELADA"]').click()
									elif EstConf =='VISITA CONFIRMADA':
										driver.find_element(by=By.XPATH, value='//*[@title="CONFIRMADO"]').click()
									elif EstConf=="NO CONTACTO":
										driver.find_element(by=By.XPATH, value='//*[@title="NO CONTACTO"]').click()
									elif EstConf=="NUMERO ERRADO":
										driver.find_element(by=By.XPATH, value='//*[@title="NUMERO ERRADO"]').click()
									elif EstConf=="REPROGRAMADA":
										driver.find_element(by=By.XPATH, value='//*[@atitle="REPROGRAMADA")]').click()
									else:
										driver.find_element(by=By.XPATH, value='//*[@title="CONFIRMADO"]').click()							
									break

								except Exception as e:
									print(e)
									time.sleep(1)
									gs+=1
						
						R_confirmacion()

						def aliado():				
							driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_CONF_Aliado CGO"]').click()
							gs=0
							while gs<2:
								try:
									element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_CONF_Aliado CGO"]')))
									if driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_CONF_Aliado CGO"]').get_attribute("value")!="GNP":
										driver.find_element(by=By.XPATH, value='//div[@data-value="GNP"]').click()        													
									break
								except Exception as e:
									print(e)
									time.sleep(1)
									gs+=1
						
						aliado()
						
						def cliente_gestion():					
							driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Approver"]').clear()
							driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Approver"]').send_keys("Gestion backlog")																
						
						cliente_gestion()

						def usuario_CGO():
							driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_User"]').clear()
							driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_User"]').send_keys(DicionarioDatos['Asesor'])
							
						usuario_CGO()


						#======notas confirmacion============

						def notas_confirmacion():
							try:
								DicNotasBack=DicionarioDatos				

								Notageneral = f"""GESTION BACK CND OT: {data[3]}\nCuenta: {data[2]}\nAsesor:{str(DicNotasBack['Asesor']).strip()} \nFecha: {DicNotasBack['Fecha']} {DicNotasBack['Hora'] } \n{str(DicNotasBack['Contactabilidad']).strip()} {str(DicNotasBack['Gestion Realizada']).strip()} \nObservaciones {str(DicNotasBack['Observaciones']).strip()}"""
								for i in range(5):
									if "Numero Telefono%s"%i in DicNotasBack.keys():
										Notageneral+="\nNumero Telefono %s: %s, Gestion Numero %s: %s Persona que Contesta: %s"%(i,DicNotasBack["Numero Telefono%s"%i],i,DicNotasBack["Gestion Numero%s"%i],DicNotasBack["Persona_Contesta%s"%i])

								#limpiar la cadena
								Notageneral = Notageneral.replace("\t", "").strip()
								Notageneral = " ".join(Notageneral.split())
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Notes"]').clear() # limpiar el campo
								driver.find_element(by=By.XPATH, value='//*[@data-label="XA_Agent_Confirmation_Notes"]').send_keys(Notageneral)
							except Exception as e:
								Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
								print(Nomb_error)							

						notas_confirmacion()
						ConectorDbMysql().FuncInsInfoOne(["spr_upd_otsptsgeswf", [data[0],"Notas wf ok",f"{EstadoConsulta[1]} {EstadoConsulta[2]} {EstadoConsulta[3]}"]])
						
						element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
						driver.find_element(by=By.XPATH, value='//*[@type="submit" and contains(text(),"OK")]').click()	
						
						try:
							element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]')))
							driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
						except Exception as e:
							driver.back()
							time.sleep(2)
							driver.back()
							Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
							print(Nomb_error)
						
						time.sleep(1)
					else:
						# actualizar en db el resultado					
						ConectorDbMysql().FuncInsInfoOne(["spr_upd_otsptsgeswf", [data[0],"Error notas",f"{EstadoConsulta[1]} {EstadoConsulta[2]} {EstadoConsulta[3]}"]])
					time.sleep(0.5)
				else:
					time.sleep(secrets.choice((10,15,20,30,35,40,45,50,55,60)))
			
			# salida despues de cumplir el tiempo
			ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [self.idbot, self.Idactividad, 'Labor terminada']))
			#driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
			time.sleep(1)														
			self.driver.quit()
			return
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)
			self.driver.quit()