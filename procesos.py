# Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:
# -n <numero>
# -h
# -v
# El programa debe generar <numero> procesos hijos, y cada proceso calculará la suma de todos los números enteros pares entre 0 y su número de PID.
# El programa deberá mostrar por pantalla:
# PID – PPID : <suma_pares>
# El proceso padre debe esperar a que todos sus hijos terminen.
# La opción -h mostrará ayuda de uso, y la opción -v habilitará el modo verboso de la aplicación.
# El modo verboso debe mostrar, además de la suma, un mensaje al inicio y al final de la ejecución de cada proceso hijo,
# que indique su inicio y fin.


import argparse as ap
import os
from os import fork


def p_hijos(n, v):
    for _ in range(n):
        fpid = fork()  # crea el proceso hijo
        if fpid == 0:
            suma = 0
            pid = os.getpid()
            ppid = os.getppid()
            if v:
                print(f'Inicio del proceso {pid}')
            resultado = calcular(pid, suma)
            if v:
                print(f'Fin del proceso {pid}')
            print(f'{pid} - {ppid} : {resultado}')
            exit(0)

def calcular(pid, suma):  # realiza la suma de los numeros pares entre 0 y el pid
    for i in range(0, pid + 1, 2): 
        suma = i + suma
    return suma


def main():

    parser = ap.ArgumentParser(description="Forking")
    parser.add_argument("-n", "--numero", type=int,
                        help="Numero de procesos que se desea crear", required=True)
    parser.add_argument("-v", action='store_true',
                        help="Ejecutar programa en modo verboso")
    args = parser.parse_args()
    p_hijos(args.numero, args.v)
    os.wait()


if __name__ == '__main__':
    main()
