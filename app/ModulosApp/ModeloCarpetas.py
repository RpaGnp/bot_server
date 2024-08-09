import os
from datetime import datetime

def CreadorCarpetas(carpetasegura):
    if not os.path.exists(carpetasegura):
        os.mkdir(carpetasegura)

    # Crear ruta para el año
    Pathyear = os.path.join(carpetasegura, datetime.now().strftime("%Y"))
    if not os.path.exists(Pathyear):
        os.mkdir(Pathyear)

    # Crear ruta para el mes
    PathMes = os.path.join(Pathyear, datetime.now().strftime("%m"))
    if not os.path.exists(PathMes):
        os.mkdir(PathMes)

    # Crear ruta para el día
    pathDia = os.path.join(PathMes, datetime.now().strftime("%d"))
    if not os.path.exists(pathDia):
        os.mkdir(pathDia)

    return pathDia