import base64
import os
import sys

import cryptography.fernet
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import lib

KEYPATH = "/tmp/key.key"
password = str.encode(input("Password: "))
inf = input("Input file: ")

if not os.path.exists(KEYPATH):
    sys.exit(-1)
key = open(KEYPATH, "rb").read()
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=key,
    iterations=390000,
)

key = base64.urlsafe_b64encode(kdf.derive(password))
c_key = lib.Crypto(key)

try:
    print(bytes.decode(c_key.decrypt_file(inf)))
except cryptography.fernet.InvalidToken:
    print("Error: invalid password")