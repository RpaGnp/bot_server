from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64



clave = b'Rp4Gnp2023*+CNDSeguridad'

class Encriptador:
	@classmethod
	def EncriptData(self,dato):
		mensaje = dato.encode('utf-8')

		cipher = Cipher(algorithms.AES(clave), modes.CBC(b'0123456789ABCDEF'), backend=default_backend())
		encryptor = cipher.encryptor()
		mensaje_encriptado = encryptor.update(mensaje) + encryptor.finalize()

		return mensaje_encriptado

	@classmethod
	def DecriptData(self):
		mensaje_encriptado = base64.b64decode(mensaje_encriptado_base64)
		cipher = Cipher(algorithms.AES(clave), modes.CBC(b'0123456789ABCDEF'), backend=default_backend())
		decryptor = cipher.decryptor()
		mensaje_desencriptado = decryptor.update(mensaje_encriptado) + decryptor.finalize()
		
		return mensaje_desencriptado.decode()



import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

# Función para generar una clave derivada de una contraseña utilizando PBKDF2
def generar_clave_derivada(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

# Función para encriptar datos utilizando AES-GCM
def encriptar_datos(datos, clave):
    nonce = os.urandom(12)  # Generar un nonce único
    cipher = Cipher(algorithms.AES(clave), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    datos_encriptados = encryptor.update(datos) + encryptor.finalize()
    tag = encryptor.tag  # Obtener el tag de autenticación

    # Codificar los datos encriptados y el tag como base64
    datos_encriptados_base64 = base64.b64encode(datos_encriptados).decode('utf-8')
    tag_base64 = base64.b64encode(tag).decode('utf-8')

    # Concatenar el nonce, los datos encriptados y el tag codificados como base64
    datos_encriptados_varchar = nonce + datos_encriptados_base64 + tag_base64

    return datos_encriptados_varchar

# Función para desencriptar datos utilizando AES-GCM
def desencriptar_datos(datos_encriptados_varchar, clave):
    # Separar el nonce, los datos encriptados y el tag codificados como base64
    nonce = datos_encriptados_varchar[:12]
    datos_encriptados_base64 = datos_encriptados_varchar[12:-24]
    tag_base64 = datos_encriptados_varchar[-24:]

    # Decodificar los datos encriptados y el tag desde base64
    datos_encriptados = base64.b64decode(datos_encriptados_base64)
    tag = base64.b64decode(tag_base64)

    cipher = Cipher(algorithms.AES(clave), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    datos_desencriptados = decryptor.update(datos_encriptados) + decryptor.finalize()

    return datos_desencriptados

# Datos a encriptar
datos = b"Hola, este es un mensaje secreto"

# Contraseña para derivar la clave de encriptación
password = b"contrasena_segura"

# Generar una clave derivada de la contraseña
salt = os.urandom(16)  # Generar una sal aleatoria
clave = generar_clave_derivada(password, salt)

# Encriptar los datos
datos_encriptados_varchar = encriptar_datos(datos, clave)

# Desencriptar los datos
datos_desencriptados = desencriptar_datos(datos_encriptados_varchar, clave)

# Imprimir los resultados
print("Datos originales:", datos)
print("Datos encriptados (VARCHAR):", datos_encriptados_varchar)
print("Datos desencriptados:", datos_desencriptados)
