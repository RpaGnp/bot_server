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



from ..ModelDataBase import ConectorDbMysql


from funciones_varias import *
from reloj_casio import *

def FunGuardar(self,ArrayGestion):	
	ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTACTM",ArrayGestion))


def selector_Soporte(self,idBot,Idactividad):
	driver=self.driver
	try:
		compuerta=False
		Primera_ot=True
		lista_ejecucion=[]


		sql="""
			SELECT ACM_NID,ACM_CORDEN,ACM_CCUENTA,ACM_CMISELANEOS0
			FROM tbl_hactmarcacionbot
			WHERE ACM_NIDBOT='"""+str(Idactividad)+"""' AND  ACM_CESTADOOT='Pendiente';
		"""
		#print(sql)
		array_datos=ConectorDbMysql().FuncGetInfo(0,sql)
		for i,dato in enumerate(array_datos):
			data=[dato[0],dato[1],dato[3],dato[2]]
			del dato
			print(data)
			ConectorDbMysql().RepActividad(idBot)
			try:
				element = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toa-panel-content edtree"]')))
			except:pass
			#driver.find_element_by_xpath('//*[@id="action-global-search-icon"]').click()

			# refresh wf
			lista_ejecucion.append(1)
			if len(lista_ejecucion)==30:
				driver.refresh()
				time.sleep(10)
				lista_ejecucion=[]

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
							driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
							time.sleep(1)
							while 1:
								BtnSalida = self.driver.find_element_by_xpath(
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
					driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
					time.sleep(1)
					while 1:
						BtnSalida = self.driver.find_element_by_xpath(
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

			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="GlobalSearch"]')))
			lupa=driver.find_element_by_xpath('//*[@type="search"]')
			#print(lupa.is_displayed())
			if lupa.is_displayed()==False:
				driver.find_element_by_xpath('//*[@aria-label="GlobalSearch"]').click()
			else:
				pass

			driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
			driver.find_element_by_xpath('//*[@class="search-bar-input"]').clear()
			driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(data[1])
			driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(Keys.ENTER)

			try:
				element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta = False
				continue

			if driver.find_element_by_xpath('//*[@class="toa-search-empty"]').text != "":
				compuerta=False
				continue
			else:
				pass


			_fecha_hoy=fecha_actual(self)

			time.sleep(1)
			element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
			_lista_lls=driver.find_elements_by_xpath('//*[@class="found-item-activity"]')
			print("="*40,len(_lista_lls),"="*40)
			if len(_lista_lls)==0:
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta = False
				continue

			for i in range(len(_lista_lls)):
				gs=0
				while gs<5:
					try:
						fecha_Ot=driver.find_elements_by_xpath('//*[@class="activity-date"]')[i].text
						time.sleep(0.5)
						x=driver.find_elements_by_xpath('//*[@class="activity-icon icon"]')[i].get_attribute("style")
						break
					except:
						time.sleep(1)
						gs+=1

				if x=="background-color: rgb(30, 133, 37); border: 1px solid rgb(24, 106, 29);":
					if fecha_Ot==_fecha_hoy[0] or fecha_Ot=="":
						driver.find_elements_by_xpath('//*[@class="activity-title"]')[i].click()
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

			if compuerta==False:
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta=False
				continue
			else:
				pass

			if Primera_ot:
				try:
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="context-layout"]/div/div[1]/div[1]/div[1]/div/div[1]/header/span')))
				except:
					pass

			else:
				pass
			

			driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Backoffice")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
			#===================================== ingreso al formulario=============================================================
			element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button inline" and contains(text(),"Confirmación")]')))
			driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"CGE")]').click()
			WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))


			time.sleep(0.5)
			html=driver.find_element_by_xpath('//*[@id="content" and @class="content"]').text			
			if "CancelarOK" not in html:
				driver.back()
				time.sleep(2)
				driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
				FunGuardar(self,[data[0],"Confirmacion Fallida"])
				compuerta=False
				continue
				

			tokens=[]
			def AliadoVentasTecnicas():
				try:
					if driver.find_element_by_xpath('//*[@data-label="BACK_CGE_Aliado_Vte"]').get_attribute("value")!="1":
						for i in driver.find_elements_by_xpath('//*[@value="1" and contains(text(),"GNP")]'):
							i.click()
					else:
						pass
				except:
					pass

			AliadoVentasTecnicas()

			def CausaSoporteInterno():
				if driver.find_element_by_xpath('//*[@data-label="BACK_CGE_Causa Soporte In"]').get_attribute("value")!="CSIN02":
					driver.find_element_by_xpath('//*[@value="CSIN02" and contains(text(),"Seguimiento VIP")]').click()
				else:
					pass
			CausaSoporteInterno()


			def AliadoCGOCGE():
				if driver.find_element_by_xpath('//*[@data-label="BACK_CGE_Aliado CGO"]').get_attribute("value")!="GNP":
					Id=driver.find_element_by_xpath('//*[@data-label="BACK_CGE_Aliado CGO"]').get_attribute("id")
					xpath='//*[@id="'+str(Id)+'"]/option[3]'
					driver.find_element_by_xpath(xpath).click()

			AliadoCGOCGE()

			def Notas():
				driver.find_element_by_xpath('//*[@data-label="BACK_CGE_Notas Causa Soporte In"]').send_keys('ok')
				
			Notas()


			def GestionSopoInterno():				
				try:
					element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,\
					 '//*[@data-label="BACK_CGE_Gestion Soporte In"]')))
					if driver.find_element_by_xpath('//*[@data-label="BACK_CGE_Gestion Soporte In"]').get_attribute("value")!="DSIN05":
						driver.find_element_by_xpath('//*[@value="DSIN05"]').click()
					else:
						pass					
					
				except:
					time.sleep(1)
					

			GestionSopoInterno()  # aliado

			def NotasFin():				
				try:
					driver.find_element_by_xpath('//*[@data-label="BACK_CGE_Notas Gestion Soporte In"]').send_keys('ok')
					
				except:					
					time.sleep(0.5)
			NotasFin()


			driver.find_element_by_xpath('//*[@type="submit" and contains(text(),"OK")]').click()
			try:
				WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class=""loading-animated-icon big jbf-init-loading-indicator""]')))
			except:
				pass


			x=0
			while x<5:
				try:
					driver.find_element_by_xpath('//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
					break
				except:pass
				
					
			


			Primera_ot=True

			sql = ("SPR_UPD_ESTACTM", [data[0], 'Ot marcada con exito'])
			ConectorDbMysql().FuncInsInfoOne(sql)
			# si aparece la ventana de confirmacion darle continuar********************************************
			time.sleep(0.5)
		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))
		driver.quit()
		
	except Exception as e:
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print(Nomb_error)		
		try:
			driver.refresh()
			time.sleep(3)
			driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
			time.sleep(1)
			while 1:
				BtnSalida = self.driver.find_element_by_xpath('//*[@class="item-caption __logout __logout"]')
				if BtnSalida.is_displayed():
					BtnSalida.click()
					time.sleep(3)
					break
				else:
					pass
		except:pass
		try:
			driver.quit()
		except:pass