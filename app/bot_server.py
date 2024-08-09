__version__=3.41
######
import sys
import os
import time
import random
import socket
from datetime import datetime
from getpass import getuser

from ModulosApp.ModelDataBase import ConectorDbMysql
from ModulosApp.ModuloAes import chipherAes
from ModulosApp.ModeloInfoPC import GetInfPC
from ModulosApp.ModeloLauncher import GestorLabor
from Actualizador_programa import *

from NotificaActividad import NotificaActividad

import schedule
import threading

import os
from dotenv import load_dotenv

# Definir la ruta al archivo .env
env_path = '.env'

# Comprobar si el archivo .env existe
if not os.path.exists(env_path):
    print(f"El archivo {env_path} no existe. No se puede iniciar el código.")
    sys.exit()


'''from Notificar import notificar_actividad
#from encriptar_256 import Credenciales_Conexion
from manejador_errores import manejador_errores
from reloj_casio import timer
#=================actualizador automatico==========================
from Actualizador_programa import download_actualizacion
'''


class Bot_server:
	def __init__(self):
		'''self.ruta_escritorio = f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\\ArchivosControlBots"
								if os.path.isdir(self.ruta_escritorio)==False:    
									os.mkdir(self.ruta_escritorio)
								else:
									pass'''

		comprobar_ruta=str(os.path.dirname(sys.argv[0]))
		if comprobar_ruta.strip()==None:
			self.EjecutablePrograma=str(os.path.basename(sys.executable))
			RutaEjecutablePrograma=str(os.path.dirname(sys.executable))
		elif comprobar_ruta.strip()=='':
			self.EjecutablePrograma=str(os.path.basename(sys.executable))
			RutaEjecutablePrograma=str(os.path.dirname(sys.executable))
		else:
			self.EjecutablePrograma=str(os.path.basename(sys.argv[0]))
			RutaEjecutablePrograma=str(os.path.dirname(sys.argv[0]))

		print('este es el bot: ', os.getenv('BOT_NAME', 'DefaultBot')+'.exe')
		print(self.EjecutablePrograma)
		print(RutaEjecutablePrograma)
		'''self.ruta_archivo = "{}\\{}".format(self.ruta_escritorio,f"RegActividad_{self.EjecutablePrograma}.csv")
								if os.path.isfile(self.ruta_archivo)==False:
									f=open(self.ruta_archivo,"a")
									f.close()'''

		# 3450
		# self.EjecutablePrograma="Bot_GestorBuc1.exe"  # esto para tocaro ver desde codigo un bot de produccion, se pone el nombre completo
		# self.EjecutablePrograma="Bot_MarcadorCali5.exe"  # esto para tocaro ver desde codigo un bot de produccion, se pone el nombre completo
		self.EjecutablePrograma=os.getenv('BOT_NAME', 'DefaultBot')+'.exe'  # esto para tocaro ver desde codigo un bot de produccion, se pone el nombre completo
		
		print(self.EjecutablePrograma, "<>", RutaEjecutablePrograma)
		nombre_equipo = socket.gethostname()
		direccion_equipo = socket.gethostbyname(nombre_equipo)
		usuario_pc = getuser()
		print(nombre_equipo, "direccion ip: ", direccion_equipo, "sección usuario: ", usuario_pc)


		#---------------------Hilo para verificar actualizaciones----------------
		#threading.Thread(target=self.VerificadorAct, daemon=True).start()

		# self.EjecutablePrograma+="x"  # se descomenta para desarrollo ya que se agrega una "x" al final de nombre del bot

		print("bot en labor ",self.EjecutablePrograma)
		print("Version: ",__version__)
		
		sql=("SPR_GET_INFOBOT",[self.EjecutablePrograma])
		IdBot =ConectorDbMysql().GetQueryPars(sql)[0]		
		#IsAlive = NotificaActividad(self.EjecutablePrograma)
		#IsAlive.Savedata()
		print(IdBot)
		if IdBot is None:			
			# se crea el mismo en la base de datos
			sql=("SPR_INS_NEWBOT",[self.EjecutablePrograma,direccion_equipo,usuario_pc,nombre_equipo])					
			ConectorDbMysql().GetQueryPars(sql)
			time.sleep(3)
			sql=("SPR_GET_INFOBOT",[self.EjecutablePrograma])
			IdBot=ConectorDbMysql().GetQueryPars(sql)[0]
		else:
			print(IdBot)

		IdAct = None
		while 1:
			try:
				IdAct=ConectorDbMysql().FuncGetUpdSpr(1,"SPR_GET_ACTBOT",[IdBot,self.EjecutablePrograma])									
				if IdAct[0] is not None:
					GestorLabor().LauncherBots(IdBot,IdAct[0],self.EjecutablePrograma)						
				else:					
					time.sleep(random.randint(5, 55))

				#ConectorDbMysql().RepActividad(IdBot)					
			except Exception as e:
				Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
				print(Nomb_error)
					
			


	#def VerificadorAct(self):		
		#print("Verificador actualizaciones iniciado!")
		'''schedule.every(300).seconds.do(self.GetActualizacion)	
								while 1:
									try:			
										schedule.run_pending()
										time.sleep(1)			
									except Exception as e:
										print(e)'''
						
	def GetActualizacion(self):		
		nombre_bot='bot_server'
		VersionDb=ComprobarVersion(self,'bot_server')		
		if float(__version__)<float(VersionDb):
			download_actualizacion(self, nombre_bot, VersionDb)
			sys.exit()
		else:
			pass
			
if __name__ == '__main__':
	time.sleep(10)
	aplication = Bot_server()
