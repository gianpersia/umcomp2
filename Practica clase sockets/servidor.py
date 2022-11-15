#servidor
import socket
import threading

host = "127.0.0.1"
port = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket establecido")
sock.bind((host, port))
print ("Socket bind ok")
sock.listen(1)
print ("Socket esperando")


def worker(*args):
    conn = args[0]
    addr = args[1]
    try:
        print('conexion con {}.'.format(addr))
        conn.send("server: Hola cliente".encode('UTF-8'))
        while True:
            datos = conn.recv(4096)
            if datos:
                print('recibido: {}'.format(datos.decode('utf-8')))
            else:
                print("Fin conexion cliente")
                break
        datos_upper = sock.recv(4096)
        conn.send("Enviaste: {}".encode('UTF-8'))
    finally:
        conn.close()

while 1:
    conn, addr = sock.accept()
    threading.Thread(target=worker, args=(conn, addr)).start()