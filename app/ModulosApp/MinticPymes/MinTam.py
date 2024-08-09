import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from ..ModelDataBase import ConectorDbMysql
from funciones_varias import *
from reloj_casio import *


def FunGuardar(self,ArrayGestion):
	sql=("SPR_UPD_ESTACTM",ArrayGestion)
	ConectorDbMysql().FuncInsInfoOne(sql)


def selector_MarTam(self,idBot,Idactividad):
    driver=self.driver

    try:
        sql = """
    		SELECT ACM_NID,ACM_CORDEN,ACM_CCUENTA,ACM_CMISELANEOS0
    		FROM tbl_hactmarcacionbot
    		WHERE ACM_NIDBOT='""" + str(Idactividad) + """' AND  ACM_CESTADOOT='Pendiente';
    	"""
        array_datos = ConectorDbMysql().FuncGetInfo(0, sql)
        lista_refresh = []

        for i, data in enumerate(array_datos):
            data = [data[0], data[1]]
            print(data)

            lista_refresh.append(data[1])
            if len(lista_refresh) == 30:
                driver.refresh()
                lista_refresh = []

            ConectorDbMysql().RepActividad(idBot)
            # funcion de salida, pausa del bot
            Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idBot]))
            # print(Dato[0])
            if Dato[0] != None:
                if Dato[0] == "Pausar":
                    while 1:
                        ConectorDbMysql().RepActividad(idBot)
                        time.sleep(3)
                        Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idBot]))
                        if Dato[0] != None:
                            if Dato[0] == "Reanudar":
                                ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_ESTBOTGES", [idBot]))
                                break
                        elif Dato[0] == "Eliminar":
                            ConectorDbMysql().FuncInsInfoOne(
                                ("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
                            driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
                            time.sleep(1)
                            while 1:
                                BtnSalida = self.driver.find_element_by_xpath(
                                    '//*[@class="item-caption __logout __logout"]')
                                if BtnSalida.is_displayed():
                                    BtnSalida.click()
                                    time.sleep(3)
                                    break
                                else:
                                    pass
                            driver.quit()
                            return

                elif Dato[0] == "Eliminar":
                    ConectorDbMysql().FuncInsInfoOne(
                        ("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))
                    driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
                    time.sleep(1)
                    while 1:
                        BtnSalida = self.driver.find_element_by_xpath(
                            '//*[@class="item-caption __logout __logout"]')
                        if BtnSalida.is_displayed():
                            BtnSalida.click()
                            time.sleep(3)
                            break
                        else:
                            pass
                    driver.quit()
                    return
            else:
                pass

            element = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="GlobalSearch"]')))
            lupa = driver.find_element_by_xpath('//*[@type="search"]')
            # print(lupa.is_displayed())
            if lupa.is_displayed() == False:
                driver.find_element_by_xpath('//*[@aria-label="GlobalSearch"]').click()
            else:
                pass
            time.sleep(0.50)
            driver.execute_script('document.querySelector("#search-bar-container > div.oj-flex-item.oj-sm-12 > div > div.search-bar-input-element-wrap > div > div.search-bar-input-hint-text").click()')
            driver.find_element_by_xpath('//*[@class="search-bar-input"]').clear()
            driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(data[1])
            driver.find_element_by_xpath('//*[@class="search-bar-input"]').send_keys(Keys.ENTER)

            try:
                element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
            except Exception as e:
                Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e

                FunGuardar(self, [data[0], 'Marcacion Tam Fallida'])
                compuerta = False
                continue

            if driver.find_element_by_xpath('//*[@class="toa-search-empty"]').text != "":
                compuerta = False
                continue
            else:
                pass

            _lista_lls = ""
            _fecha_hoy = fecha_actual(self)
            # print("*",_fecha_hoy)

            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="found-item-activity"]')))
            _lista_lls = driver.find_elements_by_xpath('//*[@class="found-item-activity"]')
            if len(_lista_lls) == 0:
                tokens = []
                FunGuardar(self, [data[0], 'Marcacion TAM Fallida'])
                compuerta = False
                continue

            for i in range(len(_lista_lls)):
                gs = 0
                while gs < 5:
                    try:
                        fecha_Ot = driver.find_elements_by_xpath('//*[@class="activity-date"]')[i].text
                        time.sleep(0.5)
                        x = driver.find_elements_by_xpath('//*[@class="activity-icon icon"]')[i].get_attribute("style")
                        break
                    except:
                        time.sleep(1)
                        gs += 1
                #amarillo,gris,naranjado,verde oscuro, verde claro,rojo  https://convertingcolors.com/
                if x == "background-color: rgb(255, 255, 38); border: 1px solid rgb(204, 204, 30);"\
                    or x == "background-color: rgb(156, 162, 173); border: 1px solid rgb(124, 129, 138);" \
                    or x == "background-color: rgb(255, 172, 99); border: 1px solid rgb(204, 137, 79);" \
                    or x == 'background-color: rgb(167, 209, 0); border: 1px solid rgb(133, 167, 0);'\
                    or x=="background-color: rgb(255, 50, 17); border: 1px solid rgb(204, 40, 13);"\
                    or x=="background-color: rgb(30, 133, 37); border: 1px solid rgb(24, 106, 29);":

                    if fecha_Ot == _fecha_hoy[0] or fecha_Ot == "":
                        driver.find_elements_by_xpath('//*[@class="activity-title"]')[i].click()
                        driver.implicitly_wait(0)
                        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located(
                            (By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
                        compuerta = True
                        break
                    else:
                        compuerta = False
                        continue
                else:
                    compuerta = False
                    continue

            if compuerta == False:
                FunGuardar(self, [data[0], 'Marcacion TAM Fallida'])
                compuerta = False
                continue
            else:
                pass

            driver.find_element_by_xpath('//*[@class="button inline" and contains(text(),"Backoffice")]').click()
            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

            # ===================================== ingreso al formulario=============================================================
            driver.find_element_by_xpath('//*[@role="button" and contains(text(),"TAM")]').click()

            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="loading-animated-icon big jbf-init-loading-indicator"]')))

            time.sleep(1)

            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@type="submit" and contains(text(),"OK")]')))
            except Exception as e:
                for i in range(2):
                    driver.back()
                FunGuardar(self, [data[0], 'Marcacion Demora Fallida'])
                compuerta = False
                continue

            tokens = []

            def AliadoCND():
                if driver.find_element_by_xpath('//*[@data-label="aliadoTAM"]').get_attribute("value") != "2":
                    driver.find_element_by_xpath('//*[@value="2" and contains(text(),"GNP")]').click()
                else:
                    pass

            AliadoCND()


            def CausaSolicitudTAM():
                if driver.find_element_by_xpath('//*[@data-label="Conf_Caus"]').get_attribute("value") != "SGV":
                    driver.find_element_by_xpath('//*[contains(text(),"Seguimiento visita")]').click()
                else:
                    pass
            CausaSolicitudTAM()

            def NotasCausa():
                if "Seguimiento visita Tam" not in driver.find_element_by_xpath('//*[@data-label="Conf_Not_Causa"]').get_attribute("value"):
                    driver.find_element_by_xpath('//*[@data-label="Conf_Not_Causa"]').send_keys("Seguimiento visita Tam")

            NotasCausa()

            def GestionTAM():
                if driver.find_element_by_xpath('//*[@data-label="Conf_Gest"]').get_attribute("value") != "6":
                    driver.find_element_by_xpath('//*[@value="6" and contains(text(),"Seguimiento visita")]').click()
                else:
                    pass
            GestionTAM()

            def NotasGesTAM():
                if "Seguimiento visita Tam" not in driver.find_element_by_xpath('//*[@data-label="Conf_Not_Gest"]').get_attribute("value"):
                    driver.find_element_by_xpath('//*[@data-label="Conf_Not_Gest"]').send_keys("Seguimiento visita Tam")

            NotasGesTAM()

            driver.find_element_by_xpath('//*[@type="submit" and contains(text(),"OK")]').click()
            try:
                WebDriverWait(driver, 90).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class=""loading-animated-icon big jbf-init-loading-indicator""]')))
            except:
                pass
            time.sleep(0.5)

            try:
                error1 = driver.find_element_by_xpath(
                    '//*[contains(text(),"No se pudo procesar la solicitud. Siga trabajando o póngase en contacto con el administrador para obtener ayuda.")]')
                if error1.is_displayed() == True:
                    driver.find_element_by_xpath('//*[@id="notification-clear"]').click()
                    driver.find_elements_by_xpath('//*[@class="button dismiss"]')[1].click()
            except:
                pass

            try:
                time.sleep(0.5)
                error2 = driver.find_element_by_xpath(
                    '//*[contains(text(),"Los cambios no se han enviado. ¿Desea guardar un borrador de las actualizaciones?")]')
                if error2.is_displayed() == True:
                    driver.find_element_by_xpath('//*[@class="button submit" and contains(text(),"Sí")]').click()
            except:
                pass

            time.sleep(1)
            try:
                driver.find_element_by_xpath(
                    '//*[@class="app-button-title" and contains(text(),"Consola de Despacho")]').click()
            except:
                salida_ot_marcada(driver)
            Primera_ot = True

            sql = ("SPR_UPD_ESTACTM", [data[0], 'Tam marcada con exito'])
            ConectorDbMysql().FuncInsInfoOne(sql)
            # si aparece la ventana de confirmacion darle continuar********************************************
            time.sleep(0.5)
        # salida_adelantos(driver)

        ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Labor Terminada']))
        time.sleep(5)
        driver.quit()

    except Exception as e:
        Nomb_error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        print(Nomb_error)
        try:
            driver.refresh()
            time.sleep(3)
            driver.find_element_by_xpath('//*[@data-bind="text: initials"]').click()
            time.sleep(1)
        except:pass

        try:
            driver.quit()
        except:
            pass