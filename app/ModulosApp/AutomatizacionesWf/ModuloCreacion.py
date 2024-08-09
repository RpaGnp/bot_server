
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
import os
from datetime import date
from datetime import datetime
from selenium.webdriver.chrome.options import Options


from .CreaCompleta import selector_Completacion
from ..interaccionChrome import Botinteraccion

from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *



def selector_Creacion(self,idBot,Idactividad,ActPro):
    driver=self.driver
    Bot=Botinteraccion(driver)
    print("Creacion")
    try:        
        lista_contador=[]
        sql="""SELECT  ACC_NID, ACC_CTIPGESTION, ACC_CALIADOCND, ACC_DFECHA, ACC_CTIPOOT, ACC_CREGION, ACC_NOTBACK, ACC_NCUENTA, ACC_CTIPOCLIE, ACC_CNOMCLIE, ACC_CDIRECCION, ACC_CCIUDAD, ACC_CNODO, ACC_CALIADO, ACC_CCAUSAGES, ACC_CDETGES, ACC_CNOTASOT, ACC_CTRABAJO
               from tbl_hatccreacionbot
               where ACC_NIDAC='"""+str(Idactividad)+"""' and ACC_CESTGES='Pendiente'
            """
            #print(sql)
        array_datos=ConectorDbMysql().FuncGetInfo(0,sql)                
        #contadorCompletar=0
        for i,dato in enumerate(array_datos):            
            data=list(dato)
            IdRow=data[0]
            data.pop(0)
            del dato                                        
            data[2]=data[2].replace("/","-")
            print(data)
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
                    return
                else:pass
            else:pass
            

            element = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="toaGantt-tb toaGantt-tb-name"]')))
            try:                    
                driver.execute_script('document.querySelector("#panel").setAttribute("style","display:none")')
            except:pass
            
            def ingresar_a_fomulario():
                x=0
                while x<=5:
                    try:
                        driver.implicitly_wait(5)
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="app-button-title" and contains(text(),"Acciones")]')))                        
                        driver.find_element(by=By.XPATH, value='//*[@class="app-button-title" and contains(text(),"Acciones")]').click()
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="toolbar-menu-button-title" and contains(text(),"Agregar actividad")]')))
                        botondos = driver.find_element(by=By.XPATH, value='//*[@class="toolbar-menu-button-title" and contains(text(),"Agregar actividad")]')
                        if botondos.is_displayed() == True:
                            time.sleep(0.5)
                            botondos.click()
                        else:
                            pass
                        time.sleep(2)
                        #Bot.ClicJs('document.querySelector("#id_index_0 > button").click()')
                        #driver.find_element(by=By.XPATH, value=).click()
                        driver.find_element(by=By.XPATH, value='//header[@aria-label="Sección Crear Actividad"]/parent::div//following-sibling::div//button').click()
                        #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, ('//*[@type="button" and contains(text(),"Backoffice")]'))))
                        driver.find_element(by=By.XPATH, value='//*[@aria-label="Backoffice"]').click()
                        break
                    except Exception as e:
                        Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
                        print(Nomb_error)
                        x+=1
                        time.sleep(0.5)
                        try:
                            driver.find_elements(by=By.XPATH, value='//*[@aria-label="Consola de despacho"]')[0].click()
                            time.sleep(3)
                        except:
                            pass
                time.sleep(0.5)
            ingresar_a_fomulario()

            def ActividadProgramada():
                Bot.ClicJs('document.querySelector("#_radio_index_215_1").click()')
                
            if ActPro==True:
                ActividadProgramada()                    
            else:
                pass
            #ActividadProgramada()

            def tipo_gestion(self):
                x=0
                while x<5:
                    try:
                        driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Tipo Gestion"]').click()
                        time.sleep(0.25)
                        TipGes=data[0].strip()                                                
                        driver.find_element(By.XPATH,'//div[@aria-label="Tipo Gestion, Requerido"]//div[@aria-label="%s"]'%TipGes).click()                            
                        return
                            

                        TipGes=data[0].lower().strip()
                        if  TipGes=="gestion backlog":                    
                            driver.find_element(by=By.XPATH, value='//*[@data-value="BACKBDT"]').click()
                        elif TipGes =="seguimiento despacho":
                            driver.find_element(by=By.XPATH, value='//*[@data-value="BACKSD"]').click()
                        elif TipGes=="soporte interno":
                            driver.find_element(by=By.XPATH, value='//*[@data-value="BACKSI"]').click()
                        
                        #agredadas desde cali
                        
                        elif TipGes=="cge":
                            driver.find_element(by=By.XPATH, value='//*[@data-value="BACKCG"]').click()
                        elif TipGes=="confirmación" or  TipGes=="confirmacion":
                            driver.find_element(by=By.XPATH, value='//*[@data-value="BACKCO"]').click()
                        elif TipGes=="enrutamiento":
                            driver.find_element(by=By.XPATH, value='//*[@data-value="BACKEN"]').click()
                        elif TipGes=="soporte interno resolutor myIt":
                            driver.find_element(by=By.XPATH, value='//*[@aria-label="Soporte interno Resolutor MyIt"]').click()

                        elif TipGes in ["contención de visitas","contencion de visitas"]:
                            driver.find_element(by=By.XPATH, value='//*[@aria-label="Contención de visitas"]').click()

                        elif TipGes in ["gestión dx","gestion dx"]:
                            driver.find_element(by=By.XPATH, value='//*[@aria-label="Gestión DX"]').click()                        
                            


                        else:           
                            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        break
                    except:
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(0.5)
                        x+=1
            
            def CausaGestion(self):                
                if data[0].strip() in [
                            "Cierre OT manual",                            
                            "Contención OT",
                            "Contención de visitas",                            
                            "Gestión DX",
                            "Gestión incidentes",
                            "Gestión visitas técnicas",
                            "Registro OT/LLS M.E.R"
                            ]:
                    return                                
                element=driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Causa Gestión"]')
                driver.execute_script("arguments[0].scrollIntoView();", element)
                del element
                x=0
                while x<5:
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Causa Gestión"]').click()
                        time.sleep(0.5)
                        #Gestion=data[0].strip()
                        if data[0]=="Cierre OT manual":
                            driver.find_element(by=By.XPATH, value='//*[@aria-label="Gestión de Backlog"]').click()
                        elif data[0]=="SEGUIMIENTO DESPACHO" or data[0].strip()=="Seguimiento despacho":
                            driver.find_element(by=By.XPATH, value='//*[@aria-label="Seguimiento visita"]').click()
                        
                        elif data[0] == "SOPORTE INTERNO" or data[0].strip()=="Soporte Interno":
                            if self.Ciudad=="Bogota":
                                driver.find_element(by=By.XPATH, value='//*[@data-value="CSIN04"]').click()
                            else:
                                driver.find_element(by=By.XPATH, value='//*[@aria-label="Seguimiento VIP"]').click()
                        #agregadas desde cali
                        elif data[0].strip()=="confirmación" or data[0].strip()=="confirmacion":
                            driver.find_element(by=By.XPATH, value='//*[@aria-label="Reprogramación"]').click()

                        elif data[0].strip()=="CGE":
                            driver.find_element(by=By.XPATH, value='//*[@data-value="CCGE01" and  contains(text(),"Creacion X WFM")]').click()
                        
                        elif data[0].strip()=="Enrutamiento":                        
                            driver.find_element(by=By.XPATH, value='/html/body/div[10]/div[6]/form/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[15]/div[2]/div[1]/div/div/select/option[2]').click()
                        
                        elif data[0].strip()=="Gestion Backlog":
                            driver.find_element(by=By.XPATH, value='//*[@data-value="GBACKL"]').click()

                        else:
                            time.sleep(0.5)
                            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        break
                    except:
                        driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Causa Gestión"]').click()
                        time.sleep(0.5)
                        x+=1

            def Reprogramaciones(self):
                try:
                    element=driver.find_elements(by=By.XPATH, value='//*[@name="Back_Num Reprogramaciones"]')[0]
                    actions = ActionChains(driver)
                    actions.move_to_element(element)
                    actions.perform()
                    time.sleep(0.5)
                    xpath='//*[@name="Back_Num Reprogramaciones"]'
                    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,xpath)))                    
                    driver.find_elements(by=By.XPATH, value='//*[@name="Back_Num Reprogramaciones"]')[0].click()
                    del element, xpath
                except Exception as e:
                    Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
                    print(Nomb_error)

                

            
            
            def selector_tipo_actividad(self):
                for i in range(3):
                    try:
                        element=driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Tipo OT"]')
                        actions = ActionChains(driver)
                        actions.move_to_element(element)
                        actions.perform()                        
                        break
                    except:
                        continue                
                driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Tipo OT"]').click()
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_Tipo OT"]')))
                dato=data[3].upper().strip()
                time.sleep(0.25)

                if dato.upper() == "ARREGLOS DTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ADTH"]').click()
                elif dato=="TRASLADOS DTH":
                    driver.find_element(By.XPATH,'//div[@aria-label="Traslado DTH"]').click()


                elif dato=="POSTVENTA DTH":
                    driver.find_element(By.XPATH,'//div[@aria-label="Postventa DTH"]').click()
                elif dato=="INSTALACIONES DTH":
                    driver.find_element(By.XPATH,'//div[@aria-label="Instalaciones DTH"]').click()
                elif dato == "DESCONEXION BIDIRECCIONAL".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="DESB"]').click()
                elif dato == "DESCONEXION UNIDIRECCIONAL".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="DESU"]').click()

                elif dato == 'RECONEXION PYMES'.upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="REPY"]').click()
                elif dato == 'RECONEXION UNI'.upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="REUN"]').click()
                elif dato == 'RECONEXION BI'.upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="REBI"]').click()
                    
                elif dato == "INSTALACION BIDIRECCIONAL".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="INBI"]').click()
                elif dato == "POSTVENTA BIDIRECCIONAL".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="PVBI"]').click()
                elif dato == "TRASLADO BIDIRECCIONAL".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="TRBI"]').click()
                elif dato == "ARREGLO BIDIRECCIONAL".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ARBI"]').click()
                elif dato == "Mantenimiento DTH Postpago".upper() or dato == "Mantenimiento FTTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ADTH"]').click()
                elif dato == "ARREGLOS PYMES".upper() or dato=="ARREGLO PYMES".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ARPY"]').click()
                elif dato == "BLINDAJE".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="BLIN"]').click()
                elif dato == "FO DISEÑO".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="fo"]').click()

                elif dato == "Instalacion Basica Bi".upper() or dato == "Instalacion Cableada Bi".upper()\
                     or dato == "Instalacion Empaquetada Bi".upper() or dato == "Instalacion FTTH_".upper()\
                     or dato == "INSTALACION FTTH":
                    driver.find_element(by=By.XPATH, value='//*[@data-value="INBI"]').click()
                
                elif dato == "Instalacion Pymes".upper() or dato =="INSTALACION PYMES".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="INPY"]').click()

                elif dato == "Instalaciones Basica DTH Postpago".upper() or dato == "Instalaciones Empaquetada DTH Postpago".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="IDTH"]').click()

                elif dato == "PostVenta Bi".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="PVBI"]').click()

                elif dato == "Postventa DTH Postpago".upper() or dato == "Postventa FTTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="PVDT"]').click()

                elif dato == "Postventa Pymes".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="PVPY"]').click()

                elif dato == "Traslado Bi".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="TRBI"]').click()

                elif dato == "Traslado DTH Postpago".upper() or dato == "Traslado FTTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="TRDT"]').click()

                elif dato == "Traslado Pymes".upper() or dato=="TRASLADO PYMES".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="TRPY"]').click()

                elif dato == "INSTALACION PYMES".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="INPY"]').click()

                elif dato=="INSTALACION FTTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="1" and contains(text(),"Instalaciones FTTH")]').click()                        

                elif dato == "POSTVENTA PYMES".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="PVPY"]').click()

                elif dato=="TRASLADO FTTH".upper() or data[3]=="TRASLADO  FTTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="5" and contains(text(),"Traslado FTTH")]').click()

                elif dato=="TRASLADO FTTH ALTO VALOR".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="6" and contains(text(),"Traslado FTTH Alto Valor")]').click()

                elif dato in ["ARREGLOS FTTH","ARREGLO FTTH"]:
                    driver.find_element(by=By.XPATH, value='//*[@data-value="7" and contains(text(),"Arreglos FTTH")]').click()

                elif dato=="ARREGLOS FTTH ALTO VALOR".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="8" and contains(text(),"Arreglos FTTH Alto Valor")]').click()

                elif dato=="POSTVENTA FTTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="3" and contains(text(),"Postventa FTTH")]').click()

                elif dato=="POSTVENTA FTTH ALTO VALOR".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="4" and contains(text(),"Postventa FTTH Alto Valor")]').click()

                elif dato=="BROWNFIELD".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="9" and contains(text(),"Brownfield")]').click()

                elif dato=="INSTALACIONES FTTH".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="1" and contains(text(),"Instalaciones FTTH")]').click()

                elif dato=="INSTALACIONES FTTH ALTO VALOR".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="2" and contains(text(),"Instalaciones FTTH Alto Valor")]').click()
                
                #agregado desde cali
                elif dato=="Fo Acometida".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ACF" and contains(text(),"FO Acometida")]').click()

                elif dato=="Fo Caja OB".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="CAJO" and contains(text(),"FO Caja OB")]').click()

                elif dato=="Fo Desinstalacion".upper():
                      driver.find_element(by=By.XPATH, value='//*[@data-value="DST" and contains(text(),"FO Desinstalacion")]').click()

                elif dato=="Fo Diseño".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="fo" and contains(text(),"FO Diseño")]').click()

                elif dato=="Fo Enrutamiento".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ENF" and contains(text(),"FO Enrutamiento")]').click()

                elif dato=="Fo Entrega Servicio".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ENTF" and contains(text(),"FO Entrega Servicio")]').click()

                elif dato=="Fo Instalacion".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="INSF" and contains(text(),"FO Instalación")]').click()

                elif dato=="Fo Mantenimiento".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="ARFO" and contains(text(),"FO Mantenimiento")]').click()

                elif dato=="Fo Replanteo".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="REPF" and contains(text(),"FO Replanteo")]').click()

                elif dato=="Fo Visita Tecnica".upper():
                    driver.find_element(by=By.XPATH, value='//*[@data-value="VTFO" and contains(text(),"FO Visita Tecnica")]').click()
                else:                    
                    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            def selector_tipo_regional(self):
                for i in range(3):
                    try:
                        element=driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Region"]')
                        actions = ActionChains(driver)
                        actions.move_to_element(element)
                        actions.perform()                        
                        break
                    except:
                        continue
                
                driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Region"]').click()

                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-label="BACK_Region"]')))
                region=data[4].lower().strip()

                if region=='nor oriente' or region=='nororiente' or region=="oriente":
                    driver.find_element(by=By.XPATH, value='//*[@data-value="4" and contains(text(),"Nor Oriente")]').click()
                elif region=='occidente':
                    driver.find_element(by=By.XPATH, value='//*[@data-value="5" and contains(text(),"Occidente")]').click()
                elif region=='nor occidente':
                    driver.find_element(by=By.XPATH, value='//*[@data-value="5" and contains(text(),"Nor Occidente")]').click()
                elif region=='centro':
                    driver.find_element(by=By.XPATH, value='//*[@data-value="1" and contains(text(),"Centro")]').click()
                    #

            def campo_aliado_cgo(self):
                for i in range(3):
                    try:
                        element=driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Aliado CGO"]')
                        actions = ActionChains(driver)
                        actions.move_to_element(element)
                        actions.perform()                        
                        break
                    except:
                        continue                
                driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Aliado CGO"]').click()
                driver.find_element(by=By.XPATH, value='//*[@data-value="GND"]').click()
            
            def campo_tipo_cliente(self):
                for i in range(3):
                    try:
                        element=driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Tipo Cliente"]')
                        actions = ActionChains(driver)
                        actions.move_to_element(element)
                        actions.perform()
                        del element
                        break
                    except:
                        continue
                
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@data-label="BACK_Tipo Cliente"]')))
                x=0
                while x<=3:
                    try:
                        driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Tipo Cliente"]').click()                    
                        break
                    except Exception as e:
                        time.sleep(1)
                        x+=1
                
                dato=data[7].upper().strip()                
                if dato=="MASIVO":
                    driver.find_element(by=By.XPATH, value='//*[@data-value="RE" and contains(text(),"Masivo")]').click()
                elif dato=="DTH":
                    driver.find_element(by=By.XPATH, value='//*[@data-value="DT" and contains(text(),"DTH")]').click()
                elif dato=="PYMES":
                    driver.find_element(by=By.XPATH, value='//*[@data-value="PY" and contains(text(),"Pymes")]').click()
                elif dato=='FIBRA OPTICA':
                    driver.find_element(by=By.XPATH, value='//*[@data-value="FO" and contains(text(),"Fibra Optica")]').click()
                else:
                    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            def campo_aliado(self):
                for i in range(3):
                    try:
                        element=driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Aliado"]')
                        actions = ActionChains(driver)
                        actions.move_to_element(element)
                        actions.perform()
                        del element
                        break
                    except:
                        continue  
                
                driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Aliado"]').click()
                if self.Ciudad=="Bogota" or self.Ciudad=="Bucaramanga":
                    driver.find_element(by=By.XPATH, value='//*[@aria-label="CLARO - CLARO"]').click()
                else:
                    if data[12].strip()=='CICSA COLOMBIA S.A.':
                        driver.find_element(by=By.XPATH, value='//*[@aria-label="9001113432 - Cicsa"]').click()
                    elif data[12].strip()=='DICO TELECOMUNICACIONES S.A.':
                        driver.find_element(by=By.XPATH, value='//*[@aria-label="8301361620 - Dico"]').click()
                    elif data[12].strip()=='TELCOS INGENIERIA S.A.':
                        driver.find_element(by=By.XPATH, value='//*[@aria-label="9000424742 - Telcos"]').click()
                    else:
                        driver.find_element(by=By.XPATH, value='//*[@aria-label="9000424742 - Telcos"]').click()
        


            def detalle_gestion(self):
                for i in range(3):
                    try:
                        element=driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Detalle Gestion"]')
                        actions = ActionChains(driver)
                        actions.move_to_element(element)
                        actions.perform()
                        del element
                        break
                    except Exception as e:
                        print("="*3,e)
                        continue                          
                driver.find_element(by=By.XPATH, value='//input[@data-label="BACK_Detalle Gestion"]').click()                                
                DetGes=data[0].lower().strip()
                
                if self.Ciudad=="Bogota":                                            
                    driver.find_element(by=By.XPATH, value='//*[@ aria-label="Visita completada"]').click()
                else:
                    if DetGes in ["cierre ot manual","gestión visitas técnicas","registro ot/lls m.e.r",'gestion backlog']:
                        driver.find_element(by=By.XPATH, value='//*[@ aria-label="Visita completada"]').click()
                    elif DetGes in 'contención de visitas':
                        driver.find_element(by=By.XPATH, value='//*[@aria-label="Cancelada"]').click()
                    elif DetGes=='gestión incidentes':
                        driver.find_element(by=By.XPATH, value='//*[@aria-label="Soporte de @ , Telefonía y TV"]').click()                    
                    else:
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()                
                    
                    



                #elif data[0]=="SOPORTE INTERNO":
                #    driver.find_element(by=By.XPATH, value='//*[@data-value="DSDE04"]').click()
            
            tipo_gestion(self)
            CausaGestion(self)
            campo_aliado_cgo(self)
            selector_tipo_actividad(self)                       
            selector_tipo_regional(self)
            Reprogramaciones(self)  
            campo_tipo_cliente(self)                
            campo_aliado(self)             
            detalle_gestion(self)
                    
            
                                            
            
            time.sleep(0.5)
        

            def campo_fecha(self):
                driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Fecha de Gestión"]').send_keys(data[2].replace("/","-"))
            def campo_ot(self):
                driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_OT Backoffice"]').send_keys(data[5].strip())
            def campo_cuenta(self):
                driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_CTA Bacoffice"]').send_keys(data[6].strip())
            def campo_nombre(self):
                driver.find_element(by=By.XPATH, value='p[1309]').send_keys(data[8].strip())
            def campo_direccion(self):
                driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Dirección"]').send_keys(data[9].strip())
            def campo_ciudad(self):
                driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Ciudad"]').send_keys(data[10].strip())
            def campo_nodo(self):
                driver.find_element(by=By.XPATH, value='//*[@aria-label="ID Nodo, Requerido"]').send_keys(data[11].strip())
            def campo_notas(self):
                driver.find_element(by=By.XPATH, value='//*[@data-label="BACK_Notas Causa"]').send_keys(data[15].strip())

            time.sleep(1)
            campo_fecha(self)
            campo_ot(self)
            # insertar cuenta
            campo_cuenta(self)                        
            # insertar nombre direccion
            campo_direccion(self)
            #insertar ciudad
            campo_ciudad(self)
            #insertar nodo
            campo_nodo(self)
            #inseertar notas 
            campo_notas(self)

            time.sleep(1)
            
            #'//input[@data-label="BACK_Causa Gestión"]'
            ArrayGestionado=[]
            for i in ['//input[@data-label="BACK_Tipo Gestion"]','//input[@data-label="BACK_Aliado CGO"]','//*[@data-label="BACK_Fecha de Gestión"]',
                    '//input[@data-label="BACK_Tipo OT"]','//input[@data-label="BACK_Region"]','//*[@data-label="BACK_OT Backoffice"]',
                    '//*[@data-label="BACK_CTA Bacoffice"]','//input[@data-label="BACK_Tipo Cliente"]','//*[@data-label="BACK_Ciudad"]',
                    '//*[@aria-label="ID Nodo, Requerido"]','//input[@data-label="BACK_Aliado"]',
                    '//input[@data-label="BACK_Detalle Gestion"]','//*[@data-label="BACK_Notas Causa"]'
                    ]:
                                    
                try:                    
                    ArrayGestionado.append(driver.find_element(by=By.XPATH, value=i).get_attribute('value'))
                except Exception as e:
                    print(e)
                    ArrayGestionado.append("Error")
                finally:
                    del i
            
            
            tipo_trabajo="BACKOFFICE"
            tupla_estado=("creada OK","Error creando ot")
            #lista_revicion=[]                                            
            '''if revisa_tipo_gestion!="" and revisa_aliado_cgo!="" and revisa_fecha!="" \
                                                    and revisa_tipo_ot!="" and revisa_region!="" and revisa_ot!="" \
                                                    and revisa_cuenta!="" and revisa_tipo_cliente!="" and  revisa_nodo!="" and revisa_aliado!=""\
                                                    and revisa_gestion!="" and revisa_detalle!="" and revisa_nota!=""'''
            print("!",ArrayGestionado)
            if "Error" in ArrayGestionado or "" in ArrayGestionado:
                error=str(tupla_estado[1])
                button = driver.find_element(by=By.XPATH, value='//*[@class="button dismiss" and contains(text(),"Cancelar")]')
                driver.implicitly_wait(3)
                ActionChains(driver).move_to_element(button).click(button).perform()
                ErrorGestion=True                    
            else:
                ErrorGestion=False
                error=str(tupla_estado[0])
                driver.find_element(by=By.XPATH, value='//*[@class="button submit" and contains(text(),"OK")]').click()
            
                

            time.sleep(2)
            driver.implicitly_wait(0)
            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,'//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

            '''_ubicacion = driver.find_element(by=By.XPATH, value='//*[@id="screen-title"]').text
                                                #print(_ubicacion)
                                                if _ubicacion=="Agregar actividad":
                                                    try:
                                                        driver.implicitly_wait(5)
                                                        myDinamicElement=driver.find_element_by_css_selector('.CGrightButton')
                                                        try:
                                                            driver.implicitly_wait(4)
                                                            myDinamicElement=driver.find_element_by_css_selector('.CGrightButton').click()
                                                                
                                                        except WDE:
                                                            print("alla voy con mause clic al boton")
                                                            button = driver.find_element_by_css_selector(u".CGrightButton")
                                                            driver.implicitly_wait(10)
                                                            ActionChains(driver).move_to_element(button).click(button).perform()
                                                    except:
                                                        print("no hay ventana de confimacion")
                                                else:
                                                    pass
                                                    print("no hay ventana de confirmacio v.2")'''


            
            #print(IdRow)                
            
            ConectorDbMysql().FuncInsInfoOne(["SPR_UPD_ESTACCRE",[IdRow,error]])

            try:                    
                lista_contador.append(1)
                if len(lista_contador)==31:
                    driver.refresh()
                    lista_contador=[]                    
                    time.sleep(5)
            except:
                pass
            
            '''contadorCompletar+=1
                                                #if contadorCompletar==10:
                                                    #contadorCompletar=0
                                                    try:
                                                        selector_Completacion(self,idBot,Idactividad,3)
                                                    except:pass'''


        ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))
        driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
        time.sleep(1)
        while 1:
            BtnSalida=self.driver.find_element(by=By.XPATH, value='//*[@class="item-caption __logout __logout"]')
            if BtnSalida.is_displayed():
                BtnSalida.click()
                time.sleep(3)
                break
            else:
                pass
        driver.quit()
    except Exception as e:
        Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        print(Nomb_error)        
        ConectorDbMysql().FuncInsInfoOne("SPR_INS_ESTBOT",[idBot,"Error Creacion!"])
        try:
            driver.refresh()
            time.sleep(4)
            driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
            time.sleep(1)
            driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
            time.sleep(5)            
        except:pass
        try:
            driver.quit()
        except:pass