#USB Key

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# enc
import base64
import os
import hashlib
import time

import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import lib

def getKeyPath(filename = ""):
    if not filename:
        path = os.getcwd()
    else:
        path = filename
    keyPath = path[:3] + "key.key"
    return keyPath

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(768, 458)
        MainWindow.setCursor(QCursor(Qt.ArrowCursor))
        MainWindow.setStyleSheet(u"background-color:rgb(44, 44, 44)")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_Verschlsseln = QPushButton(self.centralwidget)
        self.pushButton_Verschlsseln.setObjectName(u"pushButton_Verschlsseln")
        self.pushButton_Verschlsseln.setGeometry(QRect(90, 170, 221, 131))
        self.pushButton_Verschlsseln.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_Verschlsseln.setStyleSheet(u" color:rgb(255, 255, 255);\n"
"font: 75 12pt \"Comic Sans MS\";background-color:rgb(90, 90, 90)")
        self.pushButton_Entschlsseln = QPushButton(self.centralwidget)
        self.pushButton_Entschlsseln.setObjectName(u"pushButton_Entschlsseln")
        self.pushButton_Entschlsseln.setGeometry(QRect(450, 170, 221, 131))
        self.pushButton_Entschlsseln.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_Entschlsseln.setStyleSheet(u" color:rgb(255, 255, 255);\n"
"font: 75 12pt \"Comic Sans MS\";background-color:rgb(90, 90, 90)")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(170, -10, 471, 81))
        self.label.setStyleSheet(u"font: 75 10pt \"Comic Sans MS\"; color:rgb(255, 255, 255)")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(330, 90, 101, 71))
        self.label_2.setStyleSheet(u"font: 75 8pt \"Comic Sans MS\"; color:rgb(255, 255, 255)\n"
"")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(290, 120, 41, 41))
        self.label_3.setStyleSheet(u"font: 75 28pt \"Comic Sans MS\"; color:rgb(255, 255, 255)")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(430, 120, 41, 41))
        self.label_4.setStyleSheet(u"font: 75 28pt \"Comic Sans MS\"; color:rgb(255, 255, 255)")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"font: 75 9.5pt \"Comic Sans MS\"; color:rgb(255, 255, 255);")
        self.lineEdit.setGeometry(QRect(320, 350, 121, 31))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(340, 320, 81, 31))
        self.label_5.setStyleSheet(u"font: 75 10pt \"Comic Sans MS\"; color:rgb(255, 255, 255)\n"
"")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 768, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton_Verschlsseln.clicked.connect(self.encrypt)
        self.pushButton_Entschlsseln.clicked.connect(self.decrypt)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"USB_Verschl\u00fcsseler", None))
        self.pushButton_Verschlsseln.setText(QCoreApplication.translate("MainWindow", u"Datei Verschl\u00fcsseln", None))
        self.pushButton_Entschlsseln.setText(QCoreApplication.translate("MainWindow", u"Datei Entschl\u00fcsseln", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Dateien verschl\u00fcsseln mit physischem USB-Schl\u00fcssel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"W\u00e4hle zwischen ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u2199", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u2198", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Password", None))
    # retranslateUi
    
    def encrypt(self):
        password = self.lineEdit.text()
        if not password:
            QMessageBox.about(None, "USBCrypt", "Empty password!")
            return

        file, check = QFileDialog.getOpenFileName(None, "Select file",".", "All Files ()")
        if not check:
            return
        print(f"Continuing with encrypting {file}")

        keyPath = getKeyPath(file)

        if not os.path.exists(keyPath):
            key = os.urandom(16)
            with open(keyPath, "wb") as file:
                # read the encrypted data
                file.write(key)

        key = open(keyPath, "rb").read()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=key,
            iterations=390000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(self.lineEdit.text().encode()))
        c_key = lib.Crypto(key)

        c_key.encrypt_file(str(file), str(file)) # overwrite

        QMessageBox.about(None, "USBCrypt", "verschlüsseln war erfolgreich! ✔     ")

    def decrypt(self):
        password = self.lineEdit.text()
        if not password:
            QMessageBox.about(None, "USBCrypt", "Empty password!")
            return

        file, check = QFileDialog.getOpenFileName(None, "Select file",".", "All Files ()")
        if not check:
            return
        print(f"Continuing with decrypting {file}")

        keyPath = getKeyPath(file)

        if not os.path.exists(keyPath):
            QMessageBox.about(None, "USBCrypt", "No key found, initialize the drive")
            return

        key = open(keyPath, "rb").read()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=key,
            iterations=390000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(self.lineEdit.text().encode()))
        c_key = lib.Crypto(key)

        try:
            rawData = c_key.decrypt_file(file)
            #deData = c_key.decrypt_file(file)
            #print(bytes.decode(deData))
            open(file,"wb").write(rawData)
            
        except cryptography.fernet.InvalidToken:
            print("Error: invalid password")
            QMessageBox.about(None, "USBCrypt", "Incorrect password!")

        QMessageBox.about(None, "USBCrypt", "entschlüsseln war erfolgreich! ✔     ")

