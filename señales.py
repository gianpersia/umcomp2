import os
import argparse as ap
import sys
import signal as sig
import mmap

parser = ap.ArgumentParser(description="Señales")
parser.add_argument("-f", "--path", type=str, required=True, help="Path al archivo a leer")
args = parser.parse_args()
mem_comp = mmap.mmap(-1,1024)
h1 = 0
h2 = 0
archivo = open(args.path, 'wb')

def leer_memoria_comp(n, frame):
    mem_comp.seek(0) # Offset en 0
    leer = mem_comp.readline() # Se lee la linea en la memoria compartida
    print(f'PID {os.getpid()} --> Leido: {leer.decode()}')
    os.kill(h2, sig.SIGUSR1)# Envia la señal SIGUSR1 a h2

def enviar_signal_h1(n, frame):
    print(f'PID {os.getpid()} --> Terminando H1...')
    os.kill(h2, sig.SIGUSR2) # Envia la señal SIGUSR2 a h2
    sig.signal(sig.SIGUSR1, sig.SIG_DFL)

def enviar_signal_h2(n, frame):
    mem_comp.seek(0) # Offset en 0
    leer = mem_comp.readline().decode().upper().encode() # convierte la linea a mayusculas
    print(f'PID {os.getpid()} --> Linea convertida: {leer.decode()}')
    archivo.write(leer) # Imprime la linea convertida en el archivo
    archivo.flush() # Limpia el buffer del archivo

def terminar_h2(n, frame): # h2 recibe SIGUSR2 y termina
    print(f'PID {os.getpid()} --> Terminando H2...')
    os._exit(0)

def señales():

    print(f'PID del proceso padre {os.getpid()}')

    sig.signal(sig.SIGUSR1, leer_memoria_comp) # el proceso padre lee lo que ingreso el hijo 1 en la memoria compartida
    sig.signal(sig.SIGUSR2, enviar_signal_h1) # h1 avisa al padre

    global h1
    h1 = os.fork() # se crea el hijo 1
    if not h1:
        archivo.close()
        for linea in sys.stdin: # para cada linea
            if linea == "bye\n":
                print("Terminando procesos...")
                os.kill(os.getppid(), sig.SIGUSR2) # h1 manda una señal SIGUSR2 al padre
                break
            else:
                mem_comp.resize(len(linea)) # Redimensiona el buffer de la memoria compartida con el largo de la linea
                mem_comp.seek(0) # Offset al ppio de la linea
                mem_comp.write(linea.encode()) # Se escribe la linea ingresada en la memoria compartida
                mem_comp.seek(0) # Vuelvo a poner el offset en 0
                os.kill(os.getppid(), sig.SIGUSR1) # h1 manda la señal SIGUSR2 al padre 
        print(f'PID H1: {os.getpid()} --> Terminando...')
        os._exit(0) # h1 termina

    global h2
    h2 = os.fork() # se crea el hijo 2
    if not h2:
        sig.signal(sig.SIGUSR1, enviar_signal_h2)
        sig.signal(sig.SIGUSR2, terminar_h2) 
        while True: # h2 queda esperando a que h1 ingrese una linea
            print(f'PID H1: {h1} --> Ingrese una linea ("bye" para salir): ')
            sig.pause()
        #os._exit(0)

    sig.pause()
    print(f'PID {os.getpid()} --> Esperando terminar...')
    os.wait() 
    print(f'PID {os.getpid()} --> Terminando...')


if __name__ == '__main__':
    señales()