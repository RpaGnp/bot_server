#LIBRERIAS PARA CHROMEDRIVER***********************
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os

import time
import sys
import os
from datetime import datetime

from .GestorFiles import tempdriver
from ModulosApp.ModelDataBase import ConectorDbMysql

#modelo home
from .AutomatizacionesWf.ModuloSeguimiento import selector_Seguimiento
from .AutomatizacionesWf.ModuloSoporte import selector_Soporte
from .AutomatizacionesWf.ModuloCreacion import selector_Creacion
from .AutomatizacionesWf.ModuloCompletar import selector_Completacion
from .AutomatizacionesWf.ModuloConfirmacion import selector_Confirmacion
from .AutomatizacionesWf.ModuloDemora import selector_Demora
from .AutomatizacionesWf.ModuloTam import selector_MarTam
from .AutomatizacionesWf.ModuloValidaciones import selector_ValidacionesMg
from .AutomatizacionesWf.ModeloMultiMarc import SelectorMDCS
from .AutomatizacionesWf.ModuloHHPPEstratos import SelectorEsthhpp

from .AutomatizacionesMG.AgendarDx import SelectorAgendaDx
from .AutomatizacionesMG.AgendarOts import HandleAgendamiento
from .AutomatizacionesMG.ActualizarOts import SelectorActualizarOts
from .AutomatizacionesMG.CancelarAgendas import SelectorCancelarAgenda
from .AutomatizacionesMG.CancelaPinAgenda import handlepincancelar
from .AutomatizacionesMG.Moduloccot import handlemer

from .AutomatizacionesWf.ModuloExtAgenda import selector_extagenda
#from .AutomatizacionesWf.ModuloCompletarBack import selectorComBack
from .AutomatizacionesWf.ModuloCompletarBack2 import selectorComBack
from .AutomatizacionesWf.ModuloCancelarOts import SelectorCanOrden
from .AutomatizacionesWf.BotMonitorChats import BotMonitorChat
from .AutomatizacionesWf.ModuloRazones import SelectorNotasAuto

from .AutomatizacionesWf.ModuloNotasBacklog import SelectorNotas

#modelos mintic y pymes
from .MinticPymes.MinMultiMarc import SelectorMulMarcMYP
from pathlib import Path
import os
from dotenv import load_dotenv
from platform import platform

# Cargar las variables de entorno del archivo .env
load_dotenv()
BASEDIR = Path('.').absolute()


class GestorWf():
    """Automatizacion de wf para realizar Gestion actividades"""
    def __init__(self,idbot,idAct,NombreBot,arraygestion):       
        # self.Navegador = "Edge"#"Opera"#"firefox"#"Chrome"#,"Edge"
        self.Navegador = os.getenv('NAVEGADOR')
        print(self.Navegador)
        self.idbot=idbot
        self.idAct=idAct
        self.NombreBot=NombreBot
        self.Ciudad=arraygestion[2]
        self.Trabajo=arraygestion[1]
        self.hora = datetime.now().strftime("%H:%M:%S")
        self.fecha = datetime.now().strftime("'%d/%m/%Y'")       
        self.Jornada=datetime.now().strftime('%p')

        if 'Windows' in platform():


            print(self.Navegador)
            if self.Navegador == "Edge":
                edge_options = EdgeOptions()
                edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

            elif self.Navegador == "Opera":
                opera_options = OperaOptions()
                opera_options.binary_location = r'%s\AppData\Local\Programs\Opera\opera.exe' % os.path.expanduser('~')
                opera_options.add_argument('--start-maximized')
                self.driver = webdriver.Opera(executable_path=r'C:\dchrome\operadriver.exe', options=opera_options)

            elif self.Navegador == "Firefox":
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--private")
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)

            elif self.Navegador == "Chrome":
                chrome_options = ChromeOptions()
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                chrome_options.add_argument('--start-maximized')
                chrome_options.add_argument("--incognito")
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
                time.sleep(1) 

            else:
                raise ValueError(f"Navegador {self.Navegador} no soportado")

        else:
            print('The operating system is Linux\nWe will look for "chromedriver"')
            path = BASEDIR / 'driver/chromedriver'
            print('aqui abrimos chrome')
            print(path)
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--incognito")
            self.driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                options=chrome_options
            )
            self.driver.get('https://amx-res-co.etadirect.com/')
            self.driver.save_screenshot('./screenshot.png')

    def Login(self,Aplicativo,Usuario,Clave):
        driver=self.driver      
        Usuario=Usuario.strip()
        Clave=Clave.strip()        
        self.usuario = Usuario
        driver.maximize_window()
        if Aplicativo=="WFM":
            self.driver.get("https://amx-res-co.etadirect.com/")                
            
            # Espera explícita para el campo de usuario
            wait = WebDriverWait(self.driver, 30)
            username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
            
            # Limpiar y enviar el nombre de usuario
            username_field.clear()
            username_field.send_keys(self.usuario)
            self.driver.save_screenshot('./screenshot.png')
            
            # Espera explícita para el campo de contraseña
            password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
            
            # Limpiar y enviar la contraseña
            password_field.clear()
            password_field.send_keys(Clave)
            time.sleep(1)
            self.driver.execute_script('document.querySelector("#sign-in > div").click()')
            time.sleep(3)
            #while driver.find_element(By.XPATH,'//div[@id="wait"]').get_attribute("style")=="":
            #    time.sleep(1)
            '''except Exception as e:
                                        Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
                                        print("! error conexion: ", e, Nomb_error)'''
            self.driver.save_screenshot('./screenshot.png')

            if self.driver.title=="Oracle Field Service":                
                bucle=1
                while bucle<=2:
                    try:
                        myDinamicElement=self.driver.find_element(by=By.XPATH, value='//*[@id="username"]')
                        self.driver.find_element(by=By.XPATH, value='//*[@id="username"]').clear()
                        self.driver.find_element(by=By.XPATH, value='//*[@id="username"]').send_keys(Usuario)
                        time.sleep(2)
                        self.driver.find_element(by=By.XPATH, value='//*[@id="password"]').clear()
                        self.driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(Clave)
                        time.sleep(1)
                        self.driver.find_element(by=By.XPATH, value='//*[@id="delsession"]').click()
                        time.sleep(2)
                        self.driver.execute_script('document.querySelector("#sign-in > div").click()')
                        #intro=self.driver.find_element_by_name('user_submitted_login_form').click()
                        time.sleep(3)
                        #while driver.find_element(By.XPATH,'//div[@id="wait"]').get_attribute("style")=="":
                        #    time.sleep(1)
                        break
                    except Exception as e:
                        Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
                        print("! error conexion: ", e, Nomb_error)
                        bucle+=1
                print(bucle)

                if bucle>=2:
                    sql=("SPR_INS_ESTBOT",[self.idbot,"Error login"])
                    ConectorDbMysql().FuncInsInfoOne(sql)            
                    self.driver.quit()        
                else:
                    sql=("SPR_INS_ESTBOT",[self.idbot,"En labor"])
                    ConectorDbMysql().FuncInsInfoOne(sql)                    
                    #WebDriverWait(self.driver, 160).until(EC.visibility_of_element_located((By.XPATH,'//button[@aria-label="Ocultar árbol de recursos"]')))
                    print("Login 2 vez ok!")
                    #validar cambios de contraseñas            
                    element2=WebDriverWait(driver, 200).until(EC.invisibility_of_element_located((By.XPATH, '//div[@id="wait"]//div[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
                    time.sleep(1)            
                    print(driver.title)
                    if driver.title=="Cambiar contraseña - Oracle Field Service":
                        sql=("SPR_INS_ESTBOT",[self.idbot,"Error login"])
                        ConectorDbMysql().FuncInsInfoOne(sql)            
                        self.driver.quit()
                    else:
                        pass
                self.driver.save_screenshot('./screenshot.png')
  
            else:
                sql=("SPR_INS_ESTBOT",[self.idbot,"En labor"])
                ConectorDbMysql().FuncInsInfoOne(sql)                    
                #WebDriverWait(self.driver, 160).until(EC.visibility_of_element_located((By.XPATH,'//button[@aria-label="Ocultar árbol de recursos"]')))
                #validar cambios de contraseñas            
                element2=WebDriverWait(driver, 120).until(EC.invisibility_of_element_located((By.XPATH, '//div[@id="wait"]//div[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
                time.sleep(1)            
                print(driver.title)
                if driver.title=="Cambiar contraseña - Oracle Field Service":
                    sql=("SPR_INS_ESTBOT",[self.idbot,"Error login"])
                    ConectorDbMysql().FuncInsInfoOne(sql)            
                    self.driver.quit()
                else:
                    pass

                #print("entrada sin incovenientes")
            self.driver.save_screenshot('./screenshot.png')

        elif Aplicativo=="GLAPP":
            driver.get("https://mglapp.claro.com.co/catastro-warIns/view/MGL/template/login.xhtml")

            driver.implicitly_wait(60)
            myDinamicElement = driver.find_element(by=By.XPATH, value='//input[@id="usuario"]')

            driver.find_element(By.XPATH,value='//input[@id="usuario"]').clear()
            driver.find_element(By.XPATH,value='//input[@id="usuario"]').send_keys(Usuario)
            time.sleep(1)
            driver.find_element(By.XPATH,value='//input[@type="password"]').clear()
            driver.find_element(By.XPATH,value='//input[@type="password"]').send_keys(Clave)
            time.sleep(1)
            driver.find_element(By.XPATH,value='//input[@type="submit"]').click()
            time.sleep(5)
            if driver.current_url == "https://mglapp.claro.com.co/catastro-warIns/view/MGL/template/main.xhtml":
                sql=("SPR_INS_ESTBOT",[self.idbot,"En labor"])
                ConectorDbMysql().FuncInsInfoOne(sql)
            else:                
                driver.quit()        
                return



                    
        else:
            driver.get("https://moduloagenda.cable.net.co")
            
            driver.implicitly_wait(180)
            myDinamicElement = driver.find_element(by=By.XPATH, value='//*[@class="ico_Candado login_alertas"]')

            driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').clear()
            driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').send_keys(Usuario)
            element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="password"]')))
            time.sleep(1)
            driver.find_element(by=By.XPATH, value='//*[@type="password"]').clear()            
            driver.find_element(by=By.XPATH, value='//*[@type="password"]').send_keys(Clave)
            time.sleep(3)
            element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@name="Submit"]')))
            if driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').is_displayed():
                driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').click()
            time.sleep(2)            

            try:
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//nav[@class="ClaroTemplate-nav clearfix desktop-nav"]')))
            except:
                return False            

            if driver.current_url=='https://moduloagenda.cable.net.co/Modificar_password.php':                
                sql=("SPR_INS_ESTBOT",[self.idbot,"Error login"])
                ConectorDbMysql().FuncInsInfoOne(sql)
                driver.quit()
                del driver                

            if driver.current_url != "https://moduloagenda.cable.net.co/indexadmin.php":
                if driver.current_url=='https://moduloagenda.cable.net.co/Login.php':
                    driver.get("https://moduloagenda.cable.net.co/index.php")
                x=0
                while x<=2:          
                    try:
                        if driver.current_url=='https://moduloagenda.cable.net.co/Login.php':
                            driver.get("https://moduloagenda.cable.net.co/index.php")
                        driver.implicitly_wait(18)
                        driver.find_element(by=By.XPATH, value='//*[@class="ico_Candado login_alertas"]')

                        driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').clear()
                        driver.find_element(by=By.XPATH, value='//*[@onblur="validaRedUsuario(this.value)"]').send_keys(Usuario)
                        time.sleep(1)
                        element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="password"]')))
                        driver.find_element(by=By.XPATH, value='//*[@type="password"]').clear()
                        driver.find_element(by=By.XPATH, value='//*[@type="password"]').send_keys(Clave)
                        time.sleep(2)
                        intro = driver.find_element(by=By.XPATH, value='//*[@name="Submit"]').click()
                        time.sleep(1)
                        if driver.current_url == 'https://moduloagenda.cable.net.co/indexadmin.php':
                            break
                        else:
                            x+=1
                    except:
                        driver.refresh()
                        time.sleep(5)
                        x+=1                
                if x>2:
                    sql=("SPR_INS_ESTBOT",[self.idbot,"Error login"])
                    ConectorDbMysql().FuncInsInfoOne(sql)            
                    self.driver.quit()        
                else:
                    sql=("SPR_INS_ESTBOT",[self.idbot,"En labor"])
                    ConectorDbMysql().FuncInsInfoOne(sql)
                
            else:
                sql=("SPR_INS_ESTBOT",[self.idbot,"En labor"])
                ConectorDbMysql().FuncInsInfoOne(sql)

        self.driver.save_screenshot('./screenshot.png')

        validador=0
        while validador<=90:
            data=ConectorDbMysql().FuncGetInfoOne(1,"SPR_GET_ESTLOG",[self.idbot])
            print("!",data[0])
            if data[0]=="Error login":
                print("esperando actualizacion de credenciales")
                time.sleep(10)
                ConectorDbMysql().RepActividad(self.idbot)
                validador+=1
            elif data[0]=="En labor":
                break
            else:
                break

        self.driver.save_screenshot('./screenshot.png')

        Dato=ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES",[self.idbot]))        
        if Dato[0]!=None:            
            if Dato[0]=="Eliminar":                       
                ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT",[self.idbot,self.idAct,'Detenido por usuario']))
                driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
                time.sleep(1)                                
                return
        else:
            pass
        print("="*10,"Login ok")
    
        self.driver.save_screenshot('./screenshot.png')


    def ExpanderCiudad(self,Ciudad,ubicacion):
        #print(ArrayTecSaludo)
            #try:
            driver=self.driver
            try:
                if driver.find_element(by=By.XPATH, value='//*[@title="Consola de despacho"]').is_displayed()==False:
                    driver.find_element(by=By.XPATH, value='//*[@class="page-header-back-button"]').click()
                    time.sleep(2)
                else:
                    pass
                driver.find_element(by=By.XPATH, value='//*[@title="Consola de despacho"]').click()
            except Exception as e:
                print(e)
            
            if Ciudad=="Bogota":
                try:                
                    driver.implicitly_wait(5)
                    #element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#manage-content > div > div.toa-twopanel-first-panel.toa-twopanel.toa-twopanel-vertical > div.toa-twopanel-first-panel.ui-droppable > div > div.toa-panel-content.edtree > div.edt-root > div.edt-item > div.edt-children > div:nth-child(2) > div.edt-row.toa-layout-hbox > button.edt-open.icr.ptplus')))
                    time.sleep(3)                    
                    expander1='/html/body/div[14]/div[1]/main/div/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/div[1]/button[1]'                    

                    if "Ampliar" in driver.find_element(By.XPATH,expander1).get_attribute('aria-label'):
                        driver.find_element(By.XPATH,expander1).click()                        
                    
                    time.sleep(1)
                    if int(ubicacion)==1:
                        driver.find_elements(by=By.XPATH, value='//*[contains(text(),"BACKOFFICE GNP CENTRO 2")]')[0].click()
                    else:
                        driver.find_elements(by=By.XPATH, value='//*[contains(text(),"BACKOFFICE GNP CENTRO 3")]')[0].click()                                    
                except Exception as e:
                    print(e)
                    sql=("SPR_INS_ESTBOT",[self.idbot,"Error Arbol!"])
                    ConectorDbMysql().FuncInsInfoOne(sql)
                    driver.quit()
                    return

            elif Ciudad=="Cali":                
                try:
                    selector1='//*[@class="rtl-text rtl-prov-name" and contains(text(),"REGION OCCIDENTE")]/ancestor::div[1]/button[1]'
                    selector2='//div[@class="edt-children"]//span[@class="rtl-text rtl-prov-name" and contains(text(),"BACKOFFICE")]/ancestor::div[1]/button[1]'
                    #selector3='//*[@id="manage-content"]/div/div[2]/div[2]/div/div[2]/div[3]/div[3]/div[2]/div[3]/div[2]/div[2]/div[1]/button[1]'
                    driver.implicitly_wait(30)
                    element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, selector1)))
                    time.sleep(3)
                    if "Ampliar" in driver.find_elements(by=By.XPATH, value=selector1)[0].get_attribute('aria-label'):
                        driver.find_element(by=By.XPATH, value=selector1).click()                    
                    element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, selector2)))
                    time.sleep(1)
                    if "Ampliar" in driver.find_elements(by=By.XPATH, value=selector2)[0].get_attribute('aria-label'):
                        driver.find_element(by=By.XPATH, value=selector2).click()
                    
                    #ubicacion=int(ubicacion)+3

                    time.sleep(1)            
                    #if int(ubicacion)==1:
                    driver.find_elements(by=By.XPATH, value='//div[@aria-label="Árbol de recursos"]//span[contains(text(),"BACKOFFICE GNP OCCIDENTE 3")]')[1].click()
                    #else:
                        #elif int(ubicacion)==2:
                    #    driver.find_elements(By.XPATH,'//*[contains(text(),"BACKOFFICE GNP OCCIDENTE 3")]')[1].click()                        
                    #else:                        
                    #driver.find_elements(by=By.XPATH, value='//*[contains(text(),"BACKOFFICE GNP OCCIDENTE 1.")]')[0].click()
                    time.sleep(1)
                        

                except Exception as e:
                    ConectorDbMysql().FuncInsInfoOne(("SPR_INS_ESTBOT",[self.idbot,"Error Arbol!"]))
                    Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
                    print("! error conexion: ", e, Nomb_error)
                    driver.quit()
                    return

            else:
                try:
                    for i in ["R5 ORIENTE","R5 BACKOFFICE"]:
                        selector='//span[contains(text(),"'+str(i)+'")]/ancestor::button'    
                        idbtn=driver.find_elements(By.XPATH,selector)[0].get_attribute("data-label-pid")
                        if "Reducir" not in driver.find_element(By.XPATH,'//div[@data-id="%s"]/div[1]/button[1]'%idbtn).get_attribute('aria-label'):
                            driver.find_element(By.XPATH,'//div[@data-id="%s"]/div[1]/button[1]'%idbtn).click()                    
                        time.sleep(2)                                 
                    x='//div[@data-id="%s"]/div[@class="edt-children"]/div[@class="edt-item"]'%idbtn                
                    driver.find_elements(By.XPATH,x)[int(ubicacion)-1].click()
                except Exception as e:
                    print(e)
                    ConectorDbMysql().FuncInsInfoOne(("SPR_INS_ESTBOT",[self.idbot,"Error Arbol!"]))
                    driver.quit()
                    return

            #sql="UPDATE TBL_HTECNICOSYACTS SET TEC_CDETALLE2='Consultado', TEC_CDETALLE4='Movil saludada', TEC_CDETALLE5='"+str(mensajeEnviado)+"',TEC_CDETALLE6='"+str(self.hora)+"'  WHERE TEC_NIDROW='"+str(idRowTec)+"'"
            #Data=GestorSqlite().ConsMixta(sql)

            
            time.sleep(1)
            '''except Exception as e:
                                                                Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
                                                                print("! error saludo: ", e, Nomb_error)'''
            
    def ConfiBusqueda(self):
        driver=self.driver
        try:            
            driver.find_element(by=By.XPATH, value='//*[@placeholder="Buscar en actividades"]').click()        
            if driver.find_element(by=By.XPATH, value='//*[@id="search-bar-container"]').is_displayed():
                driver.find_element(by=By.XPATH, value='//*[@aria-label="Search Preference"]').click()
                if driver.find_element(by=By.XPATH, value='//*[@id="search-preference-page"]').is_displayed():
                    for i in[0,2,7,8,9,11,17,18,20,22,23,24,25,26,29,30,31,32,34,38,39,40]:
                        if driver.find_elements(by=By.XPATH, value='//*[@class="oj-radiocheckbox-icon oj-component-icon"]//input[@type="checkbox"]')[i].get_attribute('class')=="oj-checkbox oj-component oj-enabled oj-component-initnode":
                            driver.find_elements(by=By.XPATH, value='//*[@class="oj-radiocheckbox-icon oj-component-icon"]')[i].click()
                        else:pass

            #sin restriccion de tiempo
            driver.find_element(by=By.XPATH, value='//*[@aria-label="Back"]').click()
            time.sleep(0.5)
            driver.find_element(by=By.XPATH, value='//*[@class="global-header ui-dark"]').click()
        except Exception as e:
            print("Configuracion busquueda fallida! ",e)
            driver.find_element(by=By.XPATH, value='//*[@placeholder="Buscar en actividades"]').click()        
            
    def LauncherGestion(self,ciudad):                
        if self.Trabajo=='Marcar Seguimiento':
            selector_Seguimiento(self,self.idbot,self.idAct)
        elif self.Trabajo=='Marcar Demora':
            selector_Demora(self,self.idbot,self.idAct)
        elif self.Trabajo=='Marcar Confirmacion':
            selector_Confirmacion(self,self.idbot,self.idAct)

        elif self.Trabajo=='Marcacion Soporte':
            selector_Soporte(self,self.idbot,self.idAct)

        elif self.Trabajo=='Marcacion Multiple':
            SelectorMDCS(self,self.idbot,self.idAct)
        
        elif self.Trabajo=="Crear" or self.Trabajo=="Crear 'No programada'":
            if self.Trabajo=="Crear 'No programada'":
                ActPro=True
            else:
                ActPro=False
            selector_Creacion(self,self.idbot,self.idAct,ActPro)
        
        elif self.Trabajo=="Completar":
            selector_Completacion(self,self.idbot,self.idAct)

        elif self.Trabajo=="Completar Backlog":
            selectorComBack(self,self.idbot,self.idAct)

        elif self.Trabajo in ["Repara y Actualiza","Actualizar"]:
            selector_ValidacionesMg(self,self.idbot,self.idAct,self.Trabajo)

        elif self.Trabajo in ["Extraer Agenda"]:
            selector_extagenda(self,self.idbot,self.idAct)
        
        elif self.Trabajo=="Marcacion TAM":
            selector_MarTam(self,self.idbot,self.idAct,self.Ciudad)

        elif self.Trabajo=="Marcacion MiN & PY":
            SelectorMulMarcMYP(self,self.idbot,self.idAct)

        elif self.Trabajo in ["Gestion estratos","Gestion estratos MER","Gestion ots HHPP"]:
            SelectorEsthhpp(self,self.idbot,self.idAct,self.Trabajo)

        elif self.Trabajo in ["Agendar DX-RX"]:
            SelectorAgendaDx(self,self.idbot,self.idAct,self.Trabajo)

        elif self.Trabajo in ["Actualizar Agenda"]:
            SelectorActualizarOts(self,self.idbot,self.idAct,self.Trabajo)

        elif self.Trabajo in ["Cancelar Agenda"]:
            SelectorCancelarAgenda(self,self.idbot,self.idAct,self.Trabajo)

        elif self.Trabajo in ["Cancelar Agenda Pin"]:
            self.driver.save_screenshot('screenshot.png')
            handlepincancelar(self.driver).SelectorCancelarAgenda(self.idbot,self.idAct,self.Trabajo)
        
        elif self.Trabajo in ["Agendar Ots","Agendar->pin->cancelar"]:
            HandleAgendamiento(self.driver).SelectorAgendaOts(self.idbot,self.idAct,self.Trabajo)

        elif self.Trabajo in ["Cancelar WFM"]:
            SelectorCanOrden(self,self.idbot,self.idAct) 

        elif self.Trabajo in ["Interapps chat"]:
            ciudad="Cali"
            BotMonitorChat(self.idbot,self.idAct,ciudad,self.driver).vigilar() 
            
        elif self.Trabajo in ["Gestor Notas"]:
            SelectorNotasAuto(self.driver).VijilanteRazones(self.idbot,self.idAct,ciudad)

        elif self.Trabajo in ["Gestor Notas backlog"]:
            SelectorNotas(self.driver,self.idbot,self.idAct,ciudad).main()
        
        elif self.Trabajo in ["Cancelar pin y agenda"]:            
           handlepincancelar(self.driver).SelectorCancelarAgenda(self.idbot,self.idAct,self.Trabajo)

        elif self.Trabajo in ["Creacion CCOT"]:            
           handlemer(self.driver,self.idAct,self.idbot,self.usuario).main()

        else:
            print("!",self.Trabajo)
    
    def TearDown(self):
        self.driver.find_element(by=By.XPATH, value='//*[@data-bind="text: initials"]').click()
        time.sleep(1)
        while 1:
            BtnSalida=self.driver.find_element(by=By.XPATH, value='//*[@class="item-caption __logout __logout"]')
            if BtnSalida.is_displayed():
                BtnSalida.click()
                time.sleep(3)
                break
            else:
                pass
        print("Fin ejecucion Chrome!")
    
    def Killit(self):
        try:
            self.driver.find_element(By.XPATH,value='//div[@class="user-menu-region"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, value='//li[@class="user-menu-item" and @pos="2"]').click()
            time.sleep(5)  
        except:pass
        self.driver.quit()
#SelectorSaludo(9)