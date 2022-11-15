import socket
import sys
import socketserver
import subprocess
import argparse as ap


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

if __name__ == "__main__":
    parser = ap.ArgumentParser(description="serversocket")
    parser.add_argument("-p", "--port", type=int,
                        help="Puerto deseado: ", required=True)
    parser.add_argument("-c", '--concurrencia',
                        help="Modo de concurrencia: ")
    args = parser.parse_args()

    host, port = "localhost", args.port
    socketserver.TCPServer.allow_reuse_address = True
    if args.concurrencia=='p':
        with serverProcesos((host, port), MyTCPHandler) as servidor:
            servidor.serve_forever()
    if args.concurrencia=='t':
        with serverHilos((host, port), MyTCPHandler) as servidor:
            servidor.serve_forever()
