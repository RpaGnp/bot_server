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
import re

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

class SelectorNotasAuto():
	"""Modulo de gestion el cual consulta en base de datos nuevas razones y las getiona en Wfm"""
	def __init__(self, driver):		
		self.driver = driver		
		self.DicRazones = {'AMPLIACION DE TAP HFC':'H','AMPLIACION DE TAP FTTH':'H','CLIENTE AUN NO DESEA EL TRABAJO':'7','CLIENTE NO TIENE DINERO':'O','CLIENTE SOLICITA REPROGRAMAR':'K',
		'DIRECCION Y/O DATOS ERRADOS':'B','DUCTOS/INFRESTRUCTURA PREDIO NO APTA':'W','EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES':'6','FALTA DE MATERIALES/EQUIPOS':'F',
		'FUERA DE COBERTURA DTH':'/','FUERA DE ZONA':'Z','INSTALACIÓN REQUIERE ANDAMIO ARNES':'Y','LLUVIA - FACTORES CLIMÁTICOS':'L','MAL AGENDADO/MAL PROGRAMADO':'M',
		'NO INGRESO/CLIENTE CONFIRMA SERVICIO OK':'S','NO INGRESO/CLIENTE CONFIRMA':'S','PERMISOS DE ADMINISTRACION':'P','PROBLEMA ORDEN PUBLICO/ZONA ROJA':'X','PROBLEMAS EN LA RED EXTERNA':'%',
		'PROBLEMAS EN SISTEMAS APLICATIVOS CLARO':'Q','REPLANTEAMIENTO':'R','REQUIERE MOVIL ELITE':'=','SUSCRIPTOR NO DESEA/NO REQUIERE TRABAJOS':'E',
		'SUSCRIPTOR NO ESTA EN CONDICIÓN DE ATENDER':'?','UNIDAD POSIBLE FRAUDE':'V',
						 'VENTA DEVUELTA AL ASESOR':'4','NO CONTACTO CON CLIENTE':'C','INCUMPLIMIENTO ALIADO':"I",
						 'CAMARA/SOLDADA O INUNDADA':'+','FUERA DE COBERTURA WTTH':'/'}

		self.ArrayRazonesEspeciales=['PROBLEMAS EN SISTEMAS APLICATIVOS CLARO','REQUIERE MOVIL ELITE','PROBLEMAS EN PLATAFORMAS','FALTA DE MATERIALES/EQUIPOS']
		if 'Windows' in platform():
			self.PathImagenes = CreadorCarpetas("C://DBGestionBot//BotcndRazones/")
		else:
			self.PathImagenes = CreadorCarpetas("/DBGestionBot/BotcndRazones/")
	
	def GestorDic(self,dic):
		return json.loads(dic)

	def VijilanteRazones(self,idBot,Idactividad,ciudad):		
		BotWfm=BotGestionWF(self.driver)
		contadorReinicio=0
		LimiteContador=10
		limite_hora = tmr(22, 0, 0)
		# self.driver.save_screenshot('screenshot.png')

		while datetime.now().time() < limite_hora:
			# reporta actividad del bot
			ConectorDbMysql().RepActividad(idBot)
			# funcion de saliday  pausa del bot
			time.sleep(2)
			Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idBot]))			
			if Dato[0] != None:				
				if Dato[0] == "Eliminar":
					ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
					#driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
					time.sleep(1)														
					self.driver.quit()
					return
			
			# os.system('cls')
			print(Idactividad)
			print(ciudad)
			data = list(ConectorDbMysql().FuncGetUpdSpr(1,"spr_get_notpendes",Arraydatos=[Idactividad,ciudad]))
			print(data[0])
			if data[0] == 'False':
				try:
					print('tomar caso')
					data = list(ConectorDbMysql().FuncGetUpdSpr(1,"spr_get_notpendes_1",Arraydatos=[Idactividad,ciudad]))
				except Exception as e:
					continue
				
			print("*", data)

			if len(data) >= 1 and data[0] != 'False':
				print("*", data)
				
				# self.driver.save_screenshot('screenshot.png')

				ahora = timer()
				DicionarioDatos=self.GestorDic(data[3])
				# DicionarioDatos=json.loads(DicionarioDatos)
				DicionarioDatos['Fecha']=ahora[0]
				DicionarioDatos['Hora']=ahora[1]
				ArrayDataOt={}

				formatted_strings = [f'{x}: {str(y).strip()}' for x, y in DicionarioDatos.items()]
				resulting_string = ", ".join(formatted_strings)

				BotWfm.EsperaSearch()

				EstadoConsulta = BotWfm.FillBusqueda(data[1])
				
				if EstadoConsulta[0]:
					try:
						#dentro de la orden
						#extrae datos nesesarios de la orden
						ArrayDataOt=BotWfm.ExtraeTecOt()						
													
						# marcar notas as400						
						#BotWfm.NotasAS400(resulting_string)


						# self.driver.save_screenshot('screenshot.png')


						# marca confirmacion
						BotWfm.MarcarSeguimiento(DicionarioDatos)
						# self.driver.save_screenshot('screenshot.png')

						x=0
						while x<3: 
							try:
								# Espera hasta que el elemento `toolbar-items-list` sea visible
								toolbar_items_list = WebDriverWait(self.driver, 60).until(
									EC.visibility_of_element_located((By.CLASS_NAME, "toolbar-items-list"))
								)
								# Encuentra todos los elementos `toolbar-item` dentro de `toolbar-items-list`
								ArrayElements = toolbar_items_list.find_elements(By.CLASS_NAME, "toolbar-item")
								
								# self.driver.save_screenshot('screenshot.png')
																				
								Razon=False
								for elemento in ArrayElements:
									texto = elemento.text							
									if texto.lower()=="razón":
										print('si es razon')
										Razon=True						
								
								if Razon:
									self.driver.find_element(By.XPATH,'//button[@title="Razón"]').click()
								else:
									self.driver.find_element(By.XPATH,'//div[@class="toolbar-menu-button-container"]//button[@title="Acciones" and @aria-label="Acciones"]').click()
									WebDriverWait(self.driver, 10).until(
										EC.visibility_of_element_located((By.XPATH,'//div[@aria-label="Acciones"][1]//div//button'))
									)
									time.sleep(0.5)
									# self.driver.save_screenshot('screenshot.png')

									# verificar que  'Razon exista en la lista'
									razonlist=False
									for i in self.driver.find_elements(By.XPATH,'//div[@aria-label="Acciones"][1]//div//button'):				
										if i.text.lower()=="razón":
											razonlist=True
											break
									# self.driver.save_screenshot('screenshot.png')
									
									if razonlist:
										self.driver.find_element(By.XPATH,'//div[@aria-label="Acciones"]//button//span[contains(text(),"Razón")]').click()
										# self.driver.save_screenshot('screenshot.png')
									else:
										ConectorDbMysql().FuncUpdSpr("spr_upd_gesotdes",[data[0], EstadoConsulta[1], EstadoConsulta[2], EstadoConsulta[3],json.dumps(ArrayDataOt),f"Ot No gestionada error Boton razon "])
										time.sleep(2)								
										self.driver.save_screenshot(f"{self.PathImagenes}/{data[0]}-RAZerrorimg3.png")
										ConectorDbMysql().FuncUpdSpr("spr_upd_libotnot",[data[0],"Error botton razon",f"{self.PathImagenes}/{data[0]}-RAZerrorimg3.png"])								
										self.driver.find_element(By.XPATH,'//button[@title="Consola de Despacho"]').click()
										# self.driver.save_screenshot('screenshot.png')
										continue
								break
							except Exception as e:
								x+=1
								self.driver.refresh()
								
						'''for i in driver.find_elements(By.XPATH,'//div[@aria-label="Razon de no completar, Requerido"]/div'):
							print("'",i.get_attribute("data-key"),"'",i.get_attribute("title"))
						'''
						# self.driver.save_screenshot('screenshot.png')

						WebDriverWait(self.driver, 10).until(
							EC.visibility_of_element_located((By.XPATH,'//input[@data-label="A_NotDoneCode"]//following-sibling::button'))
						)
						self.driver.find_element(By.XPATH,'//input[@data-label="A_NotDoneCode"]//following-sibling::button').click()
						time.sleep(0.5)	
						self.driver.find_element(By.XPATH,f'//div[@aria-label="Razon de no completar, Requerido"]/div[@data-key="{self.DicRazones[DicionarioDatos["Razon"]]}"]').click()


						if DicionarioDatos['Razon'] in self.ArrayRazonesEspeciales:
							if DicionarioDatos['Razon']=='REQUIERE MOVIL ELITE':
								self.driver.find_element(By.XPATH,"//input[@data-label='RAZ_Sup Aprueba']").send_keys(DicionarioDatos['SUPERVISOR'])

							elif DicionarioDatos['Razon']== 'PROBLEMAS EN SISTEMAS APLICATIVOS CLARO':
								self.driver.find_element(By.XPATH, '//input[@data-label="XA_NumeroTicket_FallaMasiva"]').send_keys(
									DicionarioDatos['RQ'])
								time.sleep(1)
								self.driver.find_element(By.XPATH, "//label[contains(text(),'Lista Razon Q')]/parent::div//following-sibling::button").click()
								time.sleep(1)
								self.driver.find_element(By.XPATH,f"//div[@aria-label='{DicionarioDatos['APLICATIVO']}']").click()
								time.sleep(1)
							
							elif DicionarioDatos['Razon'] == 'PROBLEMAS EN PLATAFORMAS':
								self.driver.find_element(By.XPATH,"//input[@data-label='XA_NumeroTicket_FallaMasiva']").send_keys(DicionarioDatos['Supervisor'])

							elif DicionarioDatos['Razon'] == 'FALTA DE MATERIALES/EQUIPOS':
								self.driver.find_element(By.XPATH,"//label[contains(text(),'Desplegable Razon F')]/parent::div//following-sibling::button").click()
								time.sleep(1)
								self.driver.find_element(By.XPATH, f"//div[@aria-label='{ DicionarioDatos['MATERIAL'] }']").click()
								time.sleep(1)
						# self.driver.save_screenshot('screenshot.png')

						#notas
						print('valores:   '+resulting_string)
						print('ahora:  ',ahora)
						print('ahora[0]:  ',ahora[0])
						print('ahora[1]:  ',ahora[1])
						print(ahora[0]+" "+ahora[1])
      
						try:
							resulting_string = resulting_string.replace('\n', ' ').replace('\r', ' ')
							FormatedNotas = re.search(r'\bOBSERVACION(?:ES)?\b\s*:\s*(.*)', resulting_string, re.IGNORECASE)
							if FormatedNotas:
								FormatedNotas = FormatedNotas.group(1).strip()
						except Exception as e:
							FormatedNotas = resulting_string[0:398]+" "+ahora[0]+" "+ahora[1]
						FormatedNotas = FormatedNotas[:398]

						print(FormatedNotas)          
						element = self.driver.find_element(By.XPATH,'//div/textarea[@data-label="closure_notes"]')
						element.clear()
						time.sleep(1)
						actions = ActionChains(self.driver)
						print(FormatedNotas)
						actions.move_to_element(element).click().send_keys(str(FormatedNotas).strip().replace("\n","").replace("\t","")).perform()
						del FormatedNotas
						# self.driver.find_element(By.XPATH,'//div/textarea[@data-label="closure_notes"]').send_keys(resulting_string)												
						time.sleep(1)						
						element = self.driver.find_element(By.XPATH,'//button[@class="button submit"]')
						self.driver.execute_script("arguments[0].scrollIntoView();", element)
						element.click()
						ConectorDbMysql().FuncUpdSpr("spr_upd_gesotdes",[data[0],EstadoConsulta[1],EstadoConsulta[2],EstadoConsulta[3],json.dumps(ArrayDataOt),"Ot gestionada!"])							
						# foto de cada ot gestionada por cupla de los hps de cali
						time.sleep(1)
						self.driver.save_screenshot(f"{self.PathImagenes}/{data[0]}-ResGestion.png")
						ConectorDbMysql().FuncUpdSpr("spr_upd_libotnot",[data[0],"Gestion ok",f"{self.PathImagenes}/{data[0]}-ResGestion.png"])
						# self.driver.save_screenshot('screenshot.png')


						#self.driver.refresh()
						#time.sleep(3)
						# BotWfm.Salida()
						# escalar a cacelar
						# escalar tambien las ordenes de no contacto
						#21 05 2024
						Nocontacto = True
						for index,valor in DicionarioDatos.items():
							if "Gestion Numero" in index and valor =="CONTACTO":
								Nocontacto=False
								break
							else:
								continue
						if Nocontacto:
							ConectorDbMysql().FuncUpdSpr("spr_ins_otnocont",[data[0],ArrayDataOt['Trabajo'],ArrayDataOt['CARPETA']])
						del Nocontacto	
						# self.driver.save_screenshot('screenshot.png')

						# try:
						# 	ArrayRazonesCancelables = Handledbmongo().GetTrabajosRazon(ciudad,ArrayDataOt['Trabajo'],ArrayDataOt['CARPETA'])												
							# self.driver.save_screenshot('screenshot.png')
							
						# 	if len(ArrayRazonesCancelables) !=0 :														
						# 		if ciudad.lower() !="bucaramanga":
						# 			contacto = False
						# 			for index,valor in DicionarioDatos.items():
						# 				if "Gestion Numero" in index and valor =="CONTACTO":
						# 					contacto=True
						# 					break
						# 				else:
						# 					continue
						# 		else:
						# 			contacto=True
								
						# 		if  self.DicRazones[DicionarioDatos["Razon"]] in ArrayRazonesCancelables:
						# 			if contacto:
						# 				#escalar razon para cancelacion								
						# 				ConectorDbMysql().FuncUpdSpr("spr_ins_razcan",[data[0],ArrayDataOt['Trabajo'],ArrayDataOt['CARPETA'],
						# 					DicionarioDatos["Razon"],self.DicRazones[DicionarioDatos["Razon"]]])


						# except Exception as e1:
						# 	Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e1).__name__, e1
						# 	print(Nomb_error)	

					except Exception as e:
						Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
						print(Nomb_error)
						ConectorDbMysql().FuncUpdSpr("spr_upd_gesotdes",[data[0], EstadoConsulta[1], EstadoConsulta[2], EstadoConsulta[3],json.dumps(ArrayDataOt),f"Ot No gestionada error {Nomb_error[0]}"])

						time.sleep(2)
						
						self.driver.save_screenshot(f"{self.PathImagenes}/{data[0]}-RAZerrorimg1.png")
						ConectorDbMysql().FuncUpdSpr("spr_upd_libotnot",[data[0],Nomb_error[0],f"{self.PathImagenes}/{data[0]}-RAZerrorimg1.png"])

				else:
					print(f"{self.PathImagenes}/{data[0]}-RAZerrorimg1.png")
					self.driver.save_screenshot(f"{self.PathImagenes}/{data[0]}-RAZerrorimg1.png")
					ConectorDbMysql().FuncUpdSpr("spr_upd_gesotdes",[data[0],EstadoConsulta[1],EstadoConsulta[2],EstadoConsulta[3],json.dumps(ArrayDataOt),"Ot no gestionada!"])	
					time.sleep(1)
					ConectorDbMysql().FuncUpdSpr("spr_upd_libotnot",[data[0],"--",f"{self.PathImagenes}/{data[0]}-RAZerrorimg1.png"])
			else:

				contadorReinicio+=1
				if contadorReinicio == LimiteContador:
					self.driver.refresh()
					time.sleep(10)
					contadorReinicio=0	
				else:
					time.sleep(20)	
					# self.driver.save_screenshot('screenshot.png')
					# time.sleep(secrets.choice((10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)))


		# salida despues de cumplir el tiempo
		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor terminada']))
		#driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
		time.sleep(1)														
		self.driver.quit()
		return
	