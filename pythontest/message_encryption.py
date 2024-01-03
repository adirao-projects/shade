# Encryption Libraries
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import os
import secrets
import pandas as pd
import io
from hashlib import blake2b
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import textwrap

class AddressBook:
    def __init__(self, address_book_path=""):
        self.__address_book_path = address_book_path
        self.__address_book = pd.DataFrame(columns=["name", "address"])
        self.__address_book.set_index("name", inplace=True)
        self.__address_book_hash = ""
        self.__address_book_hash_check = ""
    
    def loadAddressBook(self):
        self.__address_book = pd.read_csv(self.__address_book_path)
        self.__address_book.set_index("name", inplace=True)
        self.__address_book_hash = self.__address_book_hash_check
    
    def addAddress(self, name, address):
        self.__address_book.loc[name] = address
        self.__address_book_hash = self.__address_book_hash_check


class Encryption:
    def __init__(self, password, salt=""):
        self.__password = password
        self.__salt = salt
        self.__pepper = "5BH|g1%Cg7Cbx7^JnuVM[?3N~BLdK\>A=GQV_M~@uk8;?,x*fayFQ8-nL\eo|FHGf\>6xL;rsW7Rw3aYe_]Q[Zv>=uFm^OroZ3][wq<wPWjYf~6jLrcmMPOYz3O3OTT!"
        self.__key=""
        
    def encryptKey(self):
        password_encoded = self.__pepper.encode('utf-8') + \
            self.__password.encode('utf-8')
        
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.__salt.encode('utf-8'),
                iterations=10000,
                backend = default_backend()
            )
        
        key = base64.urlsafe_b64encode(kdf.derive(password_encoded))
        self.__key = key

    def encryptValue(self, data):
        data_encrypted = Fernet(self.__key).encrypt(data.encode('utf-8'))
        return data_encrypted.decode('utf-8')
    
    def encryptFile(self,file_path):
        with open(file_path,'rb') as f:
            data=f.read()
        data_encrypted = Fernet(self.__key).encrypt(data.encode('utf-8'))
        return data_encrypted.decode('utf-8')
    
    def decryptValue(self,data):
        decrypted_data=Fernet(self.__key).decrypt(data.encode('utf-8'))
        return decrypted_data.decode('utf-8')
    

class Messege(Encryption):
    def __init__(self, data="", sender="", receiver="", signature=""):
        super().__init__(signature)
        self.data = Fernet(self.__key).encrypt(data.encode('utf-8'))
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.messengers = []

    def splice(self):
        split_length = len(self.data)//len(self.messengers)
        messege_splits = textwrap.wrap(self.data, split_length)
        checksum = SHA256(bytes(self.data)).hexdigest()

        for i, m in enumerate(messege_splits):
            messege_splits[i] = self.package(m, i, checksum)

        return messege_splits

    def package(self, data, slice, checksum):
        messege = {
            "data": data,
            "slice": slice,
            "sender": self.sender,
            "receiver": self.receiver,
            "checksum": checksum
        }

        return messege
        