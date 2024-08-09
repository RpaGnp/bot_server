import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver import ActionChains
from datetime import datetime,timedelta

from ..ModelDataBase import ConectorDbMysql
from ..interaccionChrome import Botinteraccion


class handlemer:
	def __init__(self,driver,idgestion,idbot,idusuario):
		self.driver = driver
		self.idgestion = idgestion
		self.idbot = idbot
		self.idusuario = idusuario
		self.Bot=Botinteraccion(driver)

	def gettime(self):
		# 19/06/2024 00:00:00
		now = datetime.now()
		new_date = now + timedelta(days=1)
		new_date = new_date.replace(hour=0, minute=0, second=0, microsecond=0)
		formatted_date = new_date.strftime("%d/%m/%Y %H:%M:%S")		
		return formatted_date

	def Preingreso(self):
		for xpath in ['//div[@id="cssmenu"]','//a[contains(text(), "Menú Principal")]/following-sibling::ul','//a[contains(text(), "Menú Principal")]/following-sibling::ul//following-sibling::ul']:
			icon =self.driver.find_element(By.XPATH,xpath)
			self.driver.execute_script('arguments[0].style.display = "block";', icon)
			time.sleep(1)

		self.driver.find_element(By.XPATH,'//a[@title="Buscar cuenta matriz" and contains(text(), "Búsqueda")]').click()		
		WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH,'//div[@id="panelBusquedadCm"]')))		
	
	def Actualizagestion(self,idrow,ordengenerada,observacion):
		ConectorDbMysql().FuncUpdSpr("spr_upd_otccotgen",[idrow,ordengenerada,self.idusuario,observacion])

	def waitorden(self):
		WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="white_contentError"]')))
		numeroot=self.driver.find_element(By.XPATH,'//div[@id="marcoAuditoria"]//b').text
		self.Bot.click('//a[@id="cerrarMensajeErrorBtn"]')
		return numeroot

	def crearorden(self):
		self.driver.find_element(By.XPATH,'//a[@id="formCMGeneral:detalleCmPtOt"]').click()
		WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH,'//select[@id="formCMGeneral:TipoOtList"]')))
		self.driver.find_element(By.XPATH,'//select[@id="formCMGeneral:TipoOtList"]//option[@value="1"]').click()

		self.driver.find_element(By.XPATH,'//input[@id="formCMGeneral:idNuevaOt"]').click()		
		#llenar el formulario
		
		#tencologia
		self.Bot.click('//select[@id="form33646:tecnologiasList"]//option[@value="26970"]')				
		#tipo de orden				
		self.Bot.click('//select[@id="form33646:SubtipoTrabajoLabel"]//option[@value="43130"]')
		#Subtipo
		self.Bot.click('//select[@id="form33646:tipoTrabajoOt"]//option[@value="347"]')
		#segmento
		self.Bot.click('//select[@id="form33646:SegmentoOtList"]//option[@value="43134"]')
		# estado interno
		self.Bot.click('//select[@id="form33646:EstadoOtList"]//option[@value="27332"]')
		
		#ocultar calendario		
		#fecha
		self.driver.find_element(By.XPATH,'//input[@id="form33646:FprogramacionOtInput_input"]').send_keys(self.gettime())				
		time.sleep(1)		
		while 1:
			try:
				cal =self.driver.find_element(By.XPATH,'//div[@id="ui-datepicker-div"]')
				self.driver.execute_script("arguments[0].style.display = 'none';",cal)
				break
			except:
				print("hidden")
				time.sleep(1)

		# clase de ot
		#self.Bot.click('//select[@id="form33646:ClaseTraOtList"]')
		self.Bot.click('//select[@id="form33646:ClaseTraOtList"]//option[@value="43135"]')

		# observaciones
		self.driver.find_element(By.XPATH,'//textarea[@id="form33646:ObservacionesOtInput"]').send_keys("Se envia mantenimiento")
		
		element = self.driver.find_element(By.XPATH,'//input[@type="submit"]')
		self.driver.execute_script("arguments[0].scrollIntoView();", element)
		time.sleep(0.5)
		element.click()

		orden = self.waitorden()
		print(orden)
		return orden

	def main(self):
		# traer los datos de base de datos		
		sql="""SELECT CCOT_NID,CCOT_ITEM,CCOT_NO_CTA_MATRIZ,CCOT_NOMBRE,CCOT_TIPO_DE_SITIO,
				CCOT_SITIO,CCOT_ID_SITIO,CCOT_NODO,CCOT_TIPO_TRABAJO,CCOT_SUB_TIPO_DE_TRABAJO,CCOT_CLASE_DE_OT,CCOT_NOTA_DE_OBSERVACIONES,
				CCOT_NOMBRE_DE_LA_PERSONA_DEL_PROVEEDOR,CCOT_CORREO,CCOT_CELULAR,CCOT_REGIONAL,CCOT_DEPARTAMENTO,CCOT_CIUDAD,
				CCOT_ALIADO,CCOT_ALMACEN,CCOT_CENTRO_SUMINISTRADOR,CCOT_PERSONA_CON_PERFIL_CCOA,CCOT_FECHA_EN_LA_QUE_SE_REQUIERE_AGENDAR,
				CCOT_TECNOLOGIA,CCOT_SEGMENTO,CCOT_OT_CREADA_EN_MER,CCOT_CCOT_QUE_CREA_LA_OT,CCOT_USUARIO_QUE_CREA_LA_OT				
				FROM TBL_BASEGESCCOT
				WHERE CCOT_NIDASIGNACION=%s AND  CCOT_NESTGES=0;
			"""%self.idgestion		
		array_datos=ConectorDbMysql().FuncGetInfo(0,sql)
		for data in array_datos:
			self.Preingreso()
			ConectorDbMysql().RepActividad(self.idbot)
			# funcion de salida, pausa del bot
			time.sleep(2)
			Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [self.idbot]))
			# print(Dato[0])
			if Dato[0] != None:
				if Dato[0] == "Eliminar":
					ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [self.idbot, self.idgestion, 'Detenido por usuario']))
					#driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
					time.sleep(1)					
					driver.quit()
					return
			else:
				pass	

			print(data)
			try:
				self.driver.find_element(By.XPATH,'//div[@id="contenido"]//input[@name="formPrincipal:j_idt330"]').send_keys(data[2])
				time.sleep(1)
				self.driver.find_element(By.XPATH,'//h2').click()
				while 1:
					try:
						self.Bot.click('//input[@id="formPrincipal:buttonBuscarCm"]')
						break
					except Exception as e:						
						time.sleep(1)


				time.sleep(1)
				self.Bot.click('//a[@id="formCMGeneral:detalleCmPtPenetracion"]')

				# recuperar los datos de la tabla							
				
					
				Nodofuerazona = False
				dictable={}
				for i in range(1,len(self.driver.find_elements(By.XPATH,'//table[@class="tablefeel"]//tbody/tr'))+1):						
					dictable["Tecnologia"]=self.driver.find_element(By.XPATH,'//table[@class="tablefeel"]//tbody/tr[%s]/td[1]'%i).text
					dictable["EstadoTecnologia"]=self.driver.find_element(By.XPATH,'//table[@class="tablefeel"]//tbody/tr[%s]/td[2]'%i).text
					if dictable["Tecnologia"].upper() == "NODO FUERA DE ZONA":
						ordentrabajo=self.crearorden()
						if ordentrabajo!=None:
							self.Actualizagestion(data[0],ordentrabajo,"Generado ok")							
						else:
							self.Actualizagestion(data[0],99999,"Error generando ot")
						Nodofuerazona = True
						break

				if Nodofuerazona == False:
					self.Actualizagestion(data[0],99999,"Error generando ot sin datos en tabla penetracion")

			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)

		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [self.idbot,self.idgestion, 'Labor Terminada']))			
		self.driver.quit()