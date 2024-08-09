import time
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

from funciones_varias import *



class Botinteraccion():
	def __init__(self,driver):
		self.driver=driver


	def click(self,Xpath):
		WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, Xpath)))				
		self.driver.find_element(By.XPATH, value=Xpath).click()
		time.sleep(1)

	def dobleclick(self,ArrayXpath):		
		for i in ArrayXpath:
			WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, i)))				
			self.driver.find_element(By.XPATH, value=i).click()
			time.sleep(1)

	def ClicJs(self,xpathjs):#
		self.driver.execute_script(xpathjs)
		time.sleep(0.25)
		self.driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')


	def scrollXpath(self,xpathjs):
		
		script="""
			var element = document.querySelector('"""+xpathjs+"""');
			element.scrollIntoView();
			"""
		self.driver.execute_script(script)


class BotinteraccionMG():
	"""Interaccion de bot con mg"""
	def __init__(self, driver):		
		self.driver = driver

	def Radar(self,xpath):
		return self.driver.find_element(by=By.XPATH,value=xpath)

	def Radares(self,xpath):
		return self.driver.find_elements(by=By.XPATH,value=xpath)

	def ScrollTo(self,xpath):
		element=self.driver.find_element(by=By.XPATH,value=xpath)	
		self.driver.execute_script("arguments[0].scrollIntoView();",element)
	


class BotGestionWF():
	def __init__(self,driver):
		self.driver=driver
		self.ArrayTrabajos=['Arreglos','Blindaje.','Instalaciones','INSTALACIONES DTH',
							'INSTALACIONES FTTH','Mantenimiento Especial','MANTENIMIENTO FTTH',
							'MANTENIMIENTOS DTH','Orden Especial','Post Venta',
							'POSTVENTA FTTH','POSTVENTA DTH','TRASLADO FTTH','Traslados','TRASLADOS DTH']

		self.ArrayTrabajosBack= ['INSTALACIONES DTH','Instalacion Basica Bi',
		 'Instalacion FTTH_', 'POSTVENTA FTTH', 'Cambio Tecnologia TV',
		  'Blindaje.', 'MANTENIMIENTO FTTH', 'Postventa FTTH', 'PostVenta Bi',
		   'Arreglos FTTX', 'Arreglo Pymes', 'Instalaciones', 'BROWNFIELD',
		    'Traslados Pymes', 'Arreglo Bidireccional', 'Post Venta',
		     'Instalacion Empaquetada Bi','Postventa Pymes', 'Traslados', 'Arreglos',
		      'Instalacion Cableada Bi', 'INSTALACIONES FTTH', 'Mantenimiento FTTH', 'INSTALACIONES DTH',
		       'Blindaje Pymes', 'Blindaje', 'POSTVENTA  FTTH']

		self.ArrayColores=['background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);']
		self.ArrayColoresBack=['background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);','background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);']
		self.DiaGestion = fecha_actual(self)[0]

	def EsperasTitulos(self,Titulo):
		#wait = WebDriverWait(self.driver, 10)
		for i in range(10):
			if Titulo in self.driver.title:				
				return
			else:				
				time.sleep(2)

		#wait.until(EC.title_is(Titulo))
		

	def EsperaSearch(self):
		try:
			element = WebDriverWait(self.driver,50).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))			
		except:
			self.driver.refresh()
			self.driver.quit()
			return
		element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))				
		
		lupa=self.driver.find_element(by=By.XPATH, value='//div[@id="search-bar-container"]')						
		if lupa.is_displayed()==False:
			self.driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()				
		else:
			pass

	def BuscarOtEnList(self):
		self.driver

	def FillBusqueda(self,orden):
		driver=self.driver
		self.driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
		self.driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
		self.driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(orden)
		self.driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)

		fechaOt,tipoot,EstadOtColor=False,False,False

		try:
			element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e			
			return False, fechaOt,tipoot,EstadOtColor

		if driver.find_element(by=By.XPATH, value='//*[@class="toa-search-empty"]').text != "":
			return False, fechaOt,tipoot,EstadOtColor
		
		
		time.sleep(1)
		element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
		_lista_lls=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
		
		if len(_lista_lls)==0:					
			#FunGuardar(self,[data[0],"Marcacion Fallida"])
			return False, fechaOt,tipoot,EstadOtColor		

		for i in range(len(_lista_lls)):						
			fechaOt=driver.find_elements(by=By.XPATH, value='//*[@class="activity-date"]')[i].text																
			EstadOtColor=driver.find_elements(by=By.XPATH, value='//*[@class="activity-icon icon"]')[i].get_attribute("style")							
			tipoot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].text							
			print(i,fechaOt,EstadOtColor,tipoot)		
			
			if fechaOt =="" and any(trabajo in tipoot for trabajo in self.ArrayTrabajos) and EstadOtColor in self.ArrayColores:
				driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].click()											
				self.EsperasTitulos('Detalles de actividad')
				return True,fechaOt,tipoot,EstadOtColor
			else:
				continue

		return False, fechaOt,tipoot,EstadOtColor

	def FillBusquedaBacklog(self,orden):
		driver=self.driver
		self.driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
		self.driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
		self.driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(orden)
		self.driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)

		fechaOt,tipoot,EstadOtColor=False,False,False

		try:
			element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e			
			return False, fechaOt,tipoot,EstadOtColor

		if driver.find_element(by=By.XPATH, value='//*[@class="toa-search-empty"]').text != "":
			return False, fechaOt,tipoot,EstadOtColor
		
		
		time.sleep(1)
		element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
		_lista_lls=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
		
		if len(_lista_lls)==0:					
			#FunGuardar(self,[data[0],"Marcacion Fallida"])
			return False, fechaOt,tipoot,EstadOtColor		

		for i in range(len(_lista_lls)):						
			fechaOt=driver.find_elements(by=By.XPATH, value='//*[@class="activity-date"]')[i].text																
			EstadOtColor=driver.find_elements(by=By.XPATH, value='//*[@class="activity-icon icon"]')[i].get_attribute("style")							
			tipoot=driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].text
			tipoot=tipoot.replace("-"," ")							
			print("="*30,fechaOt)
			print("="*30,tipoot)
			print("="*30,EstadOtColor)

			
			if any(trabajo in tipoot for trabajo in self.ArrayTrabajosBack) and EstadOtColor in self.ArrayColoresBack:
				driver.find_elements(by=By.XPATH, value='//*[@class="activity-title"]')[i].click()											
				self.EsperasTitulos('Detalles de actividad')
				return True,fechaOt,tipoot,EstadOtColor
			else:
				continue

		return False, fechaOt,tipoot,EstadOtColor


	def NotasAS400(self,Notas):
		driver=self.driver		
		element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Notas")]')))
		driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Notas")]').click()
		WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

		'''botonback="document.querySelector('button[history-direction=""""back""""]').setAttribute('disabled','');"
								driver.execute_script(botonback)
						
								botonok ="document.querySelector('button[type=""""submit""""]').setAttribute('disabled', '');"
								driver.execute_script(botonok)'''

		element=self.driver.find_element(By.XPATH, '//textarea[@data-label="A_NOTAS"]')
		element.clear()		
		actions = ActionChains(self.driver)
		actions.move_to_element(element).click().send_keys(str(Notas).strip().replace("\n","").replace("\t","")).perform()
		
		'''botonok ="document.querySelector('button[type=""""submit""""]').removeAttribute('disabled');"
								driver.execute_script(botonok)'''
		time.sleep(1)
		
		driver.find_element(By.XPATH,'//button[@type="submit"]').click()

	def ExtraeTecOt(self):
		dicDatos={'Aliado':'//div[@data-label="XA_CompaniaRecurso"]','Tecnico':"//div[@data-ofsc-role='page-description-text']",
		'Nodo':"//div[@data-label='Node']","Duracion":'//div[@data-label="length"]','Trabajo':'//div[@data-label="aworktype"]',
		'CARPETA':'//div[@data-label="XA_WorkOrderSubtype"]','Incio - Fin':'//div[@data-label="eta_end_time"]'}		
		for clave,valor in dicDatos.items():
			try:
				dicDatos[clave] = self.driver.find_element(By.XPATH,valor).text		
			except:
				dicDatos[clave] = 0
				
		return dicDatos

	def MarcarSeguimiento(self,DicNotas):		
		driver=self.driver
		element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Backoffice")]')))
		driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Backoffice")]').click()
		element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
		driver.find_element(by=By.XPATH, value='//*[@class="button inline" and contains(text(),"Despacho")]').click()
		WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

		formatted_strings = ["%s: %s" % (x, str(y).replace("\n","").replace("\t","")) for x, y in DicNotas.items()]
		resulting_string = ", ".join(formatted_strings)
		#print(resulting_string)

		def cedAsesor():
			driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').clear()
			driver.find_element(By.XPATH,'//input[@class="form-item" and @data-label="A_AsesorCNDAtiende"]').send_keys(DicNotas['Id Usuario Cnd'])
		cedAsesor()
		
		
		def CausaSolicitudDespacho():
			x=0
			while x<=5:
				try:
					driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Causa Solicitud"]').click()
					time.sleep(2)
					driver.find_element(by=By.XPATH, value='//div[@aria-label="Seguimiento visita"]').click()
					break
				except Exception as e:								
					time.sleep(1)
					x+=1
		CausaSolicitudDespacho()

		def aliado():
			gs=0
			while gs<3:
				try:
					element = driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Aliado CGO"]')
					element.click()
					time.sleep(1)
					driver.find_element(by=By.XPATH, value='//div[@aria-label="GNP"]').click()
					break
				except Exception as e:
					Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
					print(Nomb_error)
					time.sleep(1)
					gs+=1

		aliado()

		def NotasCausa():
			x=0						
			while x<=5:
				try:
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_DESP_Notas Causa"]')))
					#driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Notas Causa"]').send_keys(resulting_string)
					elemento = driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Notas Causa"]')
					#driver.execute_script('arguments[0].value = arguments[1];', elemento, resulting_string)
					#elemento.send_keys(resulting_string.strip().replace("\n","").replace("\t",""))
					acciones = ActionChains(driver)
					acciones.move_to_element(elemento).click()
					acciones.send_keys(Keys.END)
					acciones.send_keys("\n"+resulting_string.strip()).perform()

					break
				except Exception as e:								
					x+=1

		NotasCausa()

		def Gestion():
			try:
				element=driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Detalle Gestion"]')
				driver.execute_script("arguments[0].scrollIntoView();", element)
				element.click()
				gs=0
				while gs<5:
					try:
						driver.find_element(by=By.XPATH, value='//div[@aria-label="Seguimiento franja"]').click()									
						break
					except :								
						time.sleep(1)
						gs+=1
			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print("y",Nomb_error)
		Gestion()

		def Notas():
			gs=0
			while gs<3:
				try:								
					elemento = driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_DESP_Notas Gestion"]')
					#elemento.send_keys(resulting_string.strip().replace("\n","").replace("\t",""))
					acciones = ActionChains(driver)
					acciones.move_to_element(elemento).click()
					acciones.send_keys(Keys.END)
					acciones.send_keys("\n" + resulting_string.strip()).perform()
					#driver.execute_script('arguments[0].value = arguments[1];', elemento, resulting_string)
					break
				except Exception as e:
					print(e)
					gs+=1
					time.sleep(0.5)

		Notas()

		 # aliado
		self.SalidaConfirmacion()



	def SalidaConfirmacion(self):
		self.EsperasTitulos('Despacho.')
		element=self.driver.find_element(By.XPATH,'//*[@type="submit" and contains(text(),"OK")]')
		self.driver.execute_script("arguments[0].scrollIntoView();", element)
		element.click()								
		#self.EsperasTitulos('Backoffice - Oracle Field Service')
		#self.driver.find_element(By.XPATH,'//span[contains(text(),"Detalles de actividad")]').click()
		return 1


	def Salida(self):
		elemento=self.driver.find_element(By.XPATH,'//span[contains(text(),"Detalles de actividad")]')
		self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
		for i in range(1):
			try:
				elemento.click()
				break
			except Exception as e:
				print(e)
				time.sleep(0.5)
		print("salida!")
		#self.EsperasTitulos('Detalles de actividad - Oracle Field Service')
		#self.driver.find_element(By.XPATH,'//span[@class="app-button-title" and contains(text(),"Consola de despacho")]').click()
		#self.EsperasTitulos('Consola de despacho - Oracle Field Service')



					
				
