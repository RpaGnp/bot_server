#
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *
#


def selector_extagenda(self,idbot,idAct):
	print("Extraer agenda")
	driver=self.driver
	try:
		SQL='SELECT EXA_NID,EXA_NCUENTA,EXA_NORDEN,EXA_CTIPOACT from tbl_hextracagenda where EXA_CESTADO = "Pendiente" and EXA_CIDACT='+str(idAct)+';'	
		Data=ConectorDbMysql().FuncGetInfo(2,SQL)	
		
		for index,row in enumerate(Data):
			#driver.execute_script("window.open('');")
			#driver.execute_script("window.focus();")
			#driver.switch_to.window(driver.window_handles[-1])
			print("!",row)
			ConectorDbMysql().FuncUpdSpr("spr_upd_contgest",[idAct,index])#
			
			driver.get("http://agendamiento.claro.com.co/MGW/MGW/Agendamiento/index.php")				
			time.sleep(1)
			orden=row[2].split("_")[0]
			driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').click()
			driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').clear()
			driver.find_element(By.XPATH,'//input[@placeholder="Número Orden"]').send_keys(orden)


			if  "mantenimiento" in row[3].lower() or "arreglo" in row[3].lower():
				driver.find_element(By.XPATH,'//input[@type="radio" and @value="L"]').click()
			else:
				driver.find_element(By.XPATH,'//input[@type="radio" and @value="O"]').click()
			time.sleep(0.5)
			driver.find_element(By.XPATH,'//input[@type="submit"]').click()
			ConectorDbMysql().RepActividad(idbot)
			try: 
				element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="td_presentacion"]//th[@class="subtitulo_mod"]')))
			except Exception as e:				
				time.sleep(0.5)
				driver.switch_to.window(driver.window_handles[0])
				ConectorDbMysql().FuncUpdSpr("spr_upd_datage",[row[0],str({"Error":"No apta"}),str({"Error":"No apta"})])
				continue

			time.sleep(3)
			
			

			scv="return document.evaluate("'"//div[@role='"'dialog'"' and @aria-labelledby='"'ui-dialog-title-dialog_msg_dialog'"']"'", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;"
			#scv="return document.evaluate("'"//div[@role='"'dialog'"' and @aria-labelledby='"'ui-dialog-title-dialog_msg_dialog'"']"'", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.getAttribute('style');"
			vista=driver.execute_script(scv)
			if vista!=None:
				sc="document.evaluate("'"//div[@class='"'ui-widget-overlay'"']"'", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.remove();"
				driver.execute_script(sc)
			else:pass

			if driver.find_element(By.XPATH,'//div[@id="estadoag"]').text=='NO AGENDADO':
				time.sleep(0.5)
				#driver.switch_to.window(driver.window_handles[0])
				ConectorDbMysql().FuncUpdSpr("spr_upd_datage",[row[0],str({"Error":"No Agendada"}),str({"Error":"No Agendada"})])
				continue
			else:pass

			driver.find_element(by=By.XPATH,value='//div[@id="visita_menu"]').click()
			time.sleep(0.5)
			DicGral={}
			for i,value in enumerate(driver.find_elements(by=By.XPATH,value='//div[@id="visita"]//table/tbody/tr')):
				i+=1
				if i==1 :
					continue
				for x in range(2):
					try:
						DicGral.update({driver.find_elements(by=By.XPATH,value='//div[@id="visita"]//table/tbody/tr['+str(i)+']/th')[x].text:driver.find_elements(by=By.XPATH,value='//div[@id="visita"]//table/tbody/tr['+str(i)+']/td')[x].text})		
					except:pass

			#print(DicGral)

			time.sleep(2)
			for i in range(3):
				try:
					driver.find_element(By.XPATH,'//div[@id="bitacora_menu"]').click()
					break
				except:
					try:					
						driver.find_element(By.XPATH,'//span[@class="ui-button-text" and contains(text(),"Aceptar")]').click()
					except:
						pass
			time.sleep(2)
			DicBitacora={}

			#for i in range(0,len(driver.find_elements(By.XPATH,'//a[@class="jp-next"]'))+1):	
			ArrayCampos=["","Fecha","Hora","ProgramadoPor","Usuario","AreaUsuario","Accion","Motivo","AtencionInmediata"]
			for x in range(1,len(driver.find_elements(By.XPATH,'//table[@id="tb-bitacora"]/tbody/tr'))+1):
				scv="document.evaluate("'"//table[@id='"'tb-bitacora'"']/tbody/tr[%s]"'", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.setAttribute('style','display: table-row; opacity: 1;');"%x
				
				driver.execute_script(scv)	
				time.sleep(0.5)
				arrayfila=[]		
				for y in range(1,9):						
					arrayfila.append(driver.find_element(By.XPATH,'//table[@id="tb-bitacora"]/tbody/tr['+str(x)+']/td['+str(y)+']').text)
				arrayfila.insert(0,row[0])
				arrayfila.pop(3)
				print(arrayfila)
				
				ConectorDbMysql().FuncUpdSpr("spr_ins_datageext",arrayfila)								
					#DicBitacora.update({f"{ArrayCampos[y]}_{x}":driver.find_element(By.XPATH,'//table[@id="tb-bitacora"]/tbody/tr['+str(x)+']/td['+str(y)+']').text})
					#DicBitacora.update({f"{ArrayCampos[y]}_{x}":driver.find_element(By.XPATH,'//table[@id="tb-bitacora"]/tbody/tr['+str(x)+']/td['+str(y)+']').text})
					#print(f"{ArrayCampos[y]}_{x}")
			#print(DicBitacora)

			#driver.close()
			time.sleep(0.5)
			#driver.switch_to.window(driver.window_handles[0])
			ConectorDbMysql().FuncUpdSpr("spr_upd_datage",[row[0],str(DicGral),str(DicBitacora)])

		ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot,idAct, 'Labor Terminada']))			
		driver.quit()

	except Exception as e:
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
		print("@",Nomb_error)
		driver.quit()