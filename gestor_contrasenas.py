from os.path import expanduser
home = expanduser("~")

directorio = home + '/gestor_contrasenas'

import os
os.chdir(directorio)

import numpy as np
import pandas as pd
import re
import random
import string

from Crypto.Cipher import AES
import hashlib

#generar_contrasena()

def generar_contrasena():
    
    caracteres_especiales = re.sub(r"\[|\]|\(|\)|\\|/|\{|\}|<|>|\||`|\'|\"|\^", 
                                   "", 
                                   string.punctuation)

    caracteres = string.ascii_letters + string.digits + caracteres_especiales

    mayuscula = random.choice(string.ascii_uppercase)
    minuscula = random.choice(string.ascii_lowercase)
    numero = random.choice(string.digits)
    caracter_especial = random.choice(caracteres_especiales)

    otros = random.choices(caracteres, k = 6)
    
    lista_caracteres = [mayuscula, minuscula, numero, caracter_especial] + otros
    
    contrasena = "".join(np.random.choice(lista_caracteres, 
                                          size = 10, 
                                          replace = False))
    return(contrasena)

#validar_contrasena()

def validar_contrasena(contrasena):

    caracteres_especiales = re.sub(r"\[|\]|\(|\)|\\|/|\{|\}|<|>|\||`|\'|\"|\^", 
                                       "", 
                                       string.punctuation)
    tiene_mayuscula = re.search(r"[A-Z]", contrasena)
    tiene_minuscula = re.search(r"[a-z]", contrasena)
    tiene_numero = re.search(r"[0-9]", contrasena)
    tiene_caracter_especial = np.any([i in contrasena \
                                      for i in caracteres_especiales])
    
    if(len(contrasena) >= 10 and \
       tiene_mayuscula and \
       tiene_minuscula and \
       tiene_numero and \
       tiene_caracter_especial):
       print("La contraseña es válida.".encode("utf-8"))
    else:
        print("La contraseña no es válida.".encode("utf-8"))

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

#AESCipher()

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

#leer_contrasenas()

def leer_contrasenas():

    contrasenas_cifradas = pd.read_csv("contrasenas.csv")

    contrasenas = contrasenas_cifradas.copy()
    contrasenas['contrasena'] = [cipher.decrypt(i) \
               for i in contrasenas_cifradas['contrasena']]
    return(contrasenas)

#guardar_contrasenas()

def guardar_contrasenas(contrasenas):

    contrasenas_cifradas = contrasenas.copy()

    contrasenas_cifradas['contrasena'] = [str(cipher.encrypt(i), "utf-8") \
                        for i in contrasenas['contrasena']]

    contrasenas_cifradas.to_csv('contrasenas.csv', index = False)

#salir()

def salir():
    exit()

#crear_contrasena_maestra()

def crear_contrasena_maestra():

    raw_1 = input("Escribir contraseña: ".encode("utf-8"))
    raw_2 = input("Escribir de nuevo la contraseña: ".encode("utf-8"))

    if raw_1 == raw_2:

        archivo = open("contrasena_maestra", "wb")
        archivo.write(hashlib.sha256(raw_1.encode()).digest());
        archivo.close()
        
        global contrasena_maestra
        contrasena_maestra = raw_1
        
        contrasenas = pd.DataFrame({
        'login':[], 
        'contrasena':[]
        })
    
        contrasenas.to_csv("contrasenas.csv", index = False)
        
    else:
        print("Las contraseñas no coinciden".encode("utf-8"))

#verificar_contrasena_maestra()

def verificar_contrasena_maestra():

    raw = input("Ingresar contrasena maestra: ")
    
    archivo = open("contrasena_maestra", "rb")
    contrasena = archivo.read()
    archivo.close()
    
    if hashlib.sha256(raw.encode()).digest() == contrasena:
        global contrasena_maestra
        contrasena_maestra = raw
        return(1)
    else:
        return(0)

#agregar_cuenta()

def agregar_cuenta(*args):
        
    contrasenas = leer_contrasenas()
    
    for cuenta in args:
        if cuenta not in contrasenas['login'].values:
    
            contrasenas = contrasenas.append({'login':cuenta, 
                                              'contrasena':generar_contrasena()}, 
                                              ignore_index = True)
    
            guardar_contrasenas(contrasenas)
        else:
            print("Fallo al agregar cuenta " + cuenta + ": el nombre ya existe.")

#mostrar_cuenta()

def mostrar_cuenta(*args):

    if len(args) == 0:
        contrasenas = leer_contrasenas()
        print(contrasenas)
    else:
        contrasenas = leer_contrasenas()
        print(contrasenas[contrasenas['login'].isin(args)])

#eliminar_cuenta()

def eliminar_cuenta(*args):
    
    contrasenas = leer_contrasenas()
    
    for cuenta in args:
        
        if cuenta in contrasenas['login'].values:
            
            contrasenas = contrasenas.query('login not in @cuenta')
    
            guardar_contrasenas(contrasenas)
            
        else:
            print("No se encontró la cuenta " + cuenta + ".")

#cambiar_contrasena()

def cambiar_contrasena(*args):

    contrasenas = leer_contrasenas()
    if len(args) == 0:
        n = len(contrasenas['contrasena'])
        contrasenas['contrasena'] = np.array([generar_contrasena() for i in range(n)])
        
        guardar_contrasenas(contrasenas)
    else:
        n = len(contrasenas[contrasenas['login'].isin(args)])
        contrasenas['contrasena'][contrasenas['login'].isin(args)] = np.array([generar_contrasena() for i in range(n)])
        
        guardar_contrasenas(contrasenas)

#cambiar_contrasena_maestra()

def cambiar_contrasena_maestra():

    raw = input("Ingresar contrasena maestra: ")
    
    archivo = open("contrasena_maestra", "rb")
    contrasena = archivo.read()
    archivo.close()
    
    if hashlib.sha256(raw.encode()).digest() == contrasena:

        raw_1 = input("Escribir contraseña: ".encode("utf-8"))
        raw_2 = input("Escribir de nuevo la contraseña: ".encode("utf-8"))
    
        if raw_1 == raw_2:
    
            archivo = open("contrasena_maestra", "wb")
            archivo.write(hashlib.sha256(raw_1.encode()).digest());
            archivo.close()
            
            global contrasena_maestra
            contrasena_maestra = raw_1
            global cipher
            cipher = AESCipher(contrasena_maestra)
        else:
            print("Las contraseñas no coinciden".encode("utf-8"))

    else:
        print("La contraseña es incorrecta.".encode("utf-8"))

#ayuda()

def ayuda():

    print("Se pueden usar las siguientes funciones:\n\nsalir()\nayuda()\n\nagregar_cuenta()\nmostrar_cuenta()\neliminar_cuenta()\n\ncambiar_contrasena()\ncambiar_contrasena_maestra()")

#menu()

def menu():

    comando = None
    print("Escribir ayuda() para ver más opciones. Para salir, escribir salir().")
    
    while comando != "salir":
        
        raw = input("$ ")
        comando_raw = re.search(r"(^.*)(\(.*)", raw).group(1)
        
        if comando_raw in ["salir", "ayuda", "agregar_cuenta", "mostrar_cuenta", 
                           "eliminar_cuenta", "cambiar_contrasena", 
                           "cambiar_contrasena_maestra"]:
            comando = comando_raw
            eval(raw)
        
        else:
            print("Función inválida. Para más información escribir ayuda().")

#inicio()

def inicio():

    while(not os.path.exists('contrasena_maestra')):
        print("Para usar el gestor de contraseñas, se tiene que crear una contraseña maestra.".encode("utf-8"))
        crear_contrasena_maestra()
    
    autenticado = 0

    while autenticado == 0:
        autenticado = verificar_contrasena_maestra()
        if autenticado == 0:
            print("La contraseña es incorrecta.".encode("utf-8"))
    global cipher
    cipher = AESCipher(contrasena_maestra)
    menu()

inicio()
