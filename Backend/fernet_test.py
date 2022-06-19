from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
msg = b"my deep dark secret"

token = f.encrypt(msg)


print(token)


print(f.decrypt(token))

