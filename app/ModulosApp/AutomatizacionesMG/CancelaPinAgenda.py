from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import sys
#from datetime import time as tmr
from .InteraccionesMG import BotMg
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *


##09/04/2024 SE DEBE MODIFICAR PARA FUNCIONAR UNICAMENTE CON UN USUARIO
class handlepincancelar:
    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(0)
        self.urlPin ="https://agendamiento.claro.com.co"
        self.urlcancela="https://agendamiento.claro.com.co"
        self.Bot=BotMg(driver)
        self.codefucntion ='''
            window.validaPinReagenda = function(conPin,btn,objs){
            console.log("validaPinReagenda inyectado")
            var codPin = $('#codPin').val();
            var resWS = $('#resWS').val();
            var celular = "321277781";
            var html = '';

            if(objs.accionFront == 'MGW_ACCION_REAGENDAR')
            {
                accionFrontServ = 'reagendar';
            }
            if(objs.accionFront == 'ACCION MGW_ACCION_ANULAR')
            {
                accionFrontServ = 'anular';
            }
            if(objs.accionFront == 'ACCION MGW_ACCION_CANCELAR')
            {
                accionFrontServ = 'cancelar';
            }

            if(codPin == '')
            {
                msg = 'Pin no puede estar vacio';
                title = 'Error '+accionFrontServ;
                optionsA = '';
                addDialogInside('err_popup_motivo_'+accionFrontServ, msg, optionsA, title);
            }
            $.ajax({
                type:'POST',
                url:'ajax_pin_reagendamiento.php',
                data:{
                    'ot':ot,
                    'type': type,
                    'cuenta':order.CUENTA,
                    'pin':codPin,
                    'metodo':'validarPin',
                    'validaConPin':conPin,
                    'btn':btn,
                    'celular':celular,
                    'resWS':resWS,
                    'accionFront': accionFrontServ,
                    'actionController': 'PinReagenda'
                },
                success:function(res){
                    obj = JSON.parse(res);            
                    conPin=true;
                    obj.valido='true';
                    obj.success=true;
                    obj.enable=true;
                    console.log(obj)
                    console.log("success")
                    console.log(objs.accion, objs.dft, objs.data, objs.dialog, objs.options)
                    if(conPin){
                        if(obj.valido == 'true'){
                            html += obj.message;
                            $('#res').html(html);
                            setTimeout(function(){
                                $('#dialog_pinReagenda').dialog("close");
                                if(btn != 'back'){
                                    console.log(btn)
                                    console.log(obj.enable)
                                    if(accionFrontServ == 'reagendar' && obj.enable)
                                    {
                                       console.log("enable reagendar")                               
                                        changeStatusStepXhr('capacity_reagendar', 'step1', 'capacity', 1);
                                        console.log("paso 1 ok")
                                       executeStepFlowXhr('capacity_reagendar', 'step2', [], 'capacity');
                                       console.log("paso 2 ok")
                                    }

                                    if(accionFrontServ == 'anular')
                                    {
                                        generarMensajePersonalizado(objs.accion, objs.dft, objs.data, objs.dialog, objs.options);
                                    }

                                    if(accionFrontServ == 'cancelar')
                                    {
                                        generarMensajePersonalizado(objs.accion, objs.dft, objs.data, objs.dialog, objs.options);
                                    }
                                }
                            },2000);

                        }else{
                            $(".ui-dialog-buttonpane button:contains('Validar')").button("disable");
                            html += obj.message;
                            $('#res').html(html);
                        }
                    }else{
                        $('#dialog_reagendaSinPin').dialog("close");
                        if(btn != 'back'){
                           generarMensajePersonalizado(objs.accion, objs.dft, objs.data, objs.dialog, objs.options);
                        }
                    }

                },
               error: function(jqXHR, textStatus, errorThrown){
                $(this).dialog("close");
                var config = {
                    width: 340,               
                    buttons: {
                        Volver: function () {
                            $(this).dialog('close');                        
                        }
                    }
                }
                addDialog('Error', 
                '<strong>No se pudo generar la petici\xf3n solicitada. Por favor, intente nuevamente. Si continua experimentando este inconveniente, por favor, contactar con el area de soporte.<strong>', 
                config, "Resultado"); 
               }
            });
         }

        '''        

    def CreadorVentanas(self,idAct,idbot):        

        sql="""
            SELECT ACB_CUSUAPL2,ACB_CCLAVEAPL2
            from tbl_hactividadesbot
            where ACB_NID=%s
            """%idAct
        
        '''credencialesAgenda = ConectorDbMysql().FuncGetInfo(1,sql)                
                                      self.driver.execute_script("window.open('');")
                                      self.driver.execute_script("window.focus();")
                                      self.driver.switch_to.window(self.driver.window_handles[-1])    
                                      x = self.Bot.Login(self.urlcancela,credencialesAgenda,idbot)  '''      

        #self.venPin = self.driver.window_handles[0]    
        #self.venAgenda = self.driver.window_handles[-1]

        return 1

    def mensajesModulo(self):               
        clases = self.driver.find_elements_by_css_selector("[class^='ui-dialog ']")                 
        for clase in clases:
            if "display: block;" in clase.get_attribute("style"):
                ErrorOrden = clase.text             
                print(ErrorOrden)
                if "Pin Generado satisfactoriamente." in ErrorOrden:
                    self.hideWindowPin()
                    return 1,1  
                if "Motivo de Re Agendamiento" in ErrorOrden:
                    self.AgendamientoDirecto()
                    return 1,0
                if "Señor usuario: el estado de la cuenta matriz no cuenta con un estado habilitado para agendar el tipo de trabajo seleccionado." in ErrorOrden:
                    #self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_Error"]//button').click()
                    return 0,0
                if "La orden de trabajo NO contiene en RR caracteristicas necesarias para agendamiento en Work Force. Por favor revisar en RR los campos basicos segun el tipo de trabajo" in ErrorOrden:
                    return 0,0
                if "Se ha superado el tiempo limite para agendar sobre esta franja, por favor seleccione otra." in ErrorOrden:                                                                                  
                    return 0,0
                    
                if "Error de Creacion de la Orden de Trabajo en Sistema Ya existe Agenda Recargar" in ErrorOrden:
                    return 0,0      
                if "Revisa nuevamente la capacidad. El cupo seleccionado ya fue asignado." in ErrorOrden:
                    return 0,0
                if 'El campo "Persona que atiende" no puede estar vacío' in ErrorOrden:
                    return 0,0
                if 'El campo "E-mail 2" no puede estar vacío' in ErrorOrden:
                    return 0,0
                if 'El campo "Numero Celular" no puede estar vacío' in ErrorOrden:
                    return 0,0
                if "Usuario no tiene permisos para agendar sobre este tipo de trabajo" in ErrorOrden:
                    return 0,0
                if "Error de conexión con EtaDirect por favor intente mas tarde..." in ErrorOrden:
                    return 0,0
                if "SubTipo de Trabajo no definido" in ErrorOrden:
                    return 0,0
        return 1,1

    def GetVentcancela(self):
        self.driver.switch_to.window(self.venAgenda)

    def GetVentcancelaPin(self):
        self.driver.switch_to.window(self.venPin)

    def GetBoton(self):
        DicButton={}
        Cancelar=False
        for buttonAccion in self.driver.find_elements(By.XPATH,'//div[@class="buttons-form"]/input'):
            DicButton.update({buttonAccion.get_attribute("value"):buttonAccion.get_attribute("style")})
            if buttonAccion.get_attribute("style")=='display: inline-block;' and buttonAccion.get_attribute('value') == "Cancelar":
                #print(buttonAccion.get_attribute('value'),buttonAccion.get_attribute("style"))
                buttonAccion.click()                
                try:
                    element = WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))                    
                    Cancelar=True
                except:
                    break
                else:
                    continue

        return Cancelar,DicButton
    
    def CancelarDirecto(self):
        
        # aplica para REQ cuando no se solicite pin
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]')))
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//textarea').send_keys("Cancelacion")
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//input[@type="submit"]').click()
        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_cancelar_orden"]')))
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_cancelar_orden"]//button/span[contains(text(),"Confirmar")]').click()
        WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))

    def CancelarPin(self):
        # esperar a la ventana de envio de pin y generar el pin
        try:
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]')))
        except Exception as e:
            print("="*10,e)
            self.CancelarDirecto()
            return 0

        # self.CancelarDirecto()

        time.sleep(1)
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//textarea').send_keys('Envío pin cancelacion')
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//input[@type="submit"]').click()
        # /html/body/div[8]
        # //*[@id="dialog_msg_popup_cancelar_orden"]
        # WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))
        try:
            # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]')))   
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_msg_popup_cancelar_orden"]')))

            # time.sleep(3)
            # self.driver.find_element(By.ID, "dialog_msg_popup_cancelar_orden")
            self.driver.find_element(By.XPATH,'/html/body/div[8]/div[3]/div/button[1]').click()
            return 0
        except:
            return 1

        Resultado=self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]//tr').text

    def CancelarAgenda(self):
        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]')))
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//textarea').send_keys("Cancelacion")
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_motivo_cancelar"]//input[@type="submit"]').click()

    def waitWindowValPin(self):
        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_cancelar_orden"]')))
        self.driver.find_element(By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_cancelar_orden"]//button/span[contains(text(),"Confirmar")]').click()
        WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))

    def WindowConfCancelacion(self):        

        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_pinReagenda"]')))
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//input[@id="codPin"]').send_keys(random.randint(1000, 9999))
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//span[@class="ui-button-text" and contains(text(),"Validar")]').click()        
        WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))

    def waitWindowCancelarOrden(self):
        msnModulo = self.mensajesModulo()
        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.XPATH,'//div[@aria-labelledby="ui-dialog-title-dialog_msg_popup_cancelar_orden"]')))
        time.sleep(0.5)
        self.driver.find_element(By.XPATH,'//span[contains(text(),"Confirmar")]').click()
        WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="modal-loading-ajax"]')))        

    def MainCancelacion(self,data):
        # hilo principal de consultas // no usado
        self.Bot.ConsultaOts(self.urlcancela,data[1],data[-1])
        EstadoOT = self.Bot.Validadorestadoot(self.urlcancela)                
        
        if EstadoOT!=1:
            ConectorDbMysql().FuncUpdSpr("spr_upd_estgesdx",[data[0],EstadoOT])
            return False

        EstadoOt=self.driver.find_element(By.XPATH,'//div[@id="estadoag"]').text
        time.sleep(3)
        Cancelar = self.GetBoton()            
        print(Cancelar)
        Resultado = ""
        if Cancelar[0]:
            self.CancelarPin()
            # ====================cancelar la orden =====================
            #driver.get(self.urlPin)
            #self.driver.switch_to.window(self.venPin)
            time.sleep(1)
            # esperar modal para ingresar el pin 

            self.driver.execute_script(self.codefucntion)

            #self.Bot.ConsultaOts(self.urlPin,data[1],data[5])
            self.WindowConfCancelacion()
            self.waitWindowCancelarOrden()
            '''#CancelarAgenda = self.GetBoton()
            if CancelarAgenda:
                                                   # cancelar agenda
                                                    self.CancelarAgenda()
                                                    Resultado += " Ot cancelada con exito"'''
        else:
            Resultado=f"No se puede Gestionar, Boton cancelar no aparece {Cancelar[1]} {EstadoOt}"

        return Resultado

    def SelectorCancelarAgenda(self,idbot,idAct,Trabajo):
        # funcion principal 
        driver=self.driver        
        self.CreadorVentanas(idAct,idbot)
        
        sql="""
            SELECT dx_nid,dx_corden,dx_caliado,dx_cciudad,dx_dfechaage,dx_cobservacion
            FROM tbl_hagndasdxrx
            WHERE dx_nidbot='"""+str(idAct)+"""' AND  dx_cestgestion='Pendiente';
        """
        array_datos=ConectorDbMysql().FuncGetInfo(0,sql)
        try:
            for data in array_datos:
                print("!",data)
                ConectorDbMysql().RepActividad(idbot)  

                # self.urlPin ="https://agendamiento.claro.com.co"
                # self.urlcancela="https://agendamiento.claro.com.co"
                self.Bot.ConsultaOts(self.urlPin,data[1],data[5])
                #driver.switch_to.window(self.venPin)                
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

                EstadoOT = self.Bot.Validadorestadoot(self.urlcancela)        
                print(EstadoOT)

                #self.Bot.ConsultaOts(self.urlcancela,data[1],data[-1])
                
                if EstadoOT!=1:
                    ConectorDbMysql().FuncUpdSpr("spr_upd_estgesdx",[data[0],EstadoOT])
                    continue
                    #return False

                EstadoOt=self.driver.find_element(By.XPATH,'//div[@id="estadoag"]').text
                Cancelar = self.GetBoton()            
                print(Cancelar)
                time.sleep(3)

                Resultado = ""
                if Cancelar[0]:
                    if self.CancelarPin():
                        # ====================cancelar la orden =====================                    
                        #self.driver.switch_to.window(self.venPin)                    
                        time.sleep(1)
                        self.driver.execute_script(self.codefucntion)                    
                        self.WindowConfCancelacion()
                        self.waitWindowCancelarOrden()
                        Resultado = "Ot cancelada pin generado ok"
                    else:
                        Resultado = "Ot cancelada pin nogenerado ok"

                    #self.Bot.ConsultaOts(self.urlcancela,data[1],data[5])
                    
                    '''CancelarAgenda = self.GetBoton()  # click en cacelar
                                                                                print(CancelarAgenda)
                                                                                if CancelarAgenda:
                                                                                   # cancelar agenda
                                                                                    self.CancelarAgenda()# esperas
                                                                                    Resultado += " Ot cancelada con exito"'''
                else:
                    Resultado=f"No se puede Gestionar, Boton cancelar no aparece {Cancelar[1]} {EstadoOt}"

                #return Resultado
                if  Resultado== False:
                    ConectorDbMysql().FuncInsInfoOne(("spr_upd_estgesdx", [data[0], Resultado]))
                    continue
                    
                ##============================// continuar cancelando la orden //============================
                ConectorDbMysql().FuncInsInfoOne(("spr_upd_estgesdx", [data[0], Resultado]))


            ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idbot, idAct, 'Labor Terminada']))
            driver.quit()

        except Exception as e:
            Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
            print(Nomb_error)
            try:
                sql = ("spr_upd_estgesdx", [data[0], 'Orden no gestionada error ot!'])
                ConectorDbMysql().FuncInsInfoOne(sql)
            except:
                pass
            driver.quit()