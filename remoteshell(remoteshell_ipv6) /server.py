import socket
import sys
import socketserver
import subprocess
import argparse as ap
from multiprocessing import Process


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            mensaje=self.request.recv(1024).strip()
            print(mensaje)
            if mensaje == b'exit':
                break
            proceso = subprocess.Popen([mensaje], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            salida, error= proceso.communicate()
            print("Salida: \n", salida)
            print("Error: \n", error)
            if salida == b"":
                error=b"ERROR\n"+error
                self.request.sendall(error)
            else:
                salida=b"OK\n"+salida
                self.request.sendall(salida)
            
class serverProcesos(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

class serverHilos(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class serverProcesos6(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6

class serverHilos6(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6

def ipv4(host, port, concurrencia):
    socketserver.TCPServer.allow_reuse_address = True

    if concurrencia=='p':
        with serverProcesos((host, port), MyTCPHandler) as servidor:
            servidor.serve_forever()
    if concurrencia=='t':
        with serverHilos((host, port), MyTCPHandler) as servidor:
            servidor.serve_forever()

def ipv6(host, port, concurrencia):
    socketserver.TCPServer.allow_reuse_address = True

    if concurrencia=='p':
        with serverProcesos6((host, port), MyTCPHandler) as servidor:
            servidor.serve_forever()
    if concurrencia=='t':
        with serverHilos6((host, port), MyTCPHandler) as servidor:
            servidor.serve_forever()

if __name__ == "__main__":
    
    parser = ap.ArgumentParser(description="serversocket")
    parser.add_argument("-p", "--port", type=int,
                        help="Puerto deseado: ", required=True)
    parser.add_argument("-c", '--concurrencia',
                        help="Modo de concurrencia: ")
    args = parser.parse_args()

    host, port = "localhost", args.port

    direcciones = socket.getaddrinfo("localhost", args.port, socket.AF_UNSPEC, socket.SOCK_STREAM)

    procesos=[]
    for direccion in direcciones:
        if str(direccion[0])=="AddressFamily.AF_INET":
            procesos.append(Process(target=ipv4,args=(host, port, args.concurrencia,)))
        if str(direccion[0])=="AddressFamily.AF_INET6":
            procesos.append(Process(target=ipv6,args=(host, port, args.concurrencia,)))

    for p in procesos:
        p.start()