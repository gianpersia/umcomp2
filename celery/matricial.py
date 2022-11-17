import argparse
import calcmatriz
import os

def main():
    matriz = []
    parse = argparse.ArgumentParser(description="-f Ubicacion, -c calcmatriz")
    parse.add_argument("-f", "--ruta", type=str, required=True, help="string")
    parse.add_argument("-c", "--calcmatriz", type=str, required=True, help="string")
    argumentos = parse.parse_args()
    ruta = argumentos.ruta
    operacion = argumentos.calcmatriz

    if not (argumentos.calcmatriz == 'raiz' or argumentos.calcmatriz == 'log' or argumentos.calcmatriz == 'pot'):
        print("Incorrecto")
        os._exit(0)
    
    with open(argumentos.ruta, "r") as archivo:
        for line in archivo:
            l = [int(num) for num in line.split(',')]
            print(l)
            matriz.append(l)
    
    for linea in matriz:
        print(linea)

    resultados = funcion(matriz, operacion)
    print("obteniendo resultados...")

    for linea in resultados:
        print(linea)

def funcion(matrix, operacion):
    res = []
    lineares = []
    for linea in matrix:
        lineares = []
        for elem in linea:
            if(operacion == 'raiz'):
                res = calcmatriz.raiz.delay(int(elem))
            if(operacion == 'log'):
                res = calcmatriz.pot.delay(int(elem))
            if(operacion == 'pot'):
                res = calcmatriz.log_d.delay(int(elem))
            lineares.append(res.get())
        res.append(lineares)
    return res

if __name__ == '__main__':
    main()