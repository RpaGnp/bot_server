
#LIBRERIAS PARA CHROMEDRIVER***********************
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from datetime import datetime
from datetime import timedelta
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *


def login(driver,Usuario,Clave):	
	driver.get("https://agendamiento.claro.com.co")
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


#def SelectorAgendaDx(self,idbot,idAct,Trabajo):
def SelectorAgendaDx(self,idbot,idAct,Trabajo):
	driver=self.driver
	try:
		sql="SELECT ACB_CUSUAPL1,ACB_CCLAVEAPL1 from tbl_hactividadesbot where ACB_NID='"+str(idAct)+"'"
		Credenciales=array_datos=ConectorDbMysql().FuncGetInfo(1,sql)
		sql="""
				SELECT dx_nid,dx_corden,dx_caliado,dx_cciudad,dx_dfechaage,dx_cobservacion
				FROM tbl_hagndasdxrx
				WHERE dx_nidbot='"""+str(idAct)+"""' AND  dx_cestgestion='Pendiente';
			"""
		array_datos=ConectorDbMysql().FuncGetInfo(0,sql)		

		tomorrow = datetime.now() + timedelta(days=1)
		diaAgenda=tomorrow.strftime("%Y-%m-%d")	
		for data in array_datos:
			print(data)
			ConectorDbMysql().RepActividad(idbot)
			# funcion de salida, pausa del bot
			time.sleep(2)
			Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idbot]))
			# print(Dato[0])
			if Dato[0] != None:
				if Dato[0] == "Eliminar":
					ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Detenido por usuario']))
					driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
					time.sleep(1)					
					driver.quit()
					return
			else:
				pass


			driver.get('https://agendamiento.claro.com.co/MGW/MGW/Agendamiento/index.php')
			#ingreso consultar orden
			driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').click()
			driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').clear()
			driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').send_keys(data[1])
			time.sleep(1)
			driver.find_element(By.XPATH,'//input[@type="radio" and @value="O"]').click()
			time.sleep(1)
			driver.find_element(By.XPATH,'//input[@type="submit"]').click()
			#dentro de la orden

			if driver.find_element(By.XPATH,'//body').text=='ningun dato parametrizado':
				sql = ("spr_upd_estgesdx", [data[0], 'ningun dato parametrizado'])			
				ConectorDbMysql().FuncInsInfoOne(sql)
				continue


			try: 
				element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]')))
			except Exception as e:
				sql = ("spr_upd_estgesdx", [data[0], 'Error agendando ot'])			
				ConectorDbMysql().FuncInsInfoOne(sql)
				continue
				
			time.sleep(5)
			if driver.find_element(By.XPATH,'//div[@id="tipot"]').text=='No definido':
				sql = ("spr_upd_estgesdx", [data[0], 'Error agendando ot, tipo de trabajo no definido'])			
				ConectorDbMysql().FuncInsInfoOne(sql)
				continue

			if 'Esta orden no se puede agendar en workforce' in driver.find_element(By.XPATH,'//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]').text:
				sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada, Esta orden no se puede agendar en workforce'])			
				ConectorDbMysql().FuncInsInfoOne(sql)
				continue
			
			EstadoOt=driver.find_element(By.XPATH,'//div[@id="estadoag"]').text
			if EstadoOt != 'NO AGENDADO':								
				sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendable {EstadoOt}'])
				ConectorDbMysql().FuncInsInfoOne(sql)				
				continue
			else:pass

			driver.find_element(By.XPATH,'//div[@id="visita_menu"]').click()


			'''DicGral = {}
			for i, value in enumerate(driver.find_elements(by=By.XPATH, value='//div[@id="visita"]//table/tbody/tr')):
				i += 1
				if i == 1:
					continue
				for x in range(2):
					try:
						DicGral.update({driver.find_elements(by=By.XPATH,value='//div[@id="visita"]//table/tbody/tr[' + str(
																 i) + ']/th')[x].text: driver.find_elements(by=By.XPATH,
																											value='//div[@id="visita"]//table/tbody/tr[' + str(
																												i) + ']/td')[
							x].text})
					except:
						pass'''

			'''validar agendamiento
												si es fecha anterior  reagendar
												si es hoy o futuro, dejar'''


			#recorredor capacidad
			def Recorredorcapacidad():
				#================recorre la capacida mostrada por filas y columnas==============
				EstadoAgedar = False
				dicCapacidad = {}
				#tim = timer()
				#HoraActual =  datetime.strptime(tim[1], "%H:%M:%S").time()
				#FechaActual = datetime.strptime(tim[3], '%d/%m/%Y')

				conFilas=len(driver.find_elements(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr'))
				conCeldas =len(driver.find_elements(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody/tr[%s]/td'%conFilas))
				
				for celda in range(2,conCeldas):											
					for fila in range(1,conFilas):
						xpath='//*[@id="semana_calendario_capacity"]/table/tbody/tr['+str(fila)+']/td['+str(celda)+']'	
						elemento=driver.find_element(By.XPATH,xpath)					
						diacupo=elemento.get_attribute('data-date')
						cancupos=elemento.text				
						cancupos=int(cancupos.split(" ")[0])													
						if cancupos > 0 :# and datetime.now().time() < limite_hora:					
							#if datetime.strptime(diacupo, '%Y-%m-%d') == FechaActual and HoraActual <= datetime.strptime('12:00:00', "%H:%M:%S").time():
							EstadoAgedar=True
							driver.find_element(By.XPATH,xpath).click()
							return True
							#else:
							#	dicCapacidad[diacupo]=xpath
							#	EstadoAgedar=True						
				return EstadoAgedar







			DicButton={}
			VarAGenda=False
			for buttonAccion in driver.find_elements(By.XPATH,'//div[@class="buttons-form"]/input'):
				DicButton.update({buttonAccion.get_attribute("value"):buttonAccion.get_attribute("style")})					
				if buttonAccion.get_attribute("style")=='display: inline-block;' and  buttonAccion.get_attribute('value')=="Agendar":					
					buttonAccion.click()
					#driver.find_element(By.XPATH,'//button/span[contains(text(),"Aceptar")]').click()
					#llenar datos peronales
					def fillform():
						#//div[@id="confirmacion"]//table//tr//th[contains(text(),'Confirmación de la Visita')]
						ArrayDatos=[driver.find_element(By.XPATH,'//*[@id="mod_agenda"]/table/tbody/tr[4]/th/div[2]/div[2]').text,\
						"notiene@claro.com",'1234567890']#driver.find_element(By.XPATH,'//*[@id="confir_num_default"]').get_attribute('value')[2:-1]
						for i,j in enumerate(driver.find_elements(By.XPATH,"//input[contains(@style,'border: 1px solid red')]")):	
							j.clear()
							j.send_keys(ArrayDatos[i])
					
					
					continuarAgendando=False
					clases = driver.find_elements_by_css_selector("[class^='ui-dialog ']")					
					for clase in clases:
						if "display: block;" in clase.get_attribute("style"):
							ErrorOrden=clase.text							
							continuarAgendando=True
							

					if continuarAgendando:
						sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendable {ErrorOrden}'])
						ConectorDbMysql().FuncInsInfoOne(sql)															
						break
										
					#escoger color y fecha
					#diaAgenda="2023-05-03"

					EstadoCapacidad=driver.find_element(By.XPATH,'//*[@id="semana_calendario_capacity"]/table/tbody').text					
					if "No existe capacidad disponible para los intervalos" in EstadoCapacidad:
						sql = ("spr_upd_estgesdx", [data[0], f'Orden no agendable {EstadoCapacidad}'])
						ConectorDbMysql().FuncInsInfoOne(sql)	
						continue
					else:pass
					
					Recorredorcapacidad()
					'''try:
																					driver.find_elements(By.XPATH,'//tr//td[@data-date="'+str(diaAgenda)+'"]')[1].click()
																				except Exception as e:
																					print("]",e)
																					driver.find_elements(By.XPATH,'//tr//td[@data-date="'+str(diaAgenda)+'"]')[0].click()'''
					#wait
					
					element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//span[@id="ui-dialog-title-dialog_confirmacion_agenda"]')))
					time.sleep(1)
					driver.find_element(By.XPATH,'//button//span[contains(text(),"Confirmar")]').click()

					try:
						element = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"Agenda registrada correctamente")]')))
						driver.find_elements(By.XPATH,'//span[contains(text(),"Cerrar")]')[-1].click()
						
						sql = ("spr_upd_estgesdx", [data[0], 'Orden agendada con exito'])			
						ConectorDbMysql().FuncInsInfoOne(sql)
						VarAGenda=True
						login(driver,Credenciales[0].decode('utf-8'),Credenciales[1].decode('utf-8'))
					except Exception as e:
						try:				
							alert = driver.switch_to.alert
							time.sleep(1)				
							alert.accept()
							sql = ("spr_upd_estgesdx", [data[0], 'Orden agendada con exito'])			
							ConectorDbMysql().FuncInsInfoOne(sql)
							VarAGenda=True
							login(driver,Credenciales[0].decode('utf-8'),Credenciales[1].decode('utf-8'))							
						except Exception as e:
							print("*",e)							
					
					if VarAGenda==False:
						sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada'])			
						ConectorDbMysql().FuncInsInfoOne(sql)					
					break


				sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada'])
				ConectorDbMysql().FuncInsInfoOne(sql)
			

		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Labor Terminada']))		
		driver.quit()
	except Exception as e:
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print(Nomb_error)
		try:
			sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada error ot'])
			ConectorDbMysql().FuncInsInfoOne(sql)
		except: pass
		driver.quit()