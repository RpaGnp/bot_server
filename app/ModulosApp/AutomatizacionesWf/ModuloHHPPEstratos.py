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

import datetime
from datetime import time as tm
from datetime import date
from datetime import datetime




from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime, timedelta
import datetime

from ..interaccionChrome import Botinteraccion,BotinteraccionMG
from ..ModelDataBase import ConectorDbMysql


#from funciones_varias import *
#from reloj_casio import *

def IngresoMain(driver):
	driver.get('http://moduloagenda.cable.net.co/Autentica/Redirecciona.php?Direccion=https://mglapp.claro.com.co/catastro-warIns/view/MGL/login&nuevaVentana=TRUE')	
	time.sleep(1)
	driver.find_element(by=By.XPATH,value='//input[@type="submit"]').click()		
	driver.switch_to.window(driver.window_handles[-1])
	#click en menu boton claro		
	driver.find_element(by=By.XPATH,value='//img[@class="logo_Claro"]').click()
	script="for (var i of document.getElementsByTagName('ul')){i.setAttribute('style','display:block')}"
	driver.execute_script(script)

def confIngreso(driver):
	driver.find_element(by=By.XPATH,value='//img[@class="logo_Claro"]').click()
	script="for (var i of document.getElementsByTagName('ul')){i.setAttribute('style','display:block')}"
	driver.execute_script(script)
	
	driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(by=By.XPATH,value='//a[@title="Generar OT de ejecucin"]'))
	time.sleep(1)
	driver.find_elements(by=By.XPATH, value='//a[@title="OT Pendientes Gestin"]')[0].click()

	driver.find_element(by=By.XPATH,value='//th[contains(text(),"Estado")]//input').clear()
	driver.find_element(by=By.XPATH,value='//th[contains(text(),"Estado")]//input').send_keys('Vt Hhpp - pte gestion')
	driver.find_element(by=By.XPATH,value='//h2[contains(text(),"Gestión de Ordenes de Trabajo")]').click()

	WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contenido"]/table/tbody/tr')))					

def Timer():
	#===================fecha==========================
    FechaHora = datetime.now()
    timey=FechaHora+timedelta(minutes = 10)
    minute=timey.strftime('%M')
    timex=timey.strftime('%d/%m/%Y')

    x=int(minute)
    for i in range(5):  
        if x%5==0:
            if x>=60:
                x=0
                hora=FechaHora+timedelta(hours=1)
                hora=hora.strftime('%H')
            else:                
                hora=timey.strftime('%H')   
            break
        else:
            x+=1

    return f"{timex} {hora}:{str(x).zfill(2)}:00"



def SelectorEsthhpp(self,idBot,idAct,Trabajo):
	driver=self.driver
	Bot=BotinteraccionMG(driver)
	
	if Trabajo=="Gestion estratos":
		driver.get("http://moduloagenda.cable.net.co/Autentica/Redirecciona.php?Direccion=https://mglapp.claro.com.co/Visitas_Tecnicas/Login&nuevaVentana=TRUE")
		#validar usuario
		driver.find_element(by=By.XPATH, value='//input[@value="..Autenticar_Usuario.."]').click()
		driver.switch_to.window(driver.window_handles[-1])

		
		driver.find_element(by=By.XPATH, value='//a[contains(text(),"- Gestion de Solicitudes")]').click()
		time.sleep(0.5)
		driver.find_elements(by=By.XPATH, value='//input[@value="VTCECTM" and @type="radio"]')[1].click()
		time.sleep(0.5)
		driver.find_elements(by=By.XPATH, value='//input[@type="submit" and @value="Gestionar"]')[0].click()
		time.sleep(1)
		#ingreso al formulario
		for i in ['//*[@type="radio" and @value="2"]','//*[@type="submit"]']:
			driver.find_element(by=By.XPATH, value=i).click()
			time.sleep(1)
		#listar lo pendiente col estado
		ArrayGestionadas=[]
		#delimitar el tiempo del Bot
		while datetime.datetime.now().time()<tm.fromisoformat("22:05:00"):
		#while datetime.datetime.now().time()<tm.fromisoformat("08:45:00"):
			try:
				ConFilas=len(driver.find_elements(by=By.XPATH,value='//*[@id="form1:solicitudes:tbody_element"]//tr'))
				ContadorSig=0
				for i,tr in enumerate(driver.find_elements(by=By.XPATH,value='//*[@id="form1:solicitudes:tbody_element"]//tr')):
					i=i+1
					ConectorDbMysql().RepActividad(idBot)
					cuenta=driver.find_element(by=By.XPATH,value='//*[@id="form1:solicitudes:tbody_element"]/tr[%s]/td[3]'%(i)).text					
					print(cuenta)
					#print(driver.find_element(by=By.XPATH, value='//*[@id="form1:solicitudes:tbody_element"]/tr[%s]/td[5]'%(i)).text)
					#print(driver.find_element(by=By.XPATH, value='//*[@id="form1:solicitudes:tbody_element"]/tr[%s]/td[1]//input'%(i)).get_attribute('value'))
					
					if driver.find_element(by=By.XPATH, value='//*[@id="form1:solicitudes:tbody_element"]/tr[%s]/td[5]'%(i)).text=="PENDIENTE"\
					 	and driver.find_element(by=By.XPATH, value='//*[@id="form1:solicitudes:tbody_element"]/tr[%s]/td[1]//input'%(i)).get_attribute('value')!="Gestionando..."\
					 	and cuenta not in ArrayGestionadas:					 	
						#notificar actividad

						driver.find_element(by=By.XPATH, value='//*[@id="form1:solicitudes:tbody_element"]/tr[%s]/td[1]//input'%(i)).click()
						time.sleep(1)
						driver.find_element(by=By.XPATH, value='//OPTION[@label="GESTION DE HHPP DE FORMA MANUAL"]').click()
						time.sleep(1)
						driver.find_element(by=By.XPATH, value='//input[@value="ACEPTAR"]').click()
						time.sleep(1)
						driver.find_element(by=By.XPATH, value='//a[@dojoattachpoint="domNode" and contains(text(),"SU SOLICITUD")]').click()
						ArrayGestionadas.append(cuenta)
						conn=ConectorDbMysql().GetConn()
						with conn.cursor() as cursor:
							print(idAct,cuenta)
							cursor.callproc("spr_ins_camesthhpp",args=(idAct,cuenta))
						conn.commit()
						conn.close()

						for yz in range(ContadorSig):
							Bot.Radar('//input[@value="Ant"]').click()
							ContadorSig=0
						#driver.find_element(by=By.XPATH, value='//input[@value="Ver Todas"]').click()
						#break

				#FUNCION PARA VER PAUSA O ELIMINACION DEL BOT
				Dato=ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES",[idBot]))
				#print(Dato[0])
				if Dato[0]!=None:
					if Dato[0]=="Pausar":
						while 1:
							ConectorDbMysql().RepActividad(idBot)
							time.sleep(3)                           
							Dato=ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES",[idBot]))
							print(Dato)
							if Dato[0]!=None:
								if  Dato[0]=="Reanudar":                                    
									ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTBOTGES",[idBot]))
									break
								elif Dato[0]=="Eliminar":
									ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT",[idBot,idAct,'Detenido por usuario']))									
									time.sleep(1)
									driver.quit()
									return
							elif Dato[0]=="Eliminar":
								ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT",[idBot,idAct,'Detenido por usuario']))								
								time.sleep(1)								
								driver.quit()
								return

					elif Dato[0]=="Eliminar":                       
						ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT",[idBot,idAct,'Detenido por usuario']))						
						time.sleep(1)
						try:
							driver.refresh()
							time.sleep(4)
							driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
							time.sleep(1)
							driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
							time.sleep(5)            
						except:pass
						driver.quit()
						return
				else:
				    pass				
				
				
				time.sleep(5)
				if ConFilas<15:				
					driver.find_element(by=By.XPATH, value='//input[@value="Ver Todas"]').click()
					time.sleep(30)
				else:
					ContadorSig+=1
					Bot.Radar('//input[@value="Sig"]').click()				

								
					#driver.find_element(by=By.XPATH, value='//input[@value="Ver Todas"]').click()
			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)
				driver.quit()
				return
		if datetime.datetime.now().time()<tm.fromisoformat("22:05:00"):
			ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT",[idBot,idAct,'Detenido por horario']))				
		time.sleep(1)								
		driver.quit()
		return


	elif Trabajo=="Gestion estratos MER":
		IngresoMain(driver)
		driver.find_element(by=By.XPATH,value='//a[@title="Gestin solicitud."]').click()
		time.sleep(2)
		#integracion con la tabla
		driver.find_element(by=By.XPATH,value='//option[@value="2" and contains(text(),"CAMBIO ESTRATO")]').click()
		
		for i in driver.find_elements(by=By.XPATH,value='//*[@class="solicitudesGTable"]//tr[contains(@class,"solicitudes")]'):
			if driver.find_elements(by=By.XPATH,value='//*[@id="formPrincipal:solicitudDthList"]/tbody/tr[%s]/td[7]'%(i)).text =="PENDIENTE" and \
				driver.find_elements(by=By.XPATH, value='//*[@id="formPrincipal:solicitudDthList"]/tbody/tr[%s]/td[1]'%(i)).get_attribute('value')=="Gestionar":
				cuenta=driver.find_elements(by=By.XPATH, value='//*[@id="formPrincipal:solicitudDthList"]/tbody/tr[%s]/td[3]'%(i)).text

				driver.find_elements(by=By.XPATH,value='//*[@id="formPrincipal:solicitudDthList"]/tbody/tr[%s]/td[1]'%(i)).click()

				# dentro del formulario


	elif Trabajo=="Gestion ots HHPP":
		try:
			IngresoMain(driver)
			Bot.ScrollTo('//a[@title="Generar OT de ejecucin"]')			
			time.sleep(1)
			driver.find_elements(by=By.XPATH, value='//a[@title="OT Pendientes Gestin"]')[0].click()

			Bot.Radar('//th[contains(text(),"Estado")]//input').clear()
			Bot.Radar('//th[contains(text(),"Estado")]//input').send_keys('Vt Hhpp - pte gestion')
			Bot.Radar('//h2[contains(text(),"Gestión de Ordenes de Trabajo")]').click()
			WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contenido"]/table/tbody/tr')))				
			time.sleep(3)
			ArrayGestion=[]
			while 1:				
				for i in range(1,len(Bot.Radares('//*[@id="contenido"]/table/tbody/tr'))):					
					idot=Bot.Radar('//*[@id="contenido"]/table/tbody/tr['+str(i)+']/td[2]')				
					print(idot.text)
					if "Gestionando..." not in idot.text:
						WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contenido"]/table/tbody/tr['+str(i)+']/td[2]/a')))										
						
						driver.execute_script("arguments[0].scrollIntoView();", Bot.Radar('//*[@id="contenido"]/table/tbody/tr['+str(i)+']/td[2]/a'))
						if i not in ArrayGestion:
							while 1:
								try:								
									Bot.Radar('//*[@id="contenido"]/table/tbody/tr['+str(i)+']/td[2]/a').click()
									break
								except Exception as e:						
									#print(e)
									time.sleep(5)
						else:
							continue
						#dentro del formulario
						ArrayGestion.append(idot)
						Bot.Radar('//*[@id="tabs"]/li[2]/a[@title="Visita Tcnica"]').click()					
						#si la tabla no existe devolverse y continuar con el siguiente
						# si no hya tabla then notas nueva-
						#descripcion Error, TIPO NOTA -NOTAS HHPP, 
						html=driver.find_element(By.XPATH,'//*[@id="subcontent"]')
						if "Historial Visitas Tcnicas" not in html.text:
							#llamar salida
							confIngreso(driver)
							break


						link=Bot.Radar('//*[@class="constructGTableEvenRow"]/td/a')					
						link.click()

						Bot.Radar('//a[@title="hhpp"]').click()
						WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//input[@name="formVt:btnGenerarHhPp"]')))
						driver.execute_script("arguments[0].scrollIntoView();", Bot.Radar('//input[@name="formVt:btnGenerarHhPp"]'))
						
						Bot.Radar('//input[@name="formVt:btnGenerarHhPp"]').click()
						WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="white_contentError"]')))
						Bot.Radar('//a[@id="cerrarMensajeErrorBtn"]').click()
						time.sleep(1)
						driver.execute_script("arguments[0].scrollIntoView();", Bot.Radar('//input[@value="Regresar OT"]'))
						Bot.Radar('//input[@value="Regresar OT"]').click()
						time.sleep(1)
						Bot.Radar('//option[contains(text(),"VT HHPP - VISITA OK")]').click()
						time.sleep(0.5)
						# construir fecha y hora						

						Bot.Radar('//fieldset/table/tbody/tr[4]/td/span/span/input').send_keys(Timer())
						driver.execute_script("arguments[0].scrollIntoView();", Bot.Radar('//td[@data-handler="selectDay"]/a[contains(@class,"ui-state-highlight")]'))
						Bot.Radar('//td[@data-handler="selectDay"]/a[contains(@class,"ui-state-highlight")]').click()
						
						driver.execute_script("arguments[0].scrollIntoView();", Bot.Radar('//*/table/tbody/tr/td/input[@value="Actualizar"]'))
						Bot.Radar('//*/table/tbody/tr/td/input[@value="Actualizar"]').click()

						#alert de actualizacion
						WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="white_contentError"]')))
						Bot.Radar('//a[@id="cerrarMensajeErrorBtn"]').click()

						#pestaña notas					

						Bot.Radar('//*[@id="tabs"]/li/a[@title="Notas"]').click()
						Bot.ScrollTo('//input[@value="Nueva"]')
						Bot.Radar('//input[@value="Nueva"]').click()
						Bot.Radar('//tbody/tr/td/input[@maxlength="200"]').send_keys('hhpp creado')
						Bot.Radar('//option[contains(text(),"NOTAS HHPP")]').click()
						Bot.Radar('//textarea').send_keys('GNP YMR SE CREA HHPP SEGUN OT N° OT 245956, CUALQUIER NOVEDAD ENVIAR CORREO A SOPORTEHHPP@CLARO.COM.CO')
						Bot.ScrollTo('//input[@value="Guardar Nota"]')
						Bot.Radar('//input[@value="Guardar Nota"]').click()

						#alert
						WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="white_contentError"]')))
						Bot.Radar('//a[@id="cerrarMensajeErrorBtn"]').click()

						print("Fin")

						confIngreso(driver)					
				else:
					print("x",idot.text)
					continue
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)