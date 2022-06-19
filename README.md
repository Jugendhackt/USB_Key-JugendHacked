# CryptoUSB

The programm is written to en/decrypt files in a safer way than usual.
Because of the two factor authentication, that is achieved by using a combination of a USB-Flashdrive and a password,
Crypto USB is much safer than other encryption software.

## How to install CryptoUSB

- Download the run.exe from https://github.com/Jugendhackt/USB_Key-JugendHacked/releases/download/v1.2.0/run.exe onto a flashrive
- The flashdrive is now the key to your data

## How to use CryptoUSB

How to encrypt:
- Plug the flashdrive in
- Chose a password and the file that is to be encrypted
- After your file is encrypted pull the flashdrive out and put it in a safe place

How to decrypt:
- plug in the flashdrive
- run 'run.exe' and enter your password
- press decrypt and choose your file



## Compile
```cmd
git clone https://github.com/EdisonLamp/USB_Schluessel.git
cd USB_Schluessel
pip install pyinstaller
pyinstaller -F -w .\Frontend\run.py
```
