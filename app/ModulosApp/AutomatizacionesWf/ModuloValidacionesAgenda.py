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
import threading



from ..ModelDataBase import ConectorDbMysql
from .InteraccionChrome import BotChrome, ExtractorEstadoOrden


def Clicker(elemento):	
	elemento.click()
	

def SelectorValidacionesAgenda(self,driver,ArrayGestion):
	#esperar un elemento	
	OtApta=False
	for i in driver.find_elements(by=By.XPATH, value='//*[@class="buttons-form"]//input[@type="button"]'):		
		if 'Actualizar' in i.get_attribute('value') and i.get_attribute("style") !="display: none;":								
			#GestorSqlite().TipificarAgenda(ArrayGestion,"No actualizada!")
			#driver.refresh()			
			OtApta=True			
		else:
			OtApta=False
	'''time.sleep(3)
				c=0
				while c<3:
					try:
						AlerCloseOt=driver.find_element(by=By.XPATH, value='//*[@role="dialog" and @aria-labelledby="ui-dialog-title-dialog_msg_dialog"]')
						print(AlerCloseOt.is_displayed())
						if AlerCloseOt.is_displayed():
							OtApta=True
						else:
							OtApta=False
						print("salida")
						break
					except Exception as e:
						c+=1
						print(e)'''
	
	conn=ConectorDbMysql().GetConn()
	cursor=conn.cursor()
	
	if OtApta==True:		
		for i in range(5):
			try:
				xpath='//*[@class="tituloprincipal tituloprinc" and contains(text(),"Información del Suscriptor")]'
				element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
				break
			except:
				time.sleep(1)
				continue
		
		try:
			#element = WebDriverWait(driver,4).until(EC.invisibility_of_element_located((By.XPATH, '//*[@role="dialog" and @class="ui-dialog ui-widget ui-widget-content ui-corner-all"]')))
				#try:
			jf="""
				document.querySelector('[class="footer-p1"]').scrollIntoView({
					behavior: 'smooth'
				});
			"""
			driver.execute_script(jf)		

			for i in driver.find_elements(by=By.XPATH, value='//*[@class="buttons-form"]//input[@type="button"]'):
				print(i.get_attribute('value'))
				if 'Actualizar' in i.get_attribute('value') and i.get_attribute("style")!="display: none;":
					#threading.Thread(daemon=True,target=selector_ValidacionesMg).start()                        
					#threading.Thread(target=lambda a:i.click(),args=([i])).start()
					threading.Thread(target=Clicker, args=([i])).start()				
					#i.click()
					cursor.callproc("---",[ArrayGestion[0],"Actualizacion Realizada"])			
					conn.commit()
					conn.close()

					return
				if 'Volver' in i.get_attribute('value') and i.get_attribute("style")!="display: none;":
					#GestorSqlite().TipificarAgenda(ArrayGestion,"No actualizada!")
					cursor.callproc("---",[ArrayGestion[0],"No actualizada!"])			
					conn.commit()
					conn.close()
					return
			
		except 	Exception as e:
			print(e)
			cursor.callproc("---",[ArrayGestion[0],"No actualizada!"])			
			conn.commit()
			conn.close()
			#GestorSqlite().TipificarAgenda(ArrayGestion,"No actualizada!")
			driver.refresh()
			return	
	else:
		cursor.callproc("---",[ArrayGestion[0],"No actualizada!"])			
		conn.commit()
		conn.close()
		#GestorSqlite().TipificarAgenda(ArrayGestion,"No actualizada!")		
		driver.close()
		

		'''except Exception as e:
									Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
									print("! error conexion: ", e, Nomb_error)
									prevalence_options = WebDriverWait(driver, timeout=2).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ui-dialog ui-widget ui-widget-content ui-corner-all"]')))
						
									GestorSqlite().TipificarAgenda(ArrayGestion,"No actualizada!")
									return'''


	