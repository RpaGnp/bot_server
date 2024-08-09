
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
from selenium.webdriver.firefox.service import Service
import time
import csv
import sys
import os
from datetime import datetime

from datetime import datetime
import random
import csv
import tempfile

#from ModulosApp.ModelDataBase import ConectorDbMysql	

class ManejadorDw():
	#def __init__(self,driver):
	#	self.driver=driver

	@classmethod
	def CreadorDir(self):
		self.dirpath = tempfile.mkdtemp()

		return self.dirpath
		
	@classmethod
	def GestorDescargaFile(self,Dirtemp):		
		# Get list of all files only in the given directory
		list_of_files = filter(lambda x: os.path.isfile(os.path.join(Dirtemp, x)),
		                       os.listdir(Dirtemp))
		# Sort list of files based on last modification time in ascending order
		list_of_files = sorted(list_of_files,
		                       key=lambda x: os.path.getmtime(os.path.join(Dirtemp, x))
		                       )
		# Iterate over sorted list of files and print file path
		# along with last modification time of file
		for file_name in list_of_files:
		    file_path = os.path.join(Dirtemp, file_name)
		    timestamp_str = time.strftime('%m/%d/%Y :: %H:%M:%S', time.gmtime(os.path.getmtime(file_path)))
		    print(timestamp_str, ' -->', file_name)

		

		return timestamp_str,file_name




class HandleAvaya():
	def __init__(self,driver):
		self.driver=driver

		
	def dowhile(self,eval):
		while 1:
		    try:
		        eval
		        break
		    except Exception as e:
		        time.sleep(1)
		        print(e)


	def LoginAvaya(self,UsuarioAvaya,ClaveAvaya):	    
	    driver=self.driver
	    wait = WebDriverWait(driver, 20)        
	    driver.get("http://10.60.144.194/wfo/control/signin?rd=%2Fwfo%2Fui%2F&hash=wsm%25255Bws%25255D%253DlegacyWorkspace%2526url%253D..%25252Fcontrol%25252Fmy_notifications%25253FNEWUINAV%25253D1%2526selTab%253D3_BBM_MYNOTIFICATIONS%2526navparent%25255BworkspaceId%25255D%253D")


	    self.dowhile('Workforce Engagement Sign-in' == driver.title)
	    driver.find_element(by=By.XPATH, value='//*[@id="username"]').send_keys(UsuarioAvaya)
	    time.sleep(random.randint(1, 3))
	    driver.find_element(by=By.XPATH, value='//*[@id="loginToolbar_LOGINLabel"]').click()
	    time.sleep(random.randint(1, 3))
	    driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(ClaveAvaya)
	    time.sleep(random.randint(1, 3))
	    driver.find_element(by=By.XPATH, value='//*[@id="loginToolbar_LOGINLabel"]').click()
	    time.sleep(random.randint(1, 5))
	    try:
	        driver.find_element(by=By.XPATH, value='//*[@class="stdError messageWithImage pie"]')
	        return False
	        #notificar error login
	    except:
	        return True

	def confAvaya(self):
		driver=self.driver
		for i in ['//*[@id="as-navdrawer-arrow"]','//*[@id="tableview-1063-record-52"]','//*[@tabid="INTERACTION->interactions_tab->search_tab"]']:
			driver.find_element(by=By.XPATH, value=i).click()
			time.sleep(random.randint(1, 3))

	def Busqueda(self):
		#def Busqueda(self,Idrow,ArrayNumeros):
		driver=self.driver
		
		with open(r"C:\Users\USER\Downloads\ReporteBotCalidad-26-10-2022\BaseGestion.csv","r",encoding="latin-1") as file:
			next(file)
			csv_reader = csv.reader(file, delimiter=';')
			ArrayExtraccion=[]
			for i in csv_reader:
				#print(i)
				nu1=i[8].replace(".0","")
				nu2=i[9].replace(".0","")

				#if len(nu1)<10:

				#prepara numeros
				#print(f"('{i[0]}','{i[1]}',curdate(),'Ingresado OK'),")
				#print(nu1,nu2)
				if nu1==nu2:
					ArrayNumeros=[int(nu1)]
				else:
					ArrayNumeros=[int(nu1),int(nu2)]								

				dicExtraccion={}
				#print(ArrayNumeros)
				for index,numero in enumerate(ArrayNumeros):
					dicExtraccion[f'NumeroCel']=numero

					driver.find_element(by=By.XPATH, value='//*[@data-ref="btnInnerEl" and contains(text(),"Búsqueda avanzada")]').click()
					time.sleep(0.5)
					driver.find_element(by=By.XPATH, value='//*[@data-ref="displayEl"]').click()
					time.sleep(0.5)
					driver.find_element(by=By.XPATH, value='//*[@class="x-autocontainer-innerCt" and contains(text(),"Interacciones")]').click()
					
					#llenar campos de telefono y consultar    		
					driver.find_element(by=By.XPATH, value='//*[@elementid="DNIS"]//input').send_keys(numero)
					time.sleep(random.randint(1, 2))    		
					driver.find_elements(by=By.XPATH, value='//*[@aria-label="Búsqueda"]')[1].click()
					time.sleep(random.randint(1,2))
					
					try:
						for i,fila in enumerate(driver.find_elements(by=By.XPATH, value='//div[contains(@id,"dynamicgridpanel")]//table[contains(@id,"tableview")]/tbody/tr')):
							DicFilas={}												
							fechaLLs=driver.find_elements(by=By.XPATH, value='//div[contains(@id,"dynamicgridpanel")]//table[contains(@id,"tableview")]/tbody/tr/td[@data-columnid="audio_start_time"]')[i].text 
							if fechaLLs.split(" ")[0]!= datetime.now().strftime("%d/%m/%Y"):						
								continue

							driver.find_elements('//div[contains(@id,"dynamicgridpanel")]//table[contains(@id,"tableview")]/tbody/tr')[i].click()
							DicFilas[f"fila"]=i				
							DuracionLLs=driver.find_elements(by=By.XPATH, value='//div[contains(@id,"dynamicgridpanel")]//table[contains(@id,"tableview")]/tbody/tr/td[@data-columnid="duration"]')[i].text    		
							Empleado=driver.find_elements(by=By.XPATH, value='//div[contains(@id,"dynamicgridpanel")]//table[contains(@id,"tableview")]/tbody/tr/td[@data-columnid="personal_name"]')[i].text    		
							ExtencionLLs=driver.find_elements(by=By.XPATH, value='//div[contains(@id,"dynamicgridpanel")]//table[contains(@id,"tableview")]/tbody/tr/td[@data-columnid="ani"]')[i].text    		
							
							DicFilas['fechaLLs']=fechaLLs
							DicFilas['DuracionLLs']=DuracionLLs
							DicFilas['Empleado']=Empleado
							DicFilas['ExtenmcionLLs']=ExtencionLLs
							dicExtraccion[f'DatosFila{i}']=DicFilas


							#DESCARAGR EL AUDIO
							if int(DuracionLLs.split(":")[1])<=59:
								time.sleep(random.randint(2,4))
								driver.find_element(by=By.XPATH, value='//*[@aria-label="Descargar interacción"]').click()
								time.sleep(random.randint(1,3))
								driver.find_element(by=By.XPATH, value='//*[@data-ref="btnInnerEl" and contains(text(),"Aceptar")]').click()

								textAudio=Manjador
							#print(DicFilas)
					except Exception as e:
						Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
						print(Nomb_error)
						dicExtraccion[f'DatosFila']="No hay llamada"			
						
					driver.back()
					
					print(dicExtraccion)
		




    	
def main():	
	carptemp=ManejadorDw.CreadorDir()
	ManejadorDw.GestorDescargaFile(carptemp)
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2,
	'excludeSwitches':['enable-logging'],"download.default_directory":carptemp}
	chrome_options.add_experimental_option("prefs",prefs)

	sdriver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
	sdriver.maximize_window()


	UsuarioAvaya="1144025554"
	ClaveAvaya="Garcinc1025*"
	prueba=HandleAvaya(sdriver)
	prueba.LoginAvaya(UsuarioAvaya,ClaveAvaya)
	prueba.confAvaya()
	prueba.Busqueda()



carptemp=ManejadorDw.CreadorDir()
carptemp=r"C:\Users\USER\AppData\Local\Temp\tmp_djh4e3f"
x=ManejadorDw.GestorDescargaFile(carptemp)
print(x)