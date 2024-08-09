import ctypes
import sys
import os
import subprocess
import urllib.request
import urllib.error
import zipfile
import xml.etree.ElementTree as elemTree
import logging
import re

import base64
from pathlib import Path
from io import BytesIO
import pymysql

from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Acceder a las variables de entorno
DB_HOST_ALAMO = os.getenv('DB_HOST_ALAMO')
DB_NAME_ALAMO = os.getenv('DB_NAME_ALAMO')
DB_USER_ALAMO = os.getenv('DB_USER_ALAMO')
DB_PASSWORD_ALAMO = os.getenv('DB_PASSWORD_ALAMO')

def ConexionDbAlamo():
    try:
        conn = pymysql.connect(
            host=DB_HOST_ALAMO, 
            database=DB_NAME_ALAMO, 
            user=DB_USER_ALAMO, 
            password=DB_PASSWORD_ALAMO
            )
        return conn
    except:
        return False
    
def ComprobarVersion(self,nombre_bot):
    conn=ConexionDbAlamo()
    if conn!=False:
        cursor=conn.cursor()
        cursor.callproc("spr_get_versoft",[nombre_bot])
        data=cursor.fetchall()
        cursor.close()
        conn.close()
        del cursor,conn
        print(data)
        for i in data:
            verAlamo=i[0]

        if verAlamo==None:
            verAlamo=float(1.0)
        else:
            pass

        return verAlamo
    else:
        return False

#ComprobarVersion('bot_server')

def download_actualizacion(self,nombre_bot,version):     

    conn=ConexionDbAlamo()
    cursor=conn.cursor()
    cursor.callproc("spr_get_soft",[nombre_bot,version])
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    nombre_bot=self.EjecutablePrograma
    del conn,cursor
    for i in datos:
        version = str(i[1])
        extencion = str(i[2])
        detalles = str(i[3])
        dato_encriptado = i[0]
        dato_encriptado = dato_encriptado[2:-1]
        dato_encriptado = dato_encriptado.encode('ascii')
        decoded = base64.b64decode(dato_encriptado)
    nombre_carpeta = os.getcwd()        
    file_name = f"{nombre_carpeta}\\act_{self.EjecutablePrograma}"
    print(file_name)
    with open(file_name, "wb") as f:
        f.write(decoded)


    #os.rename(file_name,f"{file_name}.exe")
    #file_name=f"{file_name}.exe"
    #=================crear un archivo actualizador a cada bot======================
    #ruta_escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_actualizador = f"{nombre_carpeta}\\actualizar_{nombre_bot}.bat"
    ruta_lanzador = f"{nombre_carpeta}\\lanzador_{nombre_bot}.bat"
    file_bot=f"{nombre_carpeta}\\{nombre_bot}"
    #print(file_actualizador)
    if os.path.isfile(file_actualizador):
        os.remove(file_actualizador)
    else:
        pass

    f = open(file_actualizador, "w")
    command = '''
            @Echo OFF

            TimeOut /T 5

            taskkill -im '''+str(self.EjecutablePrograma)+''' -f

            TimeOut /T 3

            DEL /F /Q ''' + str(self.EjecutablePrograma) + '''

            REN ''' + str(file_name) + ''' ''' + str(self.EjecutablePrograma) + '''

            START ''' + str(self.EjecutablePrograma) + '''
            
            DEL /F /Q ''' + str(file_name) + '''.bat
            
            DEL /F /Q ''' + str(ruta_lanzador) + '''

            



            Exit

        '''
    f.write(command)
    f.close()
    ctypes.windll.kernel32.SetFileAttributesW(file_actualizador, 2)# ocultar archivo
    #===== crear el iniciador del archivo actualizador===========================
    '''debido a que os.sytem no es capaz de ejecutar el archivo actualizador sin salirse del 
    hilo principal se debe crear un lanzador para ejecutar el actualizador bat de cada bot'''


    if os.path.isfile(ruta_lanzador):
        os.remove(ruta_lanzador)
    else:
        pass
    '''cursor.execute("UPDATE TBL_CONTROL_BOT SET CON_DETALLE_5=? WHERE CON_NOMBRE_BOT=?",version,nombre_bot)
                cursor.commit()
                cursor.close()
                conn.close()'''

    file = open(ruta_lanzador, "w")
    file.write(f'start /d "{nombre_carpeta}" {file_actualizador}')
    file.close()
    ctypes.windll.kernel32.SetFileAttributesW(ruta_lanzador, 2)  # ocultar archivo
    os.system(ruta_lanzador)


    
#download_actualizacion("anydesk",'1.0')