from pymongo import MongoClient
from datetime import datetime




class Handledbmongo:
	def __init__(self,host='172.20.100.51', port=27017, username=None, password=None):		

		self.nombreDb = 'BotCND'
		self.client = MongoClient(host,port)

	def Conn(self):
		return self.client[self.nombreDb]

	def DxConn(self):
		self.client.close()

	def UpdDataOne(self, coll, JsonBusq, jsonDatos):
		db = self.Conn()
		collection = db[coll]
		collection.update_one(JsonBusq,{"$set":jsonDatos},upsert=True)
		self.DxConn()
	        # Hacer operaciones de actualización aquí

	def GetDataRazon(self, coll,Ciudad,DicKeys={}):				
		db = self.Conn()
		collection = db[coll]		
		cursor = collection.find(JsonBusq,DicKeys,sort=[('Fecha', -1),('Hora', -1)])					
		documentos = list(cursor)		
		self.DxConn()		
		return documentos

	def GetData(self, coll,Ciudad,DicKeys={}):
		criterio_busqueda = {}		
		if Ciudad:
			criterio_busqueda[Ciudad] = {"$exists": True}	
		
		db = self.Conn()
		collection = db[coll]								
		cursor = collection.find(criterio_busqueda,DicKeys)	
		documentos = list(cursor)		
		self.DxConn()		
		return documentos	
		

	def InsertDataOne(self, coll, documento):
		db = self.Conn()
		collection = db[coll]
		resultado = collection.insert_one(documento)	    
		self.DxConn()
		return resultado.inserted_id
        
	def RemoveData(self,coll,tipo=0,JsonBusq=None):
		db = self.Conn()
		collection = db[coll]
		if tipo == 0:
			collection.delete_one(JsonBusq)
		else:
			collection.delete_many({})
		self.DxConn()

	def GetTrabajosRazon(self,Ciudad,Carpeta,subtipo):				
		x=self.GetData("RazonesCancelar2",Ciudad,{"_id":0})		
		if len(x):		
			for dic in x:									
				for razones in dic.values():					
					ArrayRazones = razones.keys()
					if Carpeta in ArrayRazones:
						return razones[Carpeta][subtipo]
					else:
						return []	
					
				#print(dic[Ciudad][Carpeta])
				
		else:
			return []
			#return dic[Ciudad][Carpeta]

'''x = Handledbmongo().GetDataRazon("DicRazones",{},{"_id":0})
print(x[0])
'''
'''import json

ArrayRazonesCancelables= Handledbmongo().GetTrabajosRazon("Bucaramanga","Instalaciones","Instalacion Empaquetada Bi")
print(ArrayRazonesCancelables)
'''




'''{"Blindaje.":["M","E","V"]},
{"Instalaciones":["B","E","V","Z","M"]},
{"INSTALACIONES FTTH":["M","B","E","V","Z"]},
{"Post Venta":["M","E","4"]},
{"POSTVENTA  FTTH":["M","E","V","4"]},
{"Traslados Pymes":["E","B"]},
{"INSTALACIONES DTH":["/"]},			
{"Arreglos":["S"]},
{"MANTENIMIENTO FTTH":["S"]}


'''

#ArrayDataOt={"Razon":"EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES","OtLls":"396983466_O_CO_26","Id Usuario Cnd":"1001117754","Asesor Cnd":"MANUEL FELIPE MESA DANIELDS","OBSERVACIONES":"Casa de dos pisos, Fachada color café , Puerta blancan254466879915 este es el que tiene físico y este es el que le hace falta 254471120105","null":""}

# ArrayRazonesCancelables = Handledbmongo().GetTrabajosRazon("Bogota",'Blindaje')												
# print(ArrayRazonesCancelables)