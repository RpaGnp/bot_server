from datetime import date
from datetime import datetime

def timer():
	FechaHora = datetime.now()	
	date_actual=FechaHora.strftime('%d/%m/%Y %H:%M:%S')
	Fecha = FechaHora.strftime('%d/%m/%Y')
	Hora = FechaHora.strftime('%H:%M:%S')

	fecha = str(Fecha)
	hora = str(Hora)
	return fecha, hora, date_actual,Fecha,Hora

