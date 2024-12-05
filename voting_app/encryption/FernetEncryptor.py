import os
from cryptography.fernet import Fernet

class FernetEncryptor:
    def __init__(self):
        secret_key = os.environ.get("FERNET_KEY")
        
        if not secret_key:
            raise Exception("FERNET_KEY is not exist")
        self.encryptor = Fernet(secret_key)
            
    def encrypt(self, value: bytes|str):
        plain_value = value
        if type(value) == str:
            plain_value = value.encode()
        return self.encryptor.encrypt(plain_value)
    
    def decrypt(self, cipher: bytes|str):
        plain_cipher = cipher
        if type(cipher) == str:
            plain_cipher = cipher.encode()
        return self.encryptor.decrypt(plain_cipher)




        

        
            