import time
import os
import sys
import multiprocessing as multi

def lee_input(w, q):
    print("Hijo pide mensaje") #mensaje a introducir al pipe
    sys.stdin = open(0)
    input = sys.stdin.readline()
    w.send(input)
    w.close()
    print("Mensaje encriptado: %s" % q.get())

def lee_pipe(r, q):
    print("Esperando pipe")
    input = r.recv()
    print("Pipe leido: %s" % str(input))
    r.close()
    mensaje = rot13(str(input))
    q.put(mensaje)

def rot13(msj):
    print("Mensaje a encriptar: %s" % str(msj))
    mensaje = []
    for caracter in msj[:-1]:
        desplazo = ord(caracter) + 13
        if ord(caracter) >= 97 and ord(caracter) <= 122:
            if desplazo > 122:
                desplazo = desplazo - 122 + 97 - 1
        else:
            if desplazo > 90:
                desplazo = desplazo - 90 + 65 - 1
        caracter_encr = chr(desplazo)
        mensaje.append(caracter_encr)
    return "".join(mensaje)

if __name__ == '__main__':
    r, w = multi.Pipe()
    q = multi.Queue()
    hijo = multi.Process(target= lee_input, args=(w, q))
    hijo_segundo = multi.Process(target= lee_pipe, args=(r, q))
    hijo.start()
    hijo_segundo.start()
    hijo.join()
    hijo_segundo.join()

