import requests
import json


class ConsultorApi:
    def __init__(self):        
        self.server="http://172.20.100.51:8000"
        #self.server="http://10.206.169.233:5699"     
        #self.server="http://apicndnal/"
        self.ApiGet = f'{self.server}/api/v.1/ApiCnd/GetData'
        self.ApiUpd = f'{self.server}/api/v.1/ApiCnd/UpdData'
        self.ApiUpdGet = f'{self.server}/api/v.1/ApiCnd/UpdGetData'


    def callGet(self,dicdatos):             
        response = requests.post(self.ApiGet, json=dicdatos)                        
        data = json.loads(response.text)                         
        return data['Datos']

    def callUpd(self, dicdatos):        
        response = requests.post(self.ApiUpd, json=dicdatos)
        print(response)
        data = json.loads(response.text)
        

    def FuncUpdGetSpr(self, dicdatos):
        response = requests.post(self.ApiUpdGet, json=dicdatos)
        data = json.loads(response.text)
        return data['Datos']

#ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': 1, 'tipo': 1, 'procedimiento': 'SPR_INS_ESTBOT', 'arraydatos': [3491, 'En labor']})
#arraypermiso=ConsultorApi().callGet({'servicio': 'Koala', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_get_horlogAse","arraydatos":[1070968663]})
#print(arraypermiso)