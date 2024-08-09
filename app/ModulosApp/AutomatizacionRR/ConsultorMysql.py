import pymysql
import platform


class ConectorDbMysql:
	"""docstring for ConectorDbMysql"""
	def __init__(self):		
		self.conn = None
		self.__NAMEPC__=platform.node()

	def CreateConn(self):		
		try:
			if self.__NAMEPC__== "SERVER-1678":				
				self.conn = pymysql.connect(host='SERVER-1678', user='root', password='AdmCndCal2023*', db='dbcrmgnp',connect_timeout=60)
			else:
				self.conn = pymysql.connect(host='190.60.100.100', user='BotCND', password='1234', db='dbcrmgnp')
		
		except Exception as e:
			print(e)
		return self.conn


	def GetData(self,tipo,procedimiento,arraydatos=[]):
		with self.CreateConn().cursor() as cursor:			
			if len(arraydatos)==0:
				cursor.callproc(procedimiento)
			else:
				cursor.callproc(procedimiento,args=(arraydatos))
			
			data = cursor.fetchone() if tipo ==0 else cursor.fetchall()
		return data

	def UpData(self,procedimiento,arraydatos=[]):
		conn = self.CreateConn()
		with conn.cursor() as cursor:			
			if len(arraydatos)==0:
				cursor.callproc(procedimiento)
			else:
				cursor.callproc(procedimiento,args=(arraydatos))
			conn.commit()
		conn.close()
			

#print(ConectorDbMysql().GetData(0,"spr_get_razxcan",["Bogota"]))