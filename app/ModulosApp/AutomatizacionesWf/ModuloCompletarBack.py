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
from funciones_varias import *
from reloj_casio import *



def selectorComBack(self,idBot,Idactividad):
	try:
		driver=self.driver	
		self.TipoOt=1

		def clic(xpath):
			driver.find_element(By.XPATH,xpath).click()

		def write(xpath,Words):
			driver.find_element(By.XPATH,xpath).clear()
			driver.find_element(By.XPATH,xpath).send_keys(Words)

		def Iniciar():
			driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Iniciar")]').click()			
			time.sleep(1)
			driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
			time.sleep(1)


		def Completar(arraycon):
			x=0
			while x<=3:
				try:
					driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Completar")]').click()
					break
				except Exception as e:				
					time.sleep(1)
					x+=1
			#cerraralerts()
			clic('//input[@class="form-item dropdown-value"]')
			if self.TipoOt==1:
				clic('//div[@aria-label="Escalado a otras areas"]')
			else:
				clic('//div[@aria-label="Escalado a otras areas"]')
			
			driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
			try:
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTGESCOM",[Idactividad,orden,'Ot Completada']))		
			except Exception as e:
				print(e)
		#def selectorComBack(driver):


		def Razonar(arraydatos):
			x=0
			while x<=3:
				try:
					driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Razón")]').click()
					break
				except Exception as e:				
					time.sleep(1)
					x+=1

			clic('//*[@id="context-layout"]/div/div/div/div[5]/div/div/div/div[1]/div/div/div')
			time.sleep(0.5)
			clic('//div[@aria-label="CONTINUA GESTION BACKLOG"]')
			time.sleep(0.5)
			write('//textarea[@aria-label="Notas"]',arraydatos[2].strip())
			time.sleep(0.5)
			driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
			try:		
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTGESCOM",[Idactividad,orden,'Ot razonada']))		
			except Exception as e:
				print(e)


		def cerraralerts():			
			#driver.execute_script('document.querySelector(".panel-notification").setAttribute("style","display:none")')
			pass





		try:
			btnverMas=driver.find_element(By.XPATH,'//div[@class="btn-pagination-button"]//button')
			btnverMas.is_displayed()
			while btnverMas.is_displayed:
				try:
					btnverMas.click()
					time.sleep(1)
					#cerraralerts()
				except:
					break
		except:
			pass
		#cerraralerts()##
		
		#comprobar iniciada
		if len(driver.find_elements(By.XPATH,'//DIV[@class="grid-content"]//DIV[@class="grid-row pointer"]//div[@style="background-color: rgb(167, 209, 0);"]'))!=0:
			xpathini='//div[@class="grid-content"]//div[@class="grid-row pointer"]//div[@style="background-color: rgb(167, 209, 0);"]//following-sibling::div//span[@class="grid-identifier"][2]'
			orden=None
			orden=int(driver.find_element(By.XPATH,xpathini).text.split("_")[0])			
			arraydetallesot=ConectorDbMysql().FuncGetSpr(1,'spr_get_otcombac',[Idactividad,orden])
			clic(xpathini)
			if arraydetallesot==None:
				#Iniciar()
				Razonar([9999,orden,"Razon Backlog"])
			else:
				print("!",orden,arraydetallesot)				
				#driver.find_elements(By.XPATH,'//DIV[@class="grid-content"]//DIV[@class="grid-row pointer"]//div[@style="background-color: rgb(167, 209, 0);"]')[0].click()
				
				if arraydetallesot[1] in ('COMPLETADA'):					
					Completar(arraydetallesot)	
				else:
					Razonar(arraydetallesot)
			
		else:
			pass
			
		ArrayGestion=len(driver.find_elements(By.XPATH,'//DIV[@class="grid-content"]//DIV[@class="grid-row pointer"]//div[@style="background-color: rgb(255, 255, 38);"]//following-sibling::div//span[@class="grid-identifier"][2]'))
		for i in range(ArrayGestion):			
			OrdenGestion=ConectorDbMysql().FuncGetSpr(1,'spr_get_couotscom',[Idactividad])
			print(OrdenGestion)
			if OrdenGestion==0:
				break

			print(i,"\\",ArrayGestion)
			WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//h1[@title="Lista de actividades"]')))
			ConectorDbMysql().RepActividad(idBot)
			Dato = ConectorDbMysql().FuncGetInfoOne(1,"SPR_GET_ESTBOTGES",[idBot])[0]            
			if Dato!=None or Dato!='En labor':
			    if GetContBotWF(Dato,idBot,Idactividad) == False:
			        driver.refresh()
			        time.sleep(4)
			        driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
			        time.sleep(1)
			        driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
			        time.sleep(2)
			        driver.quit()
			        ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
			        return
			    else:pass
			else:pass

			xpathini='//div[@class="grid-content"]//div[@class="grid-row pointer"]//div[@style="background-color: rgb(255, 255, 38);"]//following-sibling::div//span[@class="grid-identifier"][2]'				
			orden=None
			orden=int(driver.find_element(By.XPATH,xpathini).text.split("_")[0])
			arraydetallesot=ConectorDbMysql().FuncGetSpr(1,'spr_get_otcombac',[Idactividad,orden])
			print("!",arraydetallesot)
			driver.find_elements(By.XPATH,'//DIV[@class="grid-content"]//DIV[@class="grid-row pointer"]//div[@style="background-color: rgb(255, 255, 38);"]')[0].click()
			if arraydetallesot==None:
				Iniciar()
				Razonar([9999,orden,"Razon Backlog"])
				continue

			
			#cerraralerts()			
			WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//h1[@title="Detalles de actividad"]')))				
			driver.find_element(By.XPATH,'//a[@role="button" and contains(text(),"Backoffice")]').click()
			WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//H1[@title="Backoffice"]')))	
			driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Iniciar")]').click()			
			time.sleep(1)
			driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()
			time.sleep(1)


			driver.find_element(By.XPATH,'//a[@role="button" and contains(text(),"Backlog")]').click()
			time.sleep(0.5)
			#TIPO GESTION
			clic('//input[@data-label="XA_TipoGestion_Backlog"]')
			clic('//DIV[@title="Validacion de Datos OT"]')
			time.sleep(1)
			#aliado cnd
			clic('//input[@data-label="BACKLOG_Aliado_CGO"]')
			clic('//div[@data-value="GNP"]')
			time.sleep(1)
			for i in ['//INPUT[@data-label="A_NombreGestion_Backlog"]','//INPUT[@data-label="A_ParentescoTitular_Backlog"]']:
				write(i,"N/A")
			#cerraralerts()
			time.sleep(1)
			clic('//INPUT[@data-label="A_MedioContacto_Backlog"]')
			clic('//div[@aria-label="Otro"]')
			time.sleep(1)
			write('//textarea[@data-label="A_NotasGestion_Backlog"]',"Gestion query, ver notas f7/f8")			
			driver.find_element(by=By.XPATH, value='//*[@type="submit" and @class="button submit" and contains(text(),"OK")]').click()			
			
			if arraydetallesot[1] in ('COMPLETADA'):
				Completar(arraydetallesot)	
			else:
				Razonar(arraydetallesot)

			
			#ArrayGestion=driver.find_elements(By.XPATH,'//DIV[@class="grid-content"]//DIV[@class="grid-row pointer"]//div[@style="background-color: rgb(255, 255, 38);"]')
			

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
		except:pass	
		driver.quit()
		return



def tester():
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
	import time


	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2,'excludeSwitches':['enable-logging']}
	chrome_options.add_experimental_option("prefs",prefs)

	driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
	driver.get("https://amx-res-co.etadirect.com/")

	Usuario,Clave=1019035259,"Claro2022*"

	driver.implicitly_wait(30)
	myDinamicElement=driver.find_element(by=By.XPATH, value='//*[@id="username"]')
	time.sleep(1)
	IdFile='''
	    document.getElementById("username").value = ""
	    '''
	driver.execute_script(IdFile)
	driver.find_element(by=By.XPATH, value='//*[@id="username"]').send_keys(Usuario)        
	time.sleep(2)
	IdFile='''
	    document.getElementById("password").value = ""
	    '''
	driver.execute_script(IdFile)
	driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(Clave)
	time.sleep(1)
	driver.execute_script('document.querySelector("#sign-in > div").click()')
	time.sleep(3)
	'''except Exception as e:
	                            Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
	                            print("! error conexion: ", e, Nomb_error)'''

	if driver.title=="Oracle Field Service":
	    print("desloguear secciones antiguas!")
	    bucle=0
	    while bucle<=3:
	        try:
	            #pausa()                    
	            myDinamicElement=driver.find_element(by=By.XPATH, value='//*[@id="username"]')
	            driver.find_element(by=By.XPATH, value='//*[@id="username"]').clear()
	            driver.find_element(by=By.XPATH, value='//*[@id="username"]').send_keys(Usuario)
	            time.sleep(2)
	            driver.find_element(by=By.XPATH, value='//*[@id="password"]').clear()
	            driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(Clave)
	            time.sleep(1)
	            driver.find_element(by=By.XPATH, value='//*[@id="delsession"]').click()
	            time.sleep(2)
	            driver.execute_script('document.querySelector("#sign-in > div").click()')
	            #intro=driver.find_element_by_name('user_submitted_login_form').click()
	            time.sleep(3)
	            break
	        except Exception as e:
	            Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
	            print("! error conexion: ", e, Nomb_error)
	            bucle+=1
	    print(bucle)

	#selectorComBack(driver)