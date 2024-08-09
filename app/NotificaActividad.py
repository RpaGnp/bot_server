import sqlite3
from sqlite3 import Error
from sqlite3 import connect
import time
from datetime import datetime
from datetime import date
import time
import os
from platform import platform


class GestorSqlite:
    def __init__(self):
        FechaHora = datetime.now()
        self.Fecha = FechaHora.strftime('%d/%m/%Y')
        self.Hora = FechaHora.strftime('%H:%M:%S')
        self.ruta_escritorio = f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}"
        """ create a database connection to a SQLite database """
        if 'Windows' in platform():
            base_dir = "C://DBGestionBot"
            db_file = r"C:\\DBGestionBot\\DbActividadesBots.db"
        else:
            base_dir = "/app/DBGestionBot"
            db_file = "/app/DBGestionBot/DbActividadesBots.db"

        # Crear el directorio si no existe
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)

        # Asignar la ruta de la base de datos
        self.db_file = db_file

    def CreateConn(self):
        return self.Fecha, self.Hora

    def Creador_Db(self):
        conn = sqlite3.connect(self.db_file)
        # print(sqlite3.version)
        cursor = conn.cursor()
        # ==========================CREAR LA TABLA DE CARGA DATOS====================================
        sql = '''
		CREATE TABLE IF NOT EXISTS TBL_CONTROL_BOT(		
        NOMBOT VARCHAR(250),					
		FECHAINICIO VARCHAR(250),
		HORAINICIO VARCHAR(250),
		ESTADOGESTIONBOT VARCHAR(250),
		FECHACTBOT VARCHAR(50),
		HORACTBOT VARCHAR(50),				
		DETALLE0 NVARCHAR(500),
		DETALLE1 NVARCHAR(500),
		DETALLE2 NVARCHAR(500),
		DETALLE3 NVARCHAR(500)
		)
		'''
        cursor.execute(sql)
        cursor.close()
        conn.close()

   

    def UpdInsBot(self,consulta):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(consulta)
        conn.commit()
        cur.close()
        conn.close()


    def GetGestionOne(self, query):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(query)
        DATA = cur.fetchone()
        cur.close()
        conn.close()

        return DATA

    

    def RegBot(self,NombreBot):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(f"INSERT INTO TBL_CONTROL_BOT(NOMBOT,FECHAINICIO,HORAINICIO,ESTADOGESTIONBOT) values ('{NombreBot}','{self.Fecha}','{self.Hora}','Registrado OK')")
        conn.commit()
        cur.close()
        conn.close()


    def UpdActividad(self,NombreBot):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(f"UPDATE TBL_CONTROL_BOT SET FECHACTBOT=date('now'), HORACTBOT=strftime('%H:%M:%S', 'now', 'localtime') WHERE NOMBOT='{NombreBot}'")
        conn.commit()
        cur.close()
        conn.close()


import redis


class NotificaActividad:
    def __init__(self,nombreBot):
        self.nombreBot =nombreBot
        self.dbr = redis.StrictRedis(host='localhost', port=6379, db=0)

    def _timmer(self):
        FechaHora = datetime.now()
        self.Fecha = FechaHora.strftime('%d/%m/%Y')
        self.Hora = FechaHora.strftime('%H:%M:%S')

        return self.Fecha,self.Hora

    def Savedata(self):
        Arrayahora=self._timmer()
        if not self.dbr.exists(self.nombreBot):
            dicingreso={
                "FechaInicio":Arrayahora[0],
                "HoraInicio":Arrayahora[1],
                "EstadoInicio":1,
                "fechaActualizacion":Arrayahora[0],
                "HoraActualizacion":Arrayahora[1],
                "EstadoAct":1
            }
            self.dbr.hmset(self.nombreBot, dicingreso)
        else:
            self.upddata()

    def upddata(self):
        Arrayahora=self._timmer()
        self.dbr.hset(self.nombreBot, "FechaActualizacion", Arrayahora[0])
        self.dbr.hset(self.nombreBot, "HoraActualizacion", Arrayahora[1])

    def GetData(self):
        # Recuperar datos
        diccionario_bot = self.dbr.hgetall(self.nombreBot)
        # Convertir los valores de bytes a cadenas (en Python 3)
        diccionario_bot = {campo.decode('utf-8'): valor.decode('utf-8') for campo, valor in diccionario_bot.items()}
        print(diccionario_bot)

#NotificaActividad("Botserver.exe").GetData()





