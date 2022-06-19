import base64
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import lib

KEYPATH = "/tmp/key.key"
password = str.encode(input("Password: "))
inf = input("Input file: ")
outf = input("Output file: ")

if not os.path.exists(KEYPATH):
    key = os.urandom(16)
    with open(KEYPATH, "wb") as file:
        # read the encrypted data
        file.write(key)

key = open(KEYPATH, "rb").read()
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=key,
    iterations=390000,
)

key = base64.urlsafe_b64encode(kdf.derive(password))
c_key = lib.Crypto(key)

c_key.encrypt_file(inf, outf)