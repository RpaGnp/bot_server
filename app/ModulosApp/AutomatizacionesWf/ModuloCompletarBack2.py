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
from .ModuloCompletarWF.Completa import GestionCompletar
from funciones_varias import *
from reloj_casio import *

#

def selectorComBack(self,idBot,Idactividad):
	try:
		driver=self.driver
		element = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toaGantt-tb toaGantt-tb-name"]')))		
		
		ArrayGestion=len(driver.find_elements(By.XPATH,'//DIV[@class="grid-content"]//DIV[@class="grid-row pointer"]//div[@style="background-color: rgb(255, 255, 38);"]//following-sibling::div//span[@class="grid-identifier"][2]'))
		lista_refresh=[]
		#ContadorReinicio=0
		# ==========verificar si hay ots pendientes==========
		ArrayInciadas = driver.find_elements(by=By.XPATH, value='//*[@data-activity-status="started"]')
		ArrayPendiente=driver.find_elements(by=By.XPATH, value='//*[@data-activity-status="pending"]')
		diccionario={}		
		if len(ArrayInciadas)!=0:
			ArrayPendiente.append(ArrayInciadas[0])		

		sql="SELECT  ACP_ORDEN from tbl_hactcompletarbot where ACP_NIDAC=%s and ACP_CESTGES='Pendiente'"%Idactividad			
		ArrayOtsDb=list(ConectorDbMysql().FuncGetInfo(0,sql))			
		ArrayOtsToCom=[dato[0] for dato in ArrayOtsDb]		
		del ArrayOtsDb
		
		diccionario={}			
		for i in reversed(ArrayPendiente):			
			x=i.get_attribute("aid")
			y=i.get_attribute("aria-label")				
			diccionario.update({str(x):str(y)})
			if x not in ArrayOtsToCom:
				ConectorDbMysql().FuncInsInfoOne(("SPR_INS_ACTCOMP",[Idactividad,x]))	
					
		time.sleep(2)		
		compuerta=True
		ContadorRF=0
		for numero_ot,tipo_ot in diccionario.items():								            							
			print("*"*40,numero_ot," ",tipo_ot,"*"*40)
			try:					
				driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			except:pass
			ConectorDbMysql().RepActividad(idBot)
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
			lupa=driver.find_element(by=By.XPATH, value='//*[@type="search"]')				
			time.sleep(0.5)
			if lupa.is_displayed()==False:					
				driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()							
			else:pass

			driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
			time.sleep(0.5)
			driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(numero_ot)
			driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)						
			time.sleep(1)			

			if "pending regular " in tipo_ot :
				element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="found-item-activity"]')))					
				time.sleep(0.5)
				gs=0
				while gs<10:
					try	:				
						_estado=driver.find_elements(by=By.XPATH, value="//*[@aid="+str(numero_ot)+"]")							
						estatus_orden=_estado[1].get_attribute("style")														
						break
					except:
						time.sleep(0.5)						
						gs+=1

				#x=driver.find_element(by=By.XPATH, value="/html/body/div[15]/div[1]/div[1]/div[2]/div[1]/table/tr/td[1]/div")					
				if estatus_orden=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);":						
					for i in driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]'):											
						if 'Backlog' in i.text:
							i.click()
							
					
					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

					#driver.find_element(by=By.XPATH, value='//*[@class="toa-search-identifier" and contains(text(),"Backoffice")]').click()
					compuerta=True
				else:
					compuerta=False												
					continue
				# dentro de la orden para iniciarla
				element2= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Información Actividad"]')))
				time.sleep(0.5)

				orden=int(str(driver.find_element(By.XPATH,'//input[@aria-label="OT No.:"]').get_attribute("value")).split("_")[0])
				arraydetallesot=ConectorDbMysql().FuncGetSpr(1,'spr_get_otcombac',[Idactividad,orden])

				driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Iniciar")]').click()


				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
				time.sleep(0.5)
				element2= WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and @class="button submit" and contains(text(),"OK")]')))


				driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
				try:						
					if driver.find_element(by=By.XPATH, value='//*[@class="popup-window-slot"]//div[@class="redwood-dialog__content"]').is_displayed():
						driver.find_element(by=By.XPATH, value='//*[@class="button submit" and contains(text(),"Continuar")]').click()

				except:
					pass

				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
				#salida
				
				x=0
				while x<5:
					try:
						driver.find_element(by=By.XPATH, value='//span[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
						break
					except:
						time.sleep(0.5)
						x+=1
					
				#ENTRARA A LA ORDEN YA INICIADA
				gs=0
				while gs<5:
					try:
						driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(numero_ot)
						driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)
						break
					except Exception as e:
						Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e							
						time.sleep(1)
						gs+=1
				
				for i in driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]'):						
					if 'Backlog' in i.text:
						i.click()
								
				

				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
						
				time.sleep(0.5)
				l=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
				for i in l:											
					if 'Backlog' in i.text:
						i.click()
					else:
						print("tipo de orden no admitida: ",i.text )
					


				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
								
				if driver.title!="Detalles de actividad - Oracle Field Service":
					driver.refresh()
					time.sleep(5)
					driver.find_element(by=By.XPATH, value='//*[@aria-label="GlobalSearch"]').click()
					driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').clear()
					driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(numero_ot)
					driver.find_element(by=By.XPATH, value='//*[@class="search-bar-input"]').send_keys(Keys.ENTER)
					time.sleep(1)
					l=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')					
					for i in l:							
						if 'Backlog' in i.text:
							i.click()
						else:
							print("tipo de orden no admitida: ",i.text )
					del l				
				#driver.find_element(by=By.XPATH, value='//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')
				element2= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Información Actividad"]')))

				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

				BotGESTION=GestionCompletar(driver,arraydetallesot)
				BotGESTION.NotasBack()
				BotGESTION.Finalizar()
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTGESCOM",[Idactividad,numero_ot,'Ot Completada']))

				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

			elif "started regular " in tipo_ot:					
				time.sleep(0.5)									
				element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="found-item-activity"]')))
				time.sleep(0.5)
				gs=0
				while gs<10:
					try	:				
						_estado=driver.find_elements(by=By.XPATH, value="//*[@aid="+str(numero_ot)+"]")
						estatus_orden=_estado[1].get_attribute("style")
						break
					except:
						time.sleep(0.5)						
						gs+=1
				#x=driver.find_element(by=By.XPATH, value="/html/body/div[15]/div[1]/div[1]/div[2]/div[1]/table/tr/td[1]/div")					
				if estatus_orden=="background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);" or estatus_orden=="background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);":
					l=driver.find_elements(by=By.XPATH, value='//*[@class="found-item-activity"]')
					for i in l:
						try:									
							if 'Backlog' in i.text:
								i.click()
							else:
								print("tipo de orden no admitida: ",i.text )
						except Exception as e:
							print(e)
					driver.implicitly_wait(0)
					WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

					#driver.find_element(by=By.XPATH, value='//*[@class="toa-search-identifier" and contains(text(),"Backoffice")]').click()
					compuerta=True
				else:
					compuerta=False												
					continue
				
				element2= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Información Actividad"]')))

				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

				orden=int(str(driver.find_element(By.XPATH,'//input[@aria-label="OT No.:"]').get_attribute("value")).split("_")[0])
				
				arraydetallesot=ConectorDbMysql().FuncGetSpr(1,'spr_get_otcombac',[Idactividad,orden])
				
				BotGESTION=GestionCompletar(driver,arraydetallesot)
				BotGESTION.NotasBack()
				BotGESTION.Finalizar()
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTGESCOM",[Idactividad,numero_ot,'Ot Completada']))

				driver.implicitly_wait(0)
				WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

			x=0
			while x<7:
				try:
					driver.find_element(by=By.XPATH, value='//*[@class="page-header-title" and contains(text(),"Consola de despacho")]')
					break
				except:
					time.sleep(1)
					x+=1
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
		Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print("! error conexion: ", e, Nomb_error)
		driver.quit()
		
				
				#