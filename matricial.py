from multiprocessing import pool
import os
import math
import multiprocessing as multi
import subprocess as sub
import sys
import time
import argparse
from ast import Global

matriz = []
global argumentos

def main():
    global argumentos
    parse = argparse.ArgumentParser(description="-p Procesos, -f Ubicacion, -c funcion_calculo")
    parse.add_argument("-p", "--cant_procesos", type=int, required=True, help="string")
    parse.add_argument("-f", "--ruta", type=str, required=True, help="string")
    parse.add_argument("-c", "--funcion_calculo", type=str, required=True, help="string")
    argumentos = parse.parse_args()

    print('Ingreso: %d' % argumentos.cant_procesos)
    print('Contenido archivo: %s' % argumentos.ruta) 
    print('Final: %s' % argumentos.funcion_calculo)

    if not (argumentos.funcion_calculo == 'pot' or argumentos.funcion_calculo == 'raiz' or argumentos.funcion_calculo == 'log'):
        print("Incorrecto")
        os._exit(0)
    
    with open(argumentos.ruta, "r") as archivo:
        for line in archivo:
            l = [int(num) for num in line.split(',')]
            print(l)
            matriz.append(l)
    
    pool = multi.Pool(processes = int(argumentos.cant_procesos))

    resultados = []
    resultados = pool.map_async(funcion, matriz).get()
    print("obteniendo resultados...")

    for linea in resultados:
        print(linea)

def funcion(matrix):
    global argumentos
    res = []
    if argumentos.funcion_calculo == 'pot':
        for num in matrix:
            res.append(math.pow(int(num), int(num)))
    elif argumentos.funcion_calculo == 'raiz':
        for num in matrix:
            res.append(math.sqrt(int(num)))
    elif argumentos.funcion_calculo == 'log':
        for num in matrix:
            res.append(math.log10(int(num)))
    return res


if __name__ == '__main__':
    main()