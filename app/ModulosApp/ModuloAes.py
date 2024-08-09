from Cryptodome.Cipher import AES

class chipherAes():
    def __init__(self):
        self.Gestor=False

    @classmethod
    def encrypt_Aes(self, key, data):
        cipher = AES.new(key.encode("utf8"), AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode("utf-8"))
        return cipher.nonce + tag + ciphertext
    @classmethod
    def decrypt_AES(self, key, data):
        nonce = data[:AES.block_size]
        tag = data[AES.block_size:AES.block_size * 2]
        ciphertext = data[AES.block_size * 2:]
        cipher = AES.new(key.encode("utf8"), AES.MODE_EAX, nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode("utf8")


'''key="Aut0M4T4CndGnp22"

Codificado=chipherAes.encrypt_Aes(key,"B0tS3rv3rCNDM0N2022*")
print(Codificado)



Decodificado=chipherAes.decrypt_AES(key,Codificado)

print(Decodificado)'''