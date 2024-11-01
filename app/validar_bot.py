import os
import sys
import socket
from getpass import getuser
from platform import platform

def nombre_bot():

    EjecutablePrograma = None
    RutaEjecutablePrograma = None
    
    if 'Windows' in platform():

        comprobar_ruta=str(os.path.dirname(sys.argv[0]))
        if comprobar_ruta.strip()==None:
            EjecutablePrograma=str(os.path.basename(sys.executable))
            RutaEjecutablePrograma=str(os.path.dirname(sys.executable))
        elif comprobar_ruta.strip()=='':
            EjecutablePrograma=str(os.path.basename(sys.executable))
            RutaEjecutablePrograma=str(os.path.dirname(sys.executable))
        else:
            EjecutablePrograma=str(os.path.basename(sys.argv[0]))
            RutaEjecutablePrograma=str(os.path.dirname(sys.argv[0]))

    else:
        try:
            EjecutablePrograma=os.getenv('BOT_NAME', 'DefaultBot')+'.exe'  # se toma la variable de entorno .env o del docker-compose
            RutaEjecutablePrograma = 'Docker' 
        except:
            pass

    # EjecutablePrograma = 'Bot_MarcadorCali5.exe'
    # print('este es el bot: ', EjecutablePrograma)

    return EjecutablePrograma, RutaEjecutablePrograma