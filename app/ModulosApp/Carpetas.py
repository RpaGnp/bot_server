import os
from datetime import datetime


def CreadorCarpetas(carpetasegura):
    if os.path.exists(carpetasegura)==False:
       os.mkdir(carpetasegura)
    #año	
    Pathyear=carpetasegura+"\\"+datetime.now().strftime("%Y")	
    if os.path.exists(Pathyear) ==False:
        os.mkdir(Pathyear)
    #mes
    PathMes=Pathyear+"\\"+datetime.now().strftime("%m")

    os.chdir(Pathyear)
    if os.path.exists(PathMes) ==False:
        os.mkdir(PathMes)
    #dia
    pathDia=PathMes+"\\"+datetime.now().strftime("%d")
    if os.path.exists(pathDia) ==False:
        os.mkdir(pathDia)

    return pathDia


