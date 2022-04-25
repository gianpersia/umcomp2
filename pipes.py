import os
from os import fork
import argparse
import subprocess as sub


def main():
    parser = argparse.ArgumentParser(description="Inverter")
    
    parser.add_argument("-f", "--path", type=str, required=True, help="Ingrese direccion:")
    arguments = parser.parse_args()
    with open(arguments.path, "r") as archivo:
        renglones_totales = sum(1 for line in archivo)
    r = [[] for x in range(renglones_totales)]
    w = [[] for y in range(renglones_totales)]
    r1 = [[] for z in range(renglones_totales)]
    w1 = [[] for w in range(renglones_totales)]
    archivo = open(arguments.path, "r")
    count = 0
    for line in archivo:
        invertido(line, r, w, r1, w1, count)
        count = count + 1
    for i in range(renglones_totales):
        r1[i] = os.fdopen(r1[i])
        renglon = r1[i].read()
        print("%s" % renglon)
        os.wait()
    archivo.close()

def invertido(renglon, r, w, r1, w1, i):
    r[i], w[i]=os.pipe()
    r1[i], w1[i]=os.pipe()
    pid=fork()
    if pid==0:
        os.close(w[i])
        os.close(r1[i])
        r[i]=os.fdopen(r[i])
        renglon=r[i].read()
        w1[i] = os.fdopen(w1[i],'w')
        w1[i].write("%s" % renglon[::-1])
        w1[i].flush()
        w1[i].close
        os._exit(0)
    else:
        os.close(r[i])
        os.close(w1[i])
        w[i] = os.fdopen(w[i],'w')
        w[i].write("%s" % renglon)
        w[i].flush()
        w[i].close()




if __name__ == '__main__':
    main()