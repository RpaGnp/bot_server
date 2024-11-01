#from ..ModuloCipher.ModuloAes import *.

'''import importlib.util

spec = importlib.util.spec_from_file_location("ModuloAes", "../ModuloCipher/ModuloAes.py")
Encriptador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Encriptador)
# Para invocar la rutina anteponemos el nombre del módulo
GestorEcrAes=Encriptador.chipherAes()# instancia la clase que esta en otra carpeta

'''
#from .ModuloAes import chipherAes
import pymysql
import mariadb
import datetime
from getpass import getuser
from datetime import date
from datetime import datetime
import platform
import os
from dotenv import load_dotenv
import sys
from validar_bot import nombre_bot

# Cargar las variables de entorno del archivo .env
load_dotenv()


# __NAMEPC__='SERVER-1678' # nombre pc cali 
# __NAMEPC__='DESKTOP-N2BMB8J' # nombre pc Bucaramanga 
# __NAMEPC__='100-DES1391R' # nombre pc Bogota 


class ConectorDbMysql(object):
	"""clase que maneja las tansacciones a mysql"""
	def __init__(self):
		self.conn = False		
		# print('inicio base de datos')
		EjecutablePrograma, RutaEjecutablePrograma  = nombre_bot()
		# EjecutablePrograma=os.getenv('BOT_NAME', 'DefaultBot')+'.exe'
		cal_db = ["Bot_GestorCali1.exe", "Bot_GestorCali2.exe", "Bot_GestorCali3.exe", "Bot_GestorCali4.exe", "Bot_GestorCali5.exe", "Bot_MarcadorCali.exe", "Bot_MarcadorCali1.exe", "Bot_MarcadorCali2.exe", "Bot_MarcadorCali3.exe", "Bot_MarcadorCali4.exe", "Bot_MarcadorCali5.exe", "DefaultBot.exe"]
		bog_db = ["Bot_Gestor1.exe", "Bot_Gestor2.exe", "Bot_Gestor3.exe", "Bot_Gestor4.exe", "Bot_Gestor5.exe", "Bot_GestorBuc1.exe", "Bot_GestorBuc2.exe", "Bot_GestorBuc3.exe", "Bot_GestorBuc4.exe", "Bot_GestorBuc5.exe", "Bot_GestorBuc6.exe", "Bot_Marcador1.exe", "Bot_Marcador2.exe", "Bot_Marcador3.exe", "Bot_Marcador4.exe", "DefaultBot.exe"]

		__Cali_DB__= False
		if EjecutablePrograma in cal_db:
			__Cali_DB__= True

		# Configurar la base de datos basada en el nombre del PC
		if __Cali_DB__:
		# Base de datos cali 
			# print('Base de datos cali') 
			db_config = {
				'host': os.getenv('DB_HOST_SERVER'),
				'user': os.getenv('DB_USER_SERVER'),
				'password': os.getenv('DB_PASSWORD_SERVER'),
				'db': os.getenv('DB_NAME_SERVER'),
				'port': int(os.getenv('DB_PORT_SERVER'))
			}
		else:
		# Base de datos Bogota
			# print('Base de datos Bogota')
			db_config = {
				'host': os.getenv('DB_HOST_LOCAL'),
				'user': os.getenv('DB_USER_LOCAL'),
				'password': os.getenv('DB_PASSWORD_LOCAL'),
				'db': os.getenv('DB_NAME_LOCAL'),
				'port': int(os.getenv('DB_PORT_LOCAL'))
			}
		x=0
		while x<5:
			try:
				# Imprimir las variables
				# print("Host:", db_config['host'])
				# print("User:", db_config['user'])
				# print("Password:", db_config['password'])  # Asegúrate de que sea seguro imprimir la contraseña
				# print("Database:", db_config['db'])
				# print("Port:", db_config['port'])
				self.conn = pymysql.connect(
							host=db_config['host'],
							user=db_config['user'],
							password=db_config['password'],
							db=db_config['db'], 
							port=db_config['port'],
							connect_timeout=60
						)
				break
			except Exception as e:
				print("error conexion ",e)
				x+=1

	'''def get_connection(self):		
		return self.db_pool.get_connection()'''

	def GetConn(self):
		return self.conn	

	def timer(self):
		FechaHora = datetime.now()	
		date_actual=FechaHora.strftime('%d/%m/%Y %H:%M:%S')
		Fecha = FechaHora.strftime('%d/%m/%Y')
		Hora = FechaHora.strftime('%H:%M:%S')
		fecha = str(Fecha)
		hora = str(Hora)
		return fecha, hora, date_actual,Fecha,Hora
	
	def GetQueryPars(self,sql):		
		cursor=self.conn.cursor()
		cursor.callproc(sql[0],args=(sql[1]))
		self.conn.commit()
		Consulta=cursor.fetchone()
		print(Consulta)
		cursor.close()
		self.conn.close()
		return Consulta

	def FuncGetInfoOne(self,TipoData,Consulta,Parametros):
		"""tipo data: 1 fechone, 0 fechall"""
		if Parametros==None:
			pass
		with self.conn.cursor() as cursor:
			cursor.callproc(Consulta,args=(Parametros))
			if TipoData==1:
				data=cursor.fetchone()
			else:
				data=cursor.fetchall()
		cursor.close()
		self.conn.close()
		return data

	def FuncGetInfo(self,TipoData,sql):		
		with self.conn.cursor() as cursor:					
			cursor.execute(sql)
			if TipoData==1:
				data=cursor.fetchone()
			else:
				data=cursor.fetchall()
		cursor.close()
		self.conn.close()
		return data

	def FuncInsInfoOne(self,Consulta):				
		try:		
			with self.conn.cursor() as cursor:
				cursor.callproc(Consulta[0],args=(Consulta[1]))
				self.conn.commit()
			cursor.close()
			self.conn.close()
		except Exception as e:
			print(e)

	def FunGetProcedure(self,sql):
		with self.conn.cursor() as cursor:
			cursor.callproc(sql[0],args=(sql[1]))
			data=cursor.fetchone()
		cursor.close()
		self.conn.close()
		return data

	def RepActividad(self,Idbot):
		try:
			with self.conn.cursor() as cursor:
				cursor.callproc("SPR_UPD_TIMBOT",args=([Idbot]))
				self.conn.commit()
			cursor.close()
			self.conn.close()
		except Exception as e:
			print(e)


	def FuncGetSpr(self,tipo,procedimiento,Arraydatos=[]):
		data=[]
		with self.conn.cursor() as cursor:
			if len(Arraydatos)!=0:
				cursor.callproc(procedimiento,args=(Arraydatos))
			else:
				cursor.callproc(procedimiento)
			if tipo==1:
				data=cursor.fetchone()
			else:
				data=cursor.fetchall()
		self.conn.close()
		return data

	def FuncGetUpdSpr(self,tipo,procedimiento,Arraydatos=[]):
		data=[]
		with self.conn.cursor() as cursor:
			if len(Arraydatos)!=0:
				cursor.callproc(procedimiento,args=(Arraydatos))
			else:
				cursor.callproc(procedimiento)
				
			self.conn.commit()
			
			if tipo==1:
				data=cursor.fetchone()
			else:
				data=cursor.fetchall()
		self.conn.close()
		return data

	def FuncUpdSpr(self,procedimiento,Arraydatos=[]):
		data=[]
		with self.conn.cursor() as cursor:
			if len(Arraydatos)!=0:
				cursor.callproc(procedimiento,args=(Arraydatos))
			else:
				cursor.callproc(procedimiento)
		self.conn.commit()
		
		return True


