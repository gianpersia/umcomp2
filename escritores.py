import argparse as ap
import os
from os import fork
import string
import time


def p_hijos(n, r, f, v):
    archivo = open(f, "w") # abre el archivo para escritura (si no existe lo crea)
    for _ in range(n):
        fpid = fork()  # crea el proceso hijo
        letra = string.ascii_uppercase[_] # establece la letra del abecedrio correspondiente al numero en _
        if fpid == 0:
            pid = os.getpid()
            resultado = escribir(pid, r, letra, archivo, v)
            exit(0)

def escribir(pid, r, letra, archivo, v):  # funcion para escribir en el archivo
    for _ in range(r):
        if v:
            print(f'Proceso {pid} escribiendo letra {letra}')
        archivo.write(letra) # escribe la letra en el archivo
        archivo.flush() # limpia la cache del archivo
        time.sleep(1) # duerme el programa 1 segundo


def main():

    parser = ap.ArgumentParser(description="Escritores")
    parser.add_argument("-n", "--N", type=int,
                        help="Numero de procesos que se desea crear", required=True)
    parser.add_argument("-r", "--R", type=int,
                        help="Numero de veces a escribir", required=True)
    parser.add_argument("-f", "--ruta_archivo", type=str,
                        help="Ruta del archivo a escribir", required=True)
    parser.add_argument("-v", action='store_true',
                        help="Ejecutar programa en modo verboso")
    args = parser.parse_args()
    p_hijos(args.N, args.R, args.ruta_archivo, args.v)
    os.wait()


if __name__ == '__main__':
    main()