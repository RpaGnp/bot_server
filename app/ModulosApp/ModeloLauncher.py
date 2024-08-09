from .ModelDataBase import ConectorDbMysql
from .automatizacionWFM import GestorWf
#from ModuloAes import chipherAes
import time
import random

from .AutomatizacionesWf.ModuloSeguimiento import *


class GestorLabor:
	def __init__(self):
		pass
	
	def LauncherBots(self,idBot,Idactividad,nombreBot):
		GestorDb=ConectorDbMysql()
		sql=("SPR_GET_DATCTBOT")
		para=(idBot,Idactividad)
		#print(para)
		ArrayCred=GestorDb.FuncGetInfoOne(1,sql,para)
		del sql,para
		print(ArrayCred)
		
		Dato = ConectorDbMysql().FunGetProcedure(("SPR_GET_ESTBOTGES", [idBot]))
		#print(Dato[0])
		if Dato[0] != None:		
			if Dato[0] == "Eliminar":
				ConectorDbMysql().FuncInsInfoOne(("SPR_UPD_LIBBOT", [idBot, Idactividad, 'Detenido por usuario']))				
				return
		else:pass

		try:
			Navegador=GestorWf(idBot,Idactividad,nombreBot,ArrayCred)
			
			if str(ArrayCred[1]) in ['Interapps chat','Crear', "Crear 'No programada'",'Cancelar WFM','Completar',"Completar Backlog","Gestor Notas","Gestor Notas backlog","Marcar Confirmacion","Marcar Demora","Marcacion Multiple","Marcar Seguimiento","Marcacion Soporte","Marcacion TAM"]:
				Navegador.Login("WFM",ArrayCred[4].decode('utf-8'),ArrayCred[5].decode('utf-8'))
			elif str(ArrayCred[1]) in ["Creacion CCOT"]:
				Navegador.Login("GLAPP",ArrayCred[4].decode('utf-8'),ArrayCred[5].decode('utf-8'))
			else:
				Navegador.Login("MODULO",ArrayCred[4].decode('utf-8'),ArrayCred[5].decode('utf-8'))#
				
			#if str(ArrayCred[1]) in ['Completar',"Marcar Confirmacion","Cancelar WFM","Marcar Demora","Marcacion Multiple","Marcar Seguimiento","Marcacion Soporte","Marcacion TAM"]:
			#	Navegador.ConfiBusqueda()			
			time.sleep(1)
			print(ArrayCred[1])
			if str(ArrayCred[1]) in ['Crear',"Crear 'No programada'",'Completar']:
				Navegador.ExpanderCiudad(ArrayCred[2],ArrayCred[3])
			elif str(ArrayCred[1]) in ['Completar Backlog']:
				Navegador.ExpanderCiudadBacklog(ArrayCred[2],ArrayCred[3])
   
			#return
			'''elif str(ArrayCred[1]) in ['Completar']:
				Navegador.ExpanderCiudadComp(ArrayCred[2],ArrayCred[3])'''


			Navegador.LauncherGestion(ArrayCred[2])

			return


		except Exception as e:
			print(e)
			try:
				Navegador.Killit()
			except Exception as e:
				print("*",e)


