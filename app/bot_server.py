__version__=3.41
######
import sys
import os
import time
import random
import socket
from getpass import getuser
from ModulosApp.ModelDataBase import ConectorDbMysql
from ModulosApp.ModeloLauncher import GestorLabor
from Actualizador_programa import *
from validar_bot import nombre_bot
import os

# Ruta absoluta al archivo .env (ajusta según tu sistema)
env_path = os.path.join(os.path.dirname(__file__), '.env')

try:
    if not os.path.exists(env_path):
        print(f"El archivo {env_path} no existe. No se puede iniciar el código.")
        sys.exit(1)
except FileNotFoundError as e:
    print(f"Error al verificar el archivo .env: {e}")


'''from Notificar import notificar_actividad
#from encriptar_256 import Credenciales_Conexion
from manejador_errores import manejador_errores
from reloj_casio import timer
#=================actualizador automatico==========================
from Actualizador_programa import download_actualizacion
'''


class Bot_server:
	def __init__(self):
		self.EjecutablePrograma, RutaEjecutablePrograma  = nombre_bot()

		print('este es el bot: ', os.getenv('BOT_NAME', 'DefaultBot')+'.exe')
		print(RutaEjecutablePrograma)
		print(self.EjecutablePrograma, "<>", RutaEjecutablePrograma)
		nombre_equipo = socket.gethostname()
		direccion_equipo = socket.gethostbyname(nombre_equipo)
		usuario_pc = getuser()
		print(nombre_equipo, "direccion ip: ", direccion_equipo, "sección usuario: ", usuario_pc)

		print("bot en labor ",self.EjecutablePrograma)
		print("Version: ",__version__)
		
		sql=("SPR_GET_INFOBOT",[self.EjecutablePrograma])
		IdBot =ConectorDbMysql().GetQueryPars(sql)[0]		

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
					
			
	def GetActualizacion(self):		
		nombre_bot='bot_server'
		VersionDb=ComprobarVersion(self,'bot_server')		
		if float(__version__)<float(VersionDb):
			download_actualizacion(self, nombre_bot, VersionDb)
			sys.exit()
		else:
			pass
			
if __name__ == '__main__':
	# time.sleep(10)
	aplication = Bot_server()
