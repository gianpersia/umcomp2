import socket
import sys
import argparse as ap

if __name__ == "__main__":

    parser = ap.ArgumentParser(description="serversocket")
    parser.add_argument("-ho", "--host", type=str, #pongo "ho" porque con -h me toma como "help"
        help="Host deseado: ", required=True)
    parser.add_argument("-p", '--port', type=int,
        help="Puerto deseado: ", required=True)
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


    s.connect((args.host, args.port))  
    while True:
        datos=input(">")
        s.send(bytes(datos.encode('utf-8')))
        mensaje=s.recv(1024)
        print (mensaje.decode('utf-8'))



