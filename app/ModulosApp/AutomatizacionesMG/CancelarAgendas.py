from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
#from datetime import time as tmr

from .InteraccionesMG import BotMg
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *



def SelectorCancelarAgenda(self,idbot,idAct,Trabajo):
	driver=self.driver
	Bot=BotMg(driver)
	urlPin ="https://moduloagenda.cable.net.co"
	try:
		sql="""
				SELECT dx_nid,dx_corden,dx_caliado,dx_cciudad,dx_dfechaage,dx_cobservacion
				FROM tbl_hagndasdxrx
				WHERE dx_nidbot='"""+str(idAct)+"""' AND  dx_cestgestion='Pendiente';
			"""
		array_datos=ConectorDbMysql().FuncGetInfo(0,sql)
		for data in array_datos:
			ConectorDbMysql().RepActividad(idbot)
			# funcion de salida, pausa del bot
			time.sleep(2)
			Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idbot]))			
			if Dato[0] != None:
				if Dato[0] == "Eliminar":
					ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Detenido por usuario']))
					#driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
					time.sleep(1)					
					driver.quit()
					return
			else:
				pass

			Bot.ConsultaOts(urlPin,data[1],data[5])
			# verificar orden 
			if driver.find_element(By.XPATH,'//body').text=='ningun dato parametrizado':
				sql = ("spr_upd_estgesdx", [data[0], 'ningun dato parametrizado'])			
				ConectorDbMysql().FuncInsInfoOne(sql)
				continue

			# verificar orden agenda pr wfm
			if driver.current_url!='https://moduloagenda.cable.net.co/MGW/MGW/Agendamiento/agendamiento.php':
				sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada, Redirige a modulo agendamiento antiguo!'])			
				ConectorDbMysql().FuncInsInfoOne(sql)
				continue


			#dentro de la orden
			try: 
				element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]')))
			except Exception as e:
				ConectorDbMysql().FuncInsInfoOne(("spr_upd_estgesdx", [data[0], e]))
				continue

			time.sleep(2)
			if 'Esta orden no se puede agendar en workforce' in driver.find_element(By.XPATH,'//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]').text:
				sql = ("spr_upd_estgesdx", [data[0], 'Orden no agendada, Esta orden no se puede agendar en workforce'])			
				ConectorDbMysql().FuncInsInfoOne(sql)
				continue

			try:
				driver.execute_script("document.querySelector('#cancelar').setAttribute('style','display:inline-block;')")
			except Exception as e:
				print(f"Inyeccion js fallida {e}")


			DicButton={}
			Cancelar=False
			for buttonAccion in driver.find_elements(By.XPATH,'//div[@class="buttons-form"]/input'):
				DicButton.update({buttonAccion.get_attribute("value"):buttonAccion.get_attribute("style")})					
				if buttonAccion.get_attribute("style")=='display: inline-block;' and buttonAccion.get_attribute('value') == "Cancelar":
					#print(buttonAccion.get_attribute('value'),buttonAccion.get_attribute("style"))
					buttonAccion.click()

					try:
						element = WebDriverWait(driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))
						Cancelar=True
					except:
						break
					else:
						continue

			if Cancelar:
				if Trabajo =="Cancelar Agenda Pin":
					WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]')))
					driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//textarea').send_keys('Envío pin')		
					time.sleep(1)
					driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//input[@type="submit"]').click()
					WebDriverWait(driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))

					WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]')))
					Resultado=driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]//tr').text
				else:
					WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]')))
					time.sleep(1)
					driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//textarea').send_keys("Cancelacion")
					time.sleep(1)
					driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//input[@type="submit"]').click()

					WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_cancelar_orden"]')))
					driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_cancelar_orden"]//button/span[contains(text(),"Confirmar")]').click()
					WebDriverWait(driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))

					driver.back()
					Resultado="Ot cancelada con exito"			

			else:
				Resultado=f"No se puede Gestionar, Boton cancelar no aparece {DicButton}"
			##============================// continuar cancelando la orden //============================
			ConectorDbMysql().FuncInsInfoOne(("spr_upd_estgesdx", [data[0], Resultado]))


		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Labor Terminada']))		
		driver.quit()

	except Exception as e:
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print(Nomb_error)
	
		sql = ("spr_upd_estgesdx", [data[0], f'Error cancelando orden {Nomb_error[0]} {Nomb_error[1]}'])
		ConectorDbMysql().FuncInsInfoOne(sql)
		
		driver.quit()
