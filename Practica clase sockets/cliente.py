#cliente
import socket

host = "127.0.0.1"
port = 6666

sock = socket.socket()

sock.connect((host, port))

datos = sock.recv(4096)
print (datos.decode('utf-8'))



while True:


  message = input("Pasaje: ")
  sock.send(message.encode('utf-8'))




  if message == "exit":
    break
    print("Cerrando")
    sock.close()