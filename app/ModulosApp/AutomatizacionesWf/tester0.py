
import datetime
x=((2, datetime.date(2022, 9, 23), 'SANDRA PATRICIA ACERO PULIDO', 'TORRE HFC', 'WESLEY CHAPARRO SANABRIA', 100, 'Abierto'), (3, datetime.date(2022, 9, 23), 'SANDRA PATRICIA ACERO PULIDO', 'TORRE HFC', 'WESLEY CHAPARRO SANABRIA', 0, 'Abierto'))
print(len(x))
dic={}
for i in range(len(x)):
	dic.update({str(i):x[i]})	

print(dic)