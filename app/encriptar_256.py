# AES 256 encryption/decryption using pycryptodome library
from Cryptodome.Random import get_random_bytes
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
import ctypes.wintypes
from os import getcwd
from os import remove
from os import path
import hashlib
import pyodbc
import shutil
import socket
import time
import os
import sys

def Crear_Dll():
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.Shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    Mis_documentos=buf.value

    if getattr(sys, 'frozen', False):        
        dll_path = os.path.join(sys._MEIPASS, "./dll_bot/Runtime.dll")
        ruta_dll=f"{Mis_documentos}\\dll_bots"
        
        if not os.path.isdir(ruta_dll):
            os.mkdir(ruta_dll)
        else:
            print("carpeta de dll existe!")
        
        if path.exists(ruta_dll):
            try:
                remove(ruta_dll)
            except:
                pass
        else:
            pass
       
        shutil.copyfile(dll_path,ruta_dll)

        RutaBaseRuntime=f"{ruta_dll}//{Runtime.dll}"
    
    else:
        RutaBaseRuntime = getcwd() + "\\Runtime.dll"

    return RutaBaseRuntime

def ConexionRuntime():
    # debemos crear la runtime en mis documentos para acceder a ella en al conexion

    #Funcion para Activar la conexion Runtime.dll
    DRIVER_NAME = "Microsoft Access Driver (*.mdb, *.accdb)"
    #Crear_Dll
    RutaBaseRuntime = Crear_Dll()
    #RutaBaseRuntime = getcwd() + "\\Runtime.dll"
    if os.path.isfile(RutaBaseRuntime):
        pass
    else:
        return "NoExiste"    
    conn = pyodbc.connect("Driver=Microsoft Access Driver (*.mdb, *.accdb);DBQ="+RutaBaseRuntime+";PWD=RUNTIMEORQUESTADOR")
    
    return conn 

def encrypt(plain_text, password):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted

def Credenciales_Conexion():
    #Pre Pro Desarrollo
    #Ambiente="Pre"
    #Ambiente = "Pro"
    Ambiente = "Desarrollo"
    nombre_equipo = socket.gethostname()
    if nombre_equipo!="toshiba":
        password = "Eficiencia_Operativa_2021_01_rpa"
        if Ambiente=="Pre":
            Data = [{'cipher_text': 'zNCYZQ5xel+VX+jj', 'salt': 'X46a43DKPcBoxy1EILjfYg==', 'nonce': 'A0Ut0O8gQ7SFFCDhAxtmVA==',
                 'tag': 'Vi4trp67QdANh0io1dxc3A=='},
                {'cipher_text': 'KA99suZorg==', 'salt': 'fZsge3mJYXCudPQ1B5HDMg==', 'nonce': 'aMNo8EoxTY9VrCJq3d8FdQ==',
                 'tag': 'RODHJ7XvXLCeuMyqHQvZaA=='},
                {'cipher_text': 'KA99suZorg==', 'salt': 'fZsge3mJYXCudPQ1B5HDMg==', 'nonce': 'aMNo8EoxTY9VrCJq3d8FdQ==',
                 'tag': 'RODHJ7XvXLCeuMyqHQvZaA=='},
                {'cipher_text': '8yDhh0BkaDf5Czk6zG4oxlirfCyLOPLZeOI=', 'salt': 'l/ke9lhHeVRcAVZ/AZlUoQ==',
                 'nonce': 'KNiU9Qx4ulRnzjuLtjT3Pg==', 'tag': 'Orm82fMX7lAS3OeEsrYoAA=='}
                ]
        elif Ambiente=="Pro":
            Data = [{'cipher_text': 'zNCYZQ5xel+VX+jj', 'salt': 'X46a43DKPcBoxy1EILjfYg==',
                     'nonce': 'A0Ut0O8gQ7SFFCDhAxtmVA==',
                     'tag': 'Vi4trp67QdANh0io1dxc3A=='},
                    {'cipher_text': 'KA99suZorg==', 'salt': 'fZsge3mJYXCudPQ1B5HDMg==',
                     'nonce': 'aMNo8EoxTY9VrCJq3d8FdQ==',
                     'tag': 'RODHJ7XvXLCeuMyqHQvZaA=='},
                    {'cipher_text': 'KA99suZorg==', 'salt': 'fZsge3mJYXCudPQ1B5HDMg==',
                     'nonce': 'aMNo8EoxTY9VrCJq3d8FdQ==',
                     'tag': 'RODHJ7XvXLCeuMyqHQvZaA=='},
                    {'cipher_text': '8yDhh0BkaDf5Czk6zG4oxlirfCyLOPLZeOI=', 'salt': 'l/ke9lhHeVRcAVZ/AZlUoQ==',
                     'nonce': 'KNiU9Qx4ulRnzjuLtjT3Pg==', 'tag': 'Orm82fMX7lAS3OeEsrYoAA=='}
                    ]
        elif Ambiente=="Desarrollo":
            Data = [{'cipher_text': 'NtG3zoDUbfKJdvVpXdLCpKU4lDjH', 'salt': 'pLaOvOyoe0SuJpZQECJ+/g==',
                     'nonce': 'At6IVrGMub8obHT4RlEVfg==',
                     'tag': 'iisDpW+PIjjIIGLx5mDf+Q=='},
                    {'cipher_text': 'SJAkknRPwA==', 'salt': 'Nve5xHWimD38lXomE5j4rw==',
                     'nonce': 'Lyzmlj2pf9+e6Iwo7OuRtg==',
                     'tag': 'MC2N14Dz7PfmP+KgIyl+lw=='},
                    {'cipher_text': 'SJAkknRPwA==', 'salt': 'Nve5xHWimD38lXomE5j4rw==',
                     'nonce': 'Lyzmlj2pf9+e6Iwo7OuRtg==',
                     'tag': 'MC2N14Dz7PfmP+KgIyl+lw=='},
                    {'cipher_text': 'DtSeAmoG6BgcmiOUlDob6JT742LniB6b5TLfAvUpx65YyPBxlJU=',
                     'salt': '+tebQuEv45+cYz9Z+hUObw==',
                     'nonce': 'q/yoYgf+NqyzZkqjc7kuDQ==', 'tag': 'PQ2xFUNpeMNSqE+SzimDTA=='}
                    ]

        Credenciales=[]
        for dic in Data:
            decrypted = decrypt(dic, password)
            Credenciales.append(bytes.decode(decrypted))    
        return Credenciales
    else:
        password = "Eficiencia_Operativa_2021_01_rpa"
        Data=[{'cipher_text':'gwzQGomSho7LDEtX2dUoyqSP','salt':'VGX4ydwu++8ClYDxIlVbKg==','nonce':'G3Jjkec3aqp+CTdJLtL/lw==','tag':'Iuc7ewMQOWpGC/2y/X+v2w=='},
        {'cipher_text':'qzg=','salt':'ulsYbK43/DoV0AyyY6vFSg==','nonce':'GzbY8UWBQnQS7qJw+7iFhg==','tag':'N82EmNtXuTWHRM3SARAoSQ=='},
        {'cipher_text':'TNsflg==','salt':'u9mrlH2kgQ9gKkaUZqsg0Q==','nonce':'r+LaBXQGt0SYkeUitoiVaQ==','tag':'aQysZ7l0ks0ml1hQYkIQgA=='},
        {'cipher_text':'eLVcfQnxbYgovvYbYZnxOYY+9weMFQ==','salt':'JRUI5O5SG2b7HPmhhu4oyQ==','nonce':'k5Id+5HwFY3Aj43fAUz3xQ==','tag':'rKtViPiCT3vZcbX0JHltlw=='}
        ]
        Credenciales=[]
        for dic in Data:
            decrypted = decrypt(dic, password)
            Credenciales.append(bytes.decode(decrypted))    
        return Credenciales

def main():
    password = "Eficiencia_Operativa_2021_01_rpa"

    # First let us encrypt secret message
    encrypted = encrypt("ATENTO_ACTIVIDADES_CGO", password)
    print(encrypted)

    # Let us decrypt using our original password
    decrypted = decrypt(encrypted, password)
    print(bytes.decode(decrypted))

#main()
#print(Credenciales_Conexion())