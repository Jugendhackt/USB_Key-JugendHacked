import os

from cryptography.fernet import Fernet
import base64
import os
import hashlib

import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto:
    def __init__(self, key=None):
        if not key:
            key = self.key_create()
        self._key = key

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key(self):
        return self._key

    def encrypt(self, data):
        f = Fernet(self._key)
        return f.encrypt(data)

    def decrypt(self, data):
        f = Fernet(self._key)
        return f.decrypt(data)

    def encrypt_file(self, inf, outf=None):
        with open(inf, "rb") as file:
            # read the encrypted data
            data = file.read()
        enc_data = self.encrypt(data)
        if not outf:
            return enc_data
        with open(outf, "wb") as file:
            file.write(enc_data)

    def decrypt_file(self, inf, outf=None):
        with open(inf, "rb") as file:
            # read the encrypted data
            data = file.read()
        dec_data = self.decrypt(data)
        if not outf:
            return dec_data
        with open(outf, "wb") as file:
            file.write(dec_data)


class CryptoUtils:
    def getKeyPath(filename = "") -> str:
        if not filename:
            path = os.getcwd()
        else:
            path = filename
        keyPath = path[:3] + "key.key"
        return str(keyPath)
    
    def key_from_password_and_key_path(password,keyPath) -> Crypto:
        key = open(keyPath, "rb").read()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=key,
            iterations=390000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        c_key = Crypto(key)
        return c_key
    
    def encrypt(password,file_in_name, file_out_name):
        keyPath = CryptoUtils.getKeyPath(file_in_name)
        if not os.path.exists(keyPath):
            key = os.urandom(16)
            with open(keyPath, "wb") as file:
                # read the encrypted data
                file.write(key)

        c_key = CryptoUtils.key_from_password_and_key_path(password,keyPath)
        print(c_key)
        c_key.encrypt_file(str(file_in_name), str(file_out_name)) # overwrite
    
    # return 0, wenn  "Ok"
    # return 1, wenn  "No key found, initialize the drive"
    # return 2, wenn  "Incorrect password!"
    def decrypt(password,file_in_name, file_out_name) -> int:
        keyPath = CryptoUtils.getKeyPath(file_in_name)

        if not os.path.exists(keyPath):
            return 1
            # QMessageBox.about(None, "USBCrypt", "No key found, initialize the drive")
            return

        c_key = CryptoUtils.key_from_password_and_key_path(password,keyPath)

        try:
            rawData = c_key.decrypt_file(str(file_in_name))
            open(str(file_out_name),"wb").write(rawData)
            return 0
        except cryptography.fernet.InvalidToken:
            # print("Error: invalid password")
            # QMessageBox.about(None, "USBCrypt", "Incorrect password!")
            return 2