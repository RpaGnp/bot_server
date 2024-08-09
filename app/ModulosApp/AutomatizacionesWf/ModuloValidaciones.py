import time
import csv
import sys
import os
from datetime import date
from datetime import datetime
import tempfile


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
from selenium.webdriver.firefox.service import Service

from ..ModelDataBase import ConectorDbMysql
from .InteraccionChrome import BotChrome, ExtractorEstadoOrden
from .ModuloValidacionesAgenda import SelectorValidacionesAgenda
from funciones_varias import *


def Actualizacion(self,driver,ArrayGestion):
	#modulo validaciones agenda									...						
	for i in ArrayGestion:		
		##driver.switch_to.window(self.vprincipal)
		#if len(driver.window_handles)<=self.ContadorPesatañas:
		#driver.execute_script("window.open('');")
		#driver.execute_script("window.focus();")
		#driver.switch_to.window(driver.window_handles[-1])						
		time.sleep(1)
		driver.get('http://moduloagenda.cable.net.co/MGW/MGW/Agendamiento/index.php')
		driver.find_element(by=By.XPATH, value='//*[@name="TBorden"]').send_keys(i[2].split("_")[0])
		
		if str(i[3]).upper() in ['MANTENIMIENTO FTTH','MANTENIMIENTOS ALTO VALOR',"ARREGLOS"]:
			driver.find_element(by=By.XPATH, value='//*[@for="Rbot-L" and contains(text(),"Llamada de servicio")]').click()
		else:
			driver.find_element(by=By.XPATH, value='//*[@for="Rbot-O" and contains(text(),"Orden de Trabajo")]').click()
		
		time.sleep(1)
		driver.find_element(by=By.XPATH, value='//*[@type="submit" and @value="Consultar"]').click()
		SelectorValidacionesAgenda(self,driver,i)
			#print("continue"	)

		#while len(driver.window_handles) >1:						                  
		#driver.switch_to.window(driver.window_handles[1])						
		try:
			xpath='//*[contains(text(),"La acción se realizo correctamente")]'
			element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
			driver.find_element(by=By.XPATH, value='//*[@class="ui-icon ui-icon-closethick" and contains(text(),"Cerrar")]').click()
			#driver.close()
		except:						
			pass
			##driver.close()

def selector_ValidacionesMg(self,idbot,idAct,TipoTrabajo):
	driver=self.driver
	self.ContadorPesatañas=5	
	try:
		BotInteraccion=BotChrome(driver)
		BotExtractor=ExtractorEstadoOrden(driver)
		data=ConectorDbMysql().FuncGetInfoOne(2,"SPR_GET_ACTVAL",[idAct])		#5861
		ArrayGestion=[]		
		##self.vprincipal = driver.current_window_handle
		for index,row in enumerate(data):			
			time.sleep(1)
			ConectorDbMysql().RepActividad(idbot)
			if int(row[1])==0:
				break
			print("!"*30,row)			
			ArrayGestion.append(row)			
			#pausa del bot			
			 
			Dato = ConectorDbMysql().FuncGetInfoOne(1,"SPR_GET_ESTBOTGES",[idbot])[0]
			if Dato!=None or Dato!='En labor':
				if GetContBotMG(Dato,idbot,idAct) == False:
					driver.quit()
					return
				else:pass
			else:pass
			
			# print(Dato[0])
			if TipoTrabajo in ["Repara y Actualiza","Reparar"]:
				#modulo e reparaciones
				#print("="*30,len(ArrayGestion),"=",self.ContadorPesatañas)
				#if len(ArrayGestion)<=self.ContadorPesatañas:
				#driver.execute_script("window.open('');")
				#driver.execute_script("window.focus();")
				#driver.switch_to.window(driver.window_handles[-1])
				
				driver.get("http://moduloagenda.cable.net.co/Interfaces/AprovisionamientoServicios/index.php")
				BotInteraccion.DiligenciarTexbox('//*[@name="cuenta"]',row[1])
				BotInteraccion.ClickElemento('//*[@name="consultar"]')
				time.sleep(2)

				cuadrocarga=driver.find_element(By.XPATH,'//div[@id="loading_msj"]')
				ruedacarga=driver.find_element(By.XPATH,'//img[@src="../../image/ajax-loader.gif"]')
				while cuadrocarga.is_displayed() or ruedacarga.is_displayed():
					time.sleep(5)

				Arraydata=BotExtractor.ExtraerServicios()
				print("**",Arraydata)
				if Arraydata==0:
					#driver.close()
					#driver.switch_to.window(self.vprincipal)
					conn=ConectorDbMysql().GetConn()
					cursor=conn.cursor()
					cursor.callproc("SPR_UPD_OTNOGES",[row[0]])
					conn.commit()
					cursor.close()
					conn.close()
					continue
				Arraydata.insert(0,row[0])
				while len(Arraydata)>15:
					Arraydata.pop(-1)										

				print("!",Arraydata)
				conn=ConectorDbMysql().GetConn()
				cursor=conn.cursor()				
				cursor.callproc("SPR_UPD_ESTOTIN",args=(Arraydata))
				conn.commit()
				cursor.close()
				conn.close()
				#BotInteraccion.ClickElementos('//*[@name="validarServicios"]',1)
				#print("!",Arraydata)
				#print("adentro ",'Cancelado/debiendo' in Arraydata)
				if "CREAR" in Arraydata  or "MODIFICAR" in Arraydata or "BORRAR" in Arraydata:# or "OK" in Arraydata:
					if 'Cancelado/debiendo' in Arraydata:
						#print("adentro ",'Cancelado/debiendo' in Arraydata)
						#driver.close()
						#driver.switch_to.window(self.vprincipal)
						conn=ConectorDbMysql().GetConn()
						cursor=conn.cursor()
						cursor.callproc("SPR_UPD_OTNOGES",[row[0]])
						ArrayGestion.remove(row)
						conn.commit()
						cursor.close()
						conn.close()
						continue
					else:
						pass

					driver.find_element(by=By.XPATH, value='//*[@name="validarServicios" and @value="Reparar todos los Servicios @+tel"]').click()
					
					iterador=1
					while iterador<3:
						try:
							alert_obj = driver.switch_to.alert
							#alert_obj = driver.switch_to.alert
							alert_obj.accept()
							break
						except:
							iterador+=1
							time.sleep(1)
					#continue

				

				else:
					Arraydata=BotExtractor.ExtraerServicios()
					#Arraydata.insert(0,driver.find_elements(by=By.XPATH, value='//*[@class="valor_validar"]')[0].text)				
					Arraydata.insert(0,row[0])
					ArraySerActualizados=[Arraydata[0],Arraydata[10],Arraydata[11],Arraydata[12],Arraydata[13],Arraydata[14],"Servicios OK no se envia reparacion"]
					del Arraydata
					print("*"*30,ArraySerActualizados)

					conn=ConectorDbMysql().GetConn()
					cursor=conn.cursor()
					cursor.callproc("SPR_UPD_OTNOAPTGES",ArraySerActualizados)			
					conn.commit()
					cursor.close()
					conn.close()
					#GestorSqlite().UpdValidacion(ArraySerActualizados)
					time.sleep(1)
					ArrayGestion.remove(row)
					#driver.close()
					#driver.switch_to.window(self.vprincipal)
					continue
				

				#salida validacion
				#if len(ArrayGestion)==self.ContadorPesatañas:	
					#while len(driver.window_handles) >1:
						#print(ArrayGestion)
						#for i in range(len(ArrayGestion)):
						#print(i)
						#try:                    
						#driver.switch_to.window(driver.window_handles[1])
				try:
					element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ContainerDebug"]')))
				except:
					element = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContainerDebug"]')))
				
				resultado=driver.execute_script("return document.querySelector('#ContainerDebug').innerText")
				print("Resultado: ",resultado)
				#resultado=driver.find_element(by=By.XPATH, value='//*[@class="ui-dialog-content ui-widget-content"]').text
				
				driver.implicitly_wait(0)
				WebDriverWait(driver, 600).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="loading_time"]')))
				
				BotInteraccion.ClickElemento('//*[@name="consultar"]')
				time.sleep(3)
				Arraydata=BotExtractor.ExtraerServicios()
				
				#Arraydata.insert(0,driver.find_elements(by=By.XPATH, value='//*[@class="valor_validar"]')[0].text)				
				Arraydata.insert(0,row[0])
				
				ArraySerActualizados=[Arraydata[0],Arraydata[10],Arraydata[11],Arraydata[12],Arraydata[13],Arraydata[14],resultado]
				print("Servicios actualizados: ",ArraySerActualizados)
				del Arraydata
				conn=ConectorDbMysql().GetConn()
				cursor=conn.cursor()			
				cursor.callproc("SPR_UPD_OTNOAPTGES",ArraySerActualizados)
				conn.commit()
				cursor.close()
				conn.close()
				time.sleep(1)
				#driver.close()
				
					
				#else:
				#	pass

				if TipoTrabajo == "Repara y Actualiza":
					Actualizacion(self,driver,ArrayGestion)
					ArrayGestion=[]
				else:
					continue
					
				
				##driver.switch_to.window(self.vprincipal)
				ArrayGestion=[]
			
			elif TipoTrabajo in ["Extraer Agenda"]:
				driver.execute_script("window.open('');")
				driver.execute_script("window.focus();")
				driver.switch_to.window(driver.window_handles[-1])

				driver.get("http://moduloagenda.cable.net.co/MGW/MGW/Agendamiento/index.php")				
				time.sleep(1)
				driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').click()
				driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').clear()
				driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').send_keys(row[2])


				if row[3].lower()=="mantenimientos":
					driver.find_element(By.XPATH,'//input[@type="radio" and @value="L"]').click()
				else:
					driver.find_element(By.XPATH,'//input[@type="radio" and @value="O"]').click()
				time.sleep(0.5)
				driver.find_element(By.XPATH,'//input[@type="submit"]').click()

				try: 
					element = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]')))
				except Exception as e:
					print("no carga pagina",e)


			else:
				#if len(ArrayGestion)==self.ContadorPesatañas:					
				Actualizacion(self,driver,ArrayGestion)
				ArrayGestion=[]
					
		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Labor Terminada']))		
		time.sleep(1)					
		driver.quit()
		
		try:			
			cursor.close()
			conn.close()
		except:pass
		
	except Exception as e:
		driver.quit()
		Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print("! error conexion: ", e, Nomb_error)		