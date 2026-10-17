from datetime import datetime
import os
import sys
import time
import shutil

def ruta_completa(archivo):
    if getattr(sys, "frozen", False):
        carpeta = os.path.dirname(sys.executable)
    else:
        carpeta = os.path.dirname(os.path.abspath(__file__))
    
    rutaCompleta = os.path.join(carpeta, archivo)
    return rutaCompleta

def imp(mensaje):

    print(mensaje)


def imp_derecha(mensaje):
    ancho = shutil.get_terminal_size().columns

    imp(mensaje.rjust(ancho))


def lea(mensaje):

    mens = input(mensaje)
    return mens


def intLea(mensaje, impErr):

    while True:
        try:
            valor = int(input(mensaje))
            return valor
        
        except ValueError:
            print(impErr)


def escribir_log(mensaje):
    fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ruta_completa("log.txt"), "a", encoding= "utf-8") as f:
        f.write(f"{fechaHora} - {mensaje}\n")


def salir():
    imp("\nFin del programa")
    time.sleep(1)
    imp("¡Nos vemos luego!")
    time.sleep(1)
    sys.exit()
