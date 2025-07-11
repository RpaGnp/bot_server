
#LIBRERIAS PARA CHROMEDRIVER***********************
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os
#from datetime import time as tmr
from datetime import datetime,timedelta
from .CancelaPinAgenda import handlepincancelar
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *

class HandleAgendamiento(handlepincancelar):
	def __init__(self,driver):
		self.driver = driver
		super().__init__(driver)
		self.dicGesOrdenes={"NO AGENDADO":{"VenConAgenda":'//div[contains(text(),"Agenda registrada correctamente")]'},
										"NO REALIZADO":{"VenConAgenda":'//div[contains(text(),"Reagenda realizada correctamente")]'},
										"AGENDADO":{"VenConAgenda":'//div[contains(text(),"Reagenda realizada correctamente")]'},
										"REPROGRAMADA":{"VenConAgenda":'//div[contains(text(),"Reagenda realizada correctamente")]'},
										"CANCELADA":{"VenConAgenda":'//div[contains(text(),"Agenda registrada correctamente")]'}
										}

	def login(self,driver,Usuario,Clave):	
		try:
		    driver.get("https://agendamiento.claro.com.co")
		except Exception as e:
		    driver.quit()
		    return 2
		driver.implicitly_wait(180)
		myDinamicElement = driver.find_element(by=By.XPATH, value='//*[@class="ico_Candado login_alertas"]')

		driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').clear()
		driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').send_keys(Usuario)
		time.sleep(1)	
		element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="password"]')))
		driver.find_element(by=By.XPATH, value='//*[@type="password"]').clear()
		driver.find_element(by=By.XPATH, value='//*[@type="password"]').send_keys(Clave)
		time.sleep(3)
		element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@name="Submit"]')))
		if driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').is_displayed():
		    driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').click()
		time.sleep(2) 	
		try:
			element = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//nav[@class="ClaroTemplate-nav clearfix desktop-nav"]')))
		except:
			return False

	def prepareform(self):
		for xpath in ['//div[@id="confirmacion"]//input[@name="confir__atiende"]','//div[@id="confirmacion"]//tr[@id="mail2Field"]//input[@name="email2"]',
			'//div[@id="confirmacion"]//input[@name="confir_num2"]']:
			element = self.driver.find_element(By.XPATH,xpath)
			self.driver.execute_script("arguments[0].removeAttribute('hidden')", element)

	def fillform(self):
		self.prepareform()
		#//div[@id="confirmacion"]//table//tr//th[contains(text(),'Confirmación de la Visita')]
		numerocel=self.driver.find_element(By.XPATH,'//input[@placeholder="Télefono 1" and @name="confir_num_default"]').get_attribute('value')
		ArrayDatos=[self.driver.find_element(By.XPATH,'//*[@id="mod_agenda"]/table/tbody/tr[4]/th/div[2]/div[2]').text,"notiene@claro.com","notiene@claro.com",'1234567890']#driver.find_element(By.XPATH,'//*[@id="confir_num_default"]').get_attribute('value')[2:-1]
		for i,j in enumerate(['//input[@placeholder="Persona que atiende"]','//input[@placeholder="E-mail 1"]','//input[@placeholder="E-mail 2"]','//input[@name="confir_num2"]']):
			element=self.driver.find_element(By.XPATH,j)
			if element.get_attribute('value')=="":
				element.clear()
				element.send_keys(ArrayDatos[i])		
		
		for i in range(2):
			self.fillformReagendar()
		
	def fillformReagendar(self):
		for x in ['//input[@name="confir_email1"]','//input[@name="confir_email2"]','//input[@name="check_tel2"]']:
			element=self.driver.find_element(By.XPATH,x)	
			if element.is_selected()==False:
				element.click()

	def GetFecha(self,diccapa):
		'''
		Ordena el dicionario de capacidad y da click en la mas cercana
		arg: dicionario de fecha on su respectivo XPATH
		click en el mas cercano
		'''
		sorted_fechas = sorted(diccapa.items(), key=lambda item: item[0])
		driver.find_element(By.XPATH,sorted_fechas[0][1]).click()

	def RecorredorcapacidadFecha(self,franjaAgenda,dia):
		conFilas=len(self.driver.find_elements(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr'))
		conColumnas =len(self.driver.find_elements(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr[%s]/td'%conFilas))
		arrayXpathDia = []
		try:
			fecha_original_obj = datetime.strptime(dia, "%d/%m/%Y")
		except:							
			fecha_original_obj = datetime.strptime(dia, "%d-%m-%y")			
		
		fecha_nueva_str = fecha_original_obj.strftime("%Y-%m-%d")
		
		if datetime.now().time().hour <= 12:
			inicol =2			
		else:
			inicol = 3
			
		for celda in range(inicol,conColumnas):
			for fila in range(1,conFilas):				
				elemento=self.driver.find_element(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr['+str(fila)+']/td['+str(celda)+']')
				diacupo = elemento.get_attribute('data-date')
				franja = elemento.get_attribute('data-time-slot')
				cancupos=elemento.text
				cancupos=int(cancupos.split(" ")[0])
				if fecha_nueva_str == diacupo:
					try:
						arrayXpathDia.append({"Elemento":elemento,"Franja":int(franja.split("-")[0]),"Cupos":cancupos})
					except:
						continue
				else:
					continue
		
  		# franjas segun los cupos disponibles en una fechas
		for dic in arrayXpathDia:
			if (dic['Franja'] < 12 and dic['Cupos'] > 0 and franjaAgenda.lower() == "am") or \
			(dic['Franja'] > 12 and dic['Cupos'] > 0 and franjaAgenda.lower() == "pm"):
				dic['Elemento'].click()
				return True
		return False
		
	def Recorredorcapacidad(self):
		print("ver capacidad")
		#================recorre la capacida mostrada por filas y columnas==============
		EstadoAgedar = False
		dicCapacidad = {}
		#tim = timer()
		#HoraActual =  datetime.strptime(tim[1], "%H:%M:%S").time()
		#FechaActual = datetime.strptime(tim[3], '%d/%m/%Y')
		if datetime.now().time().hour <= 12:
			inicol =2			
		else:
			inicol = 3

		conFilas=len(self.driver.find_elements(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr'))
		conCeldas =len(self.driver.find_elements(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr[%s]/td'%conFilas))
		
		for celda in range(inicol,conCeldas):											
			for fila in range(1,conFilas):					
				elemento=self.driver.find_element(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr['+str(fila)+']/td['+str(celda)+']')					
				diacupo=elemento.get_attribute('data-date')
				cancupos=elemento.text				
				cancupos=int(cancupos.split(" ")[0])													
				print(cancupos)
				if cancupos > 0 :# and datetime.now().time() < limite_hora:					
					#if datetime.strptime(diacupo, '%Y-%m-%d') == FechaActual and HoraActual <= datetime.strptime('12:00:00', "%H:%M:%S").time():
					EstadoAgedar=True
					self.driver.find_element(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr['+str(fila)+']/td['+str(celda)+']').click()
					return True
					#else:
					#	dicCapacidad[diacupo]=xpath
					#	EstadoAgedar=True						
		return EstadoAgedar

	def jumpagenda(self):		
		self.driver.execute_script("$('#iframeMapa').hide();")
		
	def fillwindowpinreagenda(self):		
		WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_reagenda"]')))
		self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_reagenda"]//textarea').send_keys('Envío pin')
		time.sleep(0.5)
		self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_reagenda"]//input[@type="submit"]').click()
		WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))
		return
		try:
			WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]')))            
			return 1
		except:
			return 0

	def hideWindowPin(self):		
		WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))
		venPin = self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]')
		if venPin.is_displayed():		
			self.driver.find_element(By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]//span[@class="ui-button-text" and contains(text(),"Volver")]').click()
			return 1
		else:
			return 0

	def Espinvvencarga(self,tiempo):
		WebDriverWait(self.driver, tiempo).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))

	def AgendamientoDirecto(self):
		#" cuando exista un Rq y se detecte esta ventana de MOtivo de reagendamiento o agenadamiento"
		self.Espinvvencarga(45)
		self.driver.find_element(By.XPATH,'//div[contains(@aria-labelledby, "ui-dialog-title-dialog_msg_popup_motivo")]//textarea').send_keys("Agendamiento orden")
		time.sleep(0.5)
		self.driver.find_element(By.XPATH,'//div[contains(@aria-labelledby, "ui-dialog-title-dialog_msg_popup_motivo")]//input[@type="submit"]').click()
		#rata
		self.Espinvvencarga(45)

	def mensajesModulo(self):				
		clases = self.driver.find_elements_by_css_selector("[class^='ui-dialog ']")					
		for clase in clases:
			if "display: block;" in clase.get_attribute("style"):
				ErrorOrden = clase.text				
				print(ErrorOrden)
				if "Pin Generado satisfactoriamente." in ErrorOrden:
					self.hideWindowPin()
					return 1,1	
				if "Motivo de Re Agendamiento" in ErrorOrden:
					self.AgendamientoDirecto()
					return 1,0
				if "Señor usuario: el estado de la cuenta matriz no cuenta con un estado habilitado para agendar el tipo de trabajo seleccionado." in ErrorOrden:
					#self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_Error"]//button').click()
					return 0,0
				if "La orden de trabajo NO contiene en RR caracteristicas necesarias para agendamiento en Work Force. Por favor revisar en RR los campos basicos segun el tipo de trabajo" in ErrorOrden:
					return 0,0
				if "Se ha superado el tiempo limite para agendar sobre esta franja, por favor seleccione otra." in ErrorOrden:																					
					return 0,0
					
				if "Error de Creacion de la Orden de Trabajo en Sistema Ya existe Agenda Recargar" in ErrorOrden:
					return 0,0		
				if "Revisa nuevamente la capacidad. El cupo seleccionado ya fue asignado." in ErrorOrden:
					return 0,0
				if 'El campo "Persona que atiende" no puede estar vacío' in ErrorOrden:
					return 0,0
				if 'El campo "E-mail 2" no puede estar vacío' in ErrorOrden:
					return 0,0
				if 'El campo "Numero Celular" no puede estar vacío' in ErrorOrden:
					return 0,0
				if "Usuario no tiene permisos para agendar sobre este tipo de trabajo" in ErrorOrden:
					return 0,0
				if "Error de conexión con EtaDirect por favor intente mas tarde..." in ErrorOrden:
					return 0,0
				if "SubTipo de Trabajo no definido" in ErrorOrden:
					return 0,0
		return 1,1

	def SelectorAgendaOts(self,idbot,idAct,Trabajo):
		# funcion principal
  
		driver=self.driver		
		#limite_hora = tmr(12, 0, 0)
		try:
			sql="SELECT ACB_CUSUAPL1,ACB_CCLAVEAPL1 from tbl_hactividadesbot where ACB_NID='"+str(idAct)+"'"
			Credenciales=array_datos=ConectorDbMysql().FuncGetInfo(1,sql)
			time.sleep(1)		
			sql="""
					SELECT dx_nid,dx_corden,dx_caliado,dx_cciudad,dx_dfechaage,dx_cobservacion
					FROM tbl_hagndasdxrx
					WHERE dx_nidbot=%s AND  dx_cestgestion='Pendiente';
				"""%idAct
			array_datos=ConectorDbMysql().FuncGetInfo(0,sql)		
			tomorrow = datetime.now() + timedelta(days=1)
			diaAgenda=tomorrow.strftime("%Y-%m-%d")	
			if Trabajo ==  "Agendar->pin->cancelar":
				self.CreadorVentanas(idAct,idbot)# modulo heredado

			for data in array_datos:	
				if Trabajo ==  "Agendar->pin->cancelar":
					self.GetVentcancelaPin()# modulo heredado
				print(data)				
				ConectorDbMysql().RepActividad(idbot)
				# funcion de salida, pausa del bot
				time.sleep(2)
				Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idbot]))
				# print(Dato[0])
				if Dato[0] != None:
					if Dato[0] == "Eliminar":
						ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Detenido por usuario']))
						#driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
						time.sleep(1)					
						driver.quit()
						return
				driver.get('https://agendamiento.claro.com.co/MGW/MGW/Agendamiento/index.php')
				#ingreso consultar orden
				driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').click()
				driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').clear()
				driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').send_keys(data[1])
				time.sleep(1)			
				if any("LLS" in str(item).upper() for item in data): #(normalmente deberia estar en data[4])
					driver.find_element(By.XPATH,'//input[@type="radio" and @value="L"]').click()
				else:
					driver.find_element(By.XPATH,'//input[@type="radio" and @value="O"]').click()
				time.sleep(0.5)
				driver.find_element(By.XPATH,'//input[@type="submit"]').click()

				try:
					estado_element = WebDriverWait(driver, 10).until(
						EC.presence_of_element_located((By.ID, "estadoag"))
					)
					estado_texto = estado_element.text.strip()
					estados_validos = [
						"AGENDADO",
						"REPROGRAMADA"
					]
					if estado_texto in estados_validos and Trabajo != "Adelantar Ots":
						continue
				except Exception as e:
					print(f"Error al validar estado: {str(e)}")
					continue

				# verificar orden 
				if driver.find_element(By.XPATH,'//body').text=='ningun dato parametrizado':
					sql = ("spr_upd_estgesdx", [data[0], 'ningun dato parametrizado'])			
					ConectorDbMysql().FuncInsInfoOne(sql)
					continue

				# verificar orden agenda pr wfm
				if driver.current_url!='https://agendamiento.claro.com.co/MGW/MGW/Agendamiento/agendamiento.php':
					sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada, Redirige a modulo agendamiento antiguo!'])			
					ConectorDbMysql().FuncInsInfoOne(sql)
					continue

				#dentro de la orden
				try:			
					WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]')))
				except Exception as e:
					ConectorDbMysql().FuncInsInfoOne(("spr_upd_estgesdx", [data[0], e]))
					continue

				time.sleep(2)
				if 'Esta orden no se puede agendar en workforce' in driver.find_element(By.XPATH,'//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]').text:
					sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada, Esta orden no se puede agendar en workforce'])			
					ConectorDbMysql().FuncInsInfoOne(sql)
					continue
				
				EstadoOt=driver.find_element(By.XPATH,'//div[@id="estadoag"]').text						
				fechaAgenda=driver.find_element(By.XPATH,'//table[@class="td_content_agend"]/tbody//th[contains(text(),"Fecha Programada :")]/following-sibling::td[@class="verderesaltado"][1]').text
				
				#llenar los campos para legalizar la orden
				try:
					driver.find_element(By.XPATH,'//div[@id="confirmacion_menu"]').click()
				except:
					sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendable Cerrada en RR'])
					ConectorDbMysql().FuncInsInfoOne(sql)									
					continue
				
				if EstadoOt in ["NO AGENDADO"]:
					self.fillform()
				
				if EstadoOt in ["AGENDADO","REPROGRAMADA","NO REALIZADO"]:
					self.fillformReagendar()
				
				#======================================= radar botones =================================================
				DicButton={}
				VarAGenda=False			
				time.sleep(2)
				EsAgendable = False
				for buttonAccion in driver.find_elements(By.XPATH,'//div[@class="buttons-form"]/input'):
					DicButton.update({buttonAccion.get_attribute("value"):buttonAccion.get_attribute("style")})					
					if buttonAccion.get_attribute("style")=='display: inline-block;':
						#print(buttonAccion.get_attribute('value'))
						valuebtn = buttonAccion.get_attribute('value') 
						if valuebtn in ["Agendar"]:
							driver.execute_script("ajaxCapacity()")					
							#buttonAccion.click()
							try:
								WebDriverWait(driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))
								EsAgendable = True
							except:
								EsAgendable = False
						elif valuebtn in ["Re Agendar"]:
							buttonAccion.click()
							WebDriverWait(driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))
							msnModulo = self.mensajesModulo()
							if msnModulo[0]:
								if EstadoOt == "CANCELADA":									
									pass								
								else:
									# esperar si aparece el cuadro de agendar
									if msnModulo[1]:
										self.fillwindowpinreagenda()									
									
									self.driver.execute_script("ajaxCapacity()")
									time.sleep(2)
								EsAgendable = True
							else:
								EsAgendable = False

						else:
							continue

					#if EstadoOt=="NO AGENDADO":
				#============================================ mensajes recientes ==========================
				ErrorOrden = ""
				if EsAgendable:
					if self.mensajesModulo()[0]==False:					
						sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendable {ErrorOrden}'])
						ConectorDbMysql().FuncInsInfoOne(sql)															
						continue
					time.sleep(1)
					
					'''if EstadoOt in ['NO REALIZADO',"AGENDADO","REPROGRAMADA"]:
																					element = WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_reagenda"]')))
																					driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_reagenda"]//textarea').send_keys("AGENDAR")
																					time.sleep(0.5)
																					driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_reagenda"]//input[@type="submit"]').click()'''
					
				#================================= verificar cupos ==================================================
				#EsAgendable=1
				if EsAgendable:
					## ocultar el mapa
					self.driver.execute_script("$('#iframeMapa').hide();")
					try:
						WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="semana_calendario_capacity"]/table/tbody')))											
					except:																	
						try:
							element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="infover"]/input[@value="Ag. Tradicional"]')))												
						except Exception as e:							
							sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendabla, Perfil de MG no permite agendar'])
							ConectorDbMysql().FuncInsInfoOne(sql)	
							continue

						x=0
						while x<5:
							try:
								elemento = driver.find_element(By.XPATH,'//div[@class="infover"]/input[@value="Ag. Tradicional"]')
								if elemento.is_displayed():
									elemento.click()							
								element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="semana_calendario_capacity"]/table/tbody')))											
								break
							except Exception as e:
								time.sleep(1.5)
								x+=1
								print(e)

						#javascript_code = "cambioTipoAgen();"
						#element = driver.find_element_by_xpath("//input[contains(@onclick, 'cambioTipoAgen();')]")
						#driver.execute_script(javascript_code, element)

					EstadoCapacidad=driver.find_element(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody').text					
					#print(EstadoCapacidad)
					if "No existe capacidad disponible para los intervalos" in EstadoCapacidad:
						sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendable {EstadoCapacidad}'])
						ConectorDbMysql().FuncInsInfoOne(sql)	
						continue
					else:pass					
					
					# ================= dependiendo de la base, si se recibe fecha y franja se debe escoger capacidad especificada
					if data[3].lower().strip() == "no aplica" and data[3].lower().strip() == "no aplica":						
						agendado= self.Recorredorcapacidad()													
					else:
						agendado= self.RecorredorcapacidadFecha(data[3],data[4])					

					try:
						driver.implicitly_wait(0)
						WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[@id="ui-dialog-title-dialog_Error"]')))
						driver.find_element(By.XPATH,'//button//span[contains(text(),"Continuar")]').click()	
						time.sleep(2)
					except:
						pass
					driver.implicitly_wait(30)

					if agendado==False:
						sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendable No hay capacidad disponible'])
						ConectorDbMysql().FuncInsInfoOne(sql)	
						continue

					#wait
					#======================== verificar que la capacidad se ha tomado correctamente ====================
					#clases = driver.find_elements_by_css_selector("[class^='ui-dialog ']")										
					
					if self.mensajesModulo()[0]==False:
						sql = ("spr_upd_estgesdx", [data[0], 'Error tomando capacidad'])			
						ConectorDbMysql().FuncInsInfoOne(sql)	
						continue

					WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, '//span[@id="ui-dialog-title-dialog_confirmacion_agenda"]')))

					time.sleep(0.5)
					driver.find_element(By.XPATH,'//button//span[contains(text(),"Confirmar")]').click()					
					WebDriverWait(driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))
					
					#======================== verificar que la capacidad se ha tomado correctamente ====================
					clases = driver.find_elements_by_css_selector("[class^='ui-dialog ']")					
					msgerrorcapacidad=False
					for clase in clases:
						if "display: block;" in clase.get_attribute("style"):
							ErrorOrden = clase.text
							print(ErrorOrden)
							if "Se ha superado el tiempo limite para agendar sobre esta franja, por favor seleccione otra." in ErrorOrden:																					
								msgerrorcapacidad=True
								break
							elif "Error de Creacion de la Orden de Trabajo en Sistema Ya existe Agenda Recargar" in ErrorOrden:
								msgerrorcapacidad=True
								break

							elif "Error de Creacion de la Orden de Trabajo en Sistema Ya existe Agenda Recargar" in ErrorOrden:
								msgerrorcapacidad=True
								break

					if msgerrorcapacidad:
						sql = ("spr_upd_estgesdx", [data[0], 'Error tomando capacidad'])			
						ConectorDbMysql().FuncInsInfoOne(sql)	
						continue

					try:
						element = WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, self.dicGesOrdenes[EstadoOt]["VenConAgenda"] )))
						for i in range(3):
							try:
								driver.find_elements(By.XPATH,'//span[contains(text(),"Cerrar")]')[-1].click()						
								break
							except:
								time.sleep(2)
								continue

						sql = ("spr_upd_estgesdx", [data[0], 'Orden agendada con exito'])			
						ConectorDbMysql().FuncInsInfoOne(sql)
						VarAGenda=True
						self.login(driver, Credenciales[0].decode('utf-8'), Credenciales[1].decode('utf-8')) if EstadoOt == "NO AGENDADO" else None

					except Exception as e:
						Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
						print(Nomb_error)					
						try:				
							alert = driver.switch_to.alert
							time.sleep(1)				
							alert.accept()
							sql = ("spr_upd_estgesdx", [data[0], 'Orden agendada con exito'])			
							ConectorDbMysql().FuncInsInfoOne(sql)
							VarAGenda=True
							self.login(driver, Credenciales[0].decode('utf-8'), Credenciales[1].decode('utf-8')) if EstadoOt == "NO AGENDADO" else None
						except Exception as e:
							Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
							print(Nomb_error)
													
					
					if VarAGenda==False:
						sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada'])			
						ConectorDbMysql().FuncInsInfoOne(sql)					
				else:
					sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendada {DicButton} {EstadoOt}'])
					ConectorDbMysql().FuncInsInfoOne(sql)
					continue
				
				# continuar a enviar pin
				'''if VarAGenda and Trabajo == "Agendar->pin->cancelar":
																	self.GetVentcancela()
																	self.MainCancelacion(data) #Modulo Heredado
																	sql = ("spr_upd_estgesdx", [data[0], 'Orden agendada con exito, pin generadado con exito, agenda cancelada con exito'])			
																	ConectorDbMysql().FuncInsInfoOne(sql)'''


			ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Labor Terminada']))		
			driver.quit()
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)
			try:
				sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendable error ot'])
				ConectorDbMysql().FuncInsInfoOne(sql)
			except: pass
			driver.quit()