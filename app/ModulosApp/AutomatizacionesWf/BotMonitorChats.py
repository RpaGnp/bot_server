import sys
import time
import random
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver import ActionChains

from ..Carpetas import	CreadorCarpetas
from ..ModelDataBase import ConectorDbMysql
from ..reloj_casio import timer


class BotMonitorChat:
	def __init__(self,IdBot,IdGestion,ciudad,driver):
		self.idbot=IdBot
		self.idAct=IdGestion
		self.ciudad=ciudad
		self.driver=driver		
		self.PathImagenes=CreadorCarpetas("C://DBGestionBot//ImgErrorChat/")		
		self.dicCiudades = {"Cali":"Interapps Oriente","Bogota":"Interapps Centro_GNP","Bucaramanga":"Interapps Occidente"}

	def is_within_time_range(self,start_hour, end_hour):
		now = datetime.datetime.now()
		start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
		end_time = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)

		return start_time <= now < end_time

	def vigilar(self):
		while 1:
			if self.is_within_time_range(6, 22):
				try:
					self.ConsultaChat()
					if self.EsperarChat() == False:
						return 
				except Exception as e:
					self.driver.save_screenshot(f"{self.PathImagenes}-ChatErrorimg{timer()[2]}.png")
					print("Error ejecucion ",e)
					self.driver.refresh()
					time.sleep(5)
					print(e)
			else:
				self.driver.quit()
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [self.idbot, self.idAct, 'Labor Terminada']))
	
	def TipificaTr(self):
		pass


	def ConsultaChat(self):
		driver=self.driver
		time.sleep(1)
		while 1:
			try:
				driver.find_element(By.XPATH,'//div[@class="buttons-panel"]/*[@role="button"][2]').click() #ok
				break
			except Exception as e:
				driver.refresh()    			
				driver.find_element(By.XPATH,'//div[@title="Cerrar"]').click()
				
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)

		time.sleep(2)
		driver.find_element(By.XPATH,'//div[@id="community-container"]//div[@id="helpdeskChatsTabHead"]').click() #ok
		time.sleep(2)
		try:
			driver.find_element(By.XPATH,'//div[@id="community-left-content-body"]//span[contains(text(),"%s")]'%self.dicCiudades[self.ciudad]).click()	
		except Exception as e:
			self.driver.save_screenshot(f"{self.PathImagenes}-ChatErrorimg{timer()[2]}.png")
			sql=("SPR_INS_ESTBOT",[self.idbot,"Error selecionando Bolsa!"])
			ConectorDbMysql().FuncInsInfoOne(sql)            

	def EsperarChat(self):
		# funcional
		driver=self.driver
		while 1:
			if driver.title=='Oracle Field Service':
				driver.quit()
				return False			
			element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="community-chat-list"]')))								
			if driver.find_element(By.XPATH,'//div[@id="community-chat-list"]').text == 'No hay chats en espera en este momento':
				time.sleep(15)
				ConectorDbMysql().RepActividad(self.idbot)				
				time.sleep(15)
				Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [self.idbot]))
				# print(Dato[0])
				
				if Dato[0] != None:
					if Dato[0] == "Eliminar":
						ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [self.idbot, self.idAct, 'Detenido por usuario']))												
						driver.quit()
						return False
				else:pass
			else:				
				for i in range(1,len(driver.find_elements(By.XPATH,'//div[@id="community-chat-list"]/div'))+1):
					#if driver.find_element(By.XPATH,'//div[@id="community-chat-list"]/div[%s]/div[@class="community-unread"]/div[@role="alert"]'%i).get_attribute("aria-label")=="Un mensaje no leído":
					dicChatAtr={"Leido":False,"Tomado":False,"Transferido":False,"transTo":None}
					driver.find_element(By.XPATH,'//div[@id="community-chat-list"]/div[%s]'%i).click()					
					self.TrasferirChat1()
					self.ConsultaChat()
		


	def SorteaAsesor(self):
		dicAsesor={}
		Dato = ConectorDbMysql().FunGetProcedure(2,"spr_get_asedis", [self.idAct])
		for i in Dato:
			dicAsesor[i[0]]:{"Nombre":dicAsesori[1],"Asignacion":0}

		return dicAsesor



	def choseone(self):
		Dato = ConectorDbMysql().FuncGetSpr(2,"spr_get_asedis", [self.idAct])
		return Dato[random.randint(0,len(Dato))-1]

	def TomarChat(self):		
		driver = self.driver		
		element = WebDriverWait(driver,12).until(EC.visibility_of_element_located((By.XPATH, '//input[@type="button" and @value="Tomar chat"]')))
		driver.find_element(By.XPATH,'//input[@type="button" and @value="Tomar chat"]').click()		
		time.sleep(1)
		Opciones ="Buen dia! Indique el numero segun la opcion solicitada 1-Adelantos de Visita: VIP 2-Agendamiento clientes VIP 3-Cancelación agendamientos 4-Cierre visitas en RR 5-Garantías de servicio 6-Re-agendamiento de visita"

		driver.find_element(By.XPATH,'//textarea[@placeholder="Introducir mensaje"]').send_keys(Opciones)		
		driver.find_element(By.XPATH,'//textarea[@placeholder="Introducir mensaje"]').send_keys(Keys.ENTER)

	def MonitorRespuestas():
		driver = self.driver
		x=0
		while x<180:
			res= driver.find_element(By.XPATH,'').text
			if res !="":
				return 
			else:
				time.sleep(1)




	def salirChat(self):		
		driver=self.driver
		element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="community-right-pane community-right-pane-show community-scroll-bg-chat-image"]//div[@aria-label="Atrás"]')))
		time.sleep(1)
		driver.find_element(By.XPATH,'//div[@class="community-right-pane community-right-pane-show community-scroll-bg-chat-image"]//div[@aria-label="Atrás"]').click()		
		#driver.find_elements(By.XPATH,'//div[@class="community-right-pane community-right-pane-show"]//div[@aria-label="Atrás"]')[0].click()
		time.sleep(1)
		driver.find_element(By.XPATH,'//div[@id="activeChatsTabHead"]').click()
		time.sleep(0.5)

	def retomarChat(self):
		driver=self.driver
		driver.find_element(By.XPATH,'//div[@id="community-left-scroll-box"]//DIV[@id="active-chat"]//div[@id="community-chat-list"]/div[1]').click()
		time.sleep(1)
		#driver.find_element(By.XPATH,'//div[@id="community-send-message-field"]/div[1]/textarea').send_keys("Buen dia!")
		#time.sleep(1)
		#driver.find_element(By.XPATH,'//div[@id="community-send-message-field"]//div[@aria-label="Enviar"]').click()

	def invitarUser(self,user):
		driver=self.driver
		try:
			print("Invitar usuario!")		
			#element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//DIV[@id="community-addUser-icon"]')))
			chatTomado=False
			for i in range(5):
				try:
					driver.find_element(By.XPATH,'//DIV[@id="community-addUser-icon"]').click()
					chatTomado=True
					break
				except:
					time.sleep(3)
					
			time.sleep(1)

			if chatTomado==False:
				self.driver.save_screenshot(f"{self.PathImagenes}-ChatErrorimg{timer()[2]}.png")
				return 0
			else:
				driver.execute_script('document.getElementById("community-search-bar").removeAttribute("style")')
				driver.execute_script('document.getElementById("community-search-field").removeAttribute("style")')
				time.sleep(1)
				xpath='//div[@id="community-search-field-hint"]'
				element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
				driver.find_element(By.XPATH,xpath).click()
				driver.find_element(By.XPATH,'//input[@aria-label="Buscar por palabra clave"]').clear()
				driver.find_element(By.XPATH,'//input[@aria-label="Buscar por palabra clave"]').send_keys(f"{user}\n")
				#selecionar usuario
				#for i in driver.find_elements(By.XPATH,'')
				time.sleep(1)
		
		except Exception as e:
			self.driver.save_screenshot(f"{self.PathImagenes}-ChatErrorimg{timer()[2]}.png")
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print("Error transfiriendo ",Nomb_error)
			return 0

		try:
			driver.find_element(By.XPATH,'//DIV[@id="u:%s@amx-res-co"]'%user).click()
			return 1
		except :
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)
			return 0

	def TrasferirChat1(self):
		driver=self.driver
		try:
			self.TomarChat()
			# transferir			
			#self.salirChat()
			time.sleep(5)
			#self.retomarChat()
			time.sleep(3)
			asesorEscogido=self.choseone()[0]
			print(asesorEscogido)			
			if self.invitarUser(asesorEscogido):
				print("transferir ",asesorEscogido)
				#driver.find_element(By.XPATH,'//textarea[@class="move-reason-text-area"]').send_keys("Gestion")				
				#driver.find_element(By.XPATH,'//input[@class="community-button button move-chat-transfer-button submit"]').click() # trasnsfiere
				#time.sleep(3)
				ConectorDbMysql().FuncUpdSpr("spr_Ins_hischtintapp",[self.idAct,9999,"Gestionado","Asesor en linea",asesorEscogido])
				driver.refresh()
				time.sleep(3)
			else:			
				ConectorDbMysql().FuncUpdSpr("spr_Ins_hischtintapp",[self.idAct,9999,"No Gestionado","Asesor Desconectado",9999])
				driver.refresh()
		except Exception as e:
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)
	

	def TrasferirChat(self):
		driver=self.driver
		self.TomarChat()
		time.sleep(1)
		try:
			self.Saludar()
			wait = WebDriverWait(driver, 60)
			element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="community-transferConversation-icon"]')))
		except Exception as e:			
			Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
			print(Nomb_error)		
			return False
		
		
		# listar los iconoes
		while 1:
			try:
				driver.find_element(By.XPATH,'//div[@id="community-transferConversation-icon"]').click()
				break
			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)

		
		wait = WebDriverWait(driver, 10)
		element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="community-helpdesk-transfer-chat-list"]/div[@role="listitem"]//div[@class="community-helpdesk-transfer-chat-list-operator-name ellipsis"]')))
		#for i in driver.find_elements(By.XPATH,'//div[@id="community-helpdesk-transfer-chat-list"]/div[@role="listitem"]//div[@class="community-helpdesk-transfer-chat-list-operator-name ellipsis"]'):	
		ArrayAsesorConWf=[x.get_attribute("address") for x in driver.find_elements(By.XPATH,'//div[@id="community-helpdesk-transfer-chat-list"]/div[@role="listitem"]')]
		print(ArrayAsesorConWf)
		interador=1
		while interador<5:
			asesorEscogido=self.choseone()[0]						
			dirasesor=f"u:{asesorEscogido}@amx-res-co"		
			print(dirasesor)

			if dirasesor not in ArrayAsesorConWf:
				interador+=1
			else:
				break


		#dirasesor=f"u:1019035259@amx-res-co"
		TrMsg=False
		for i in driver.find_elements(By.XPATH,'//div[@id="community-helpdesk-transfer-chat-list"]/div[@role="listitem"]'):
			dressasesorWf=i.get_attribute("address")
			if dirasesor==dressasesorWf:
				i.click()
				TrMsg=True
				break
				'''i.get_attribute("address")#  ="u:1032366156@amx-res-co"
																	if i.text =="GNP_PINEDA PALMA YENNY ALEXANDRA":
																		i.click()'''
		time.sleep(3)
		if TrMsg:
			print("transferir")
			driver.find_element(By.XPATH,'//textarea[@class="move-reason-text-area"]').send_keys("Gestion")
			driver.find_element(By.XPATH,'//input[@class="community-button button move-chat-transfer-button submit"]').click() # trasnsfiere
			time.sleep(3)
			ConectorDbMysql().FuncUpdSpr("spr_Ins_hischtintapp",[self.idAct,9999,"Gestionado","Asesor en linea",asesorEscogido])
			driver.refresh()
			time.sleep(3)
		else:
			driver.refresh()
			ConectorDbMysql().FuncUpdSpr("spr_Ins_hischtintapp",[self.idAct,9999,"No Gestionado","Asesor Desconectado",9999])