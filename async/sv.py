import asyncio
import os
import subprocess
import argparse as ap

async def ejecutor(reader, writer):
    while True:
        mensaje=(await reader.read(1024)).decode().strip()
        print(mensaje)
        if mensaje == 'exit':
            writer.close()
            await writer.wait_closed()
            break
        print("Mensaje: ", mensaje)
        proceso = subprocess.Popen([mensaje], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        salida, error= proceso.communicate()
        print("Salida: \n", salida)
        print("Error: \n", error)
        if salida == b"":
            error=b"ERROR\n"+error
            writer.write(error)
        else:
            salida=b"OK\n"+salida
            writer.write(salida)
        
        await writer.drain()

async def main(port):
    server = await asyncio.start_server(ejecutor, '127.0.0.1', port)

    async with server:
        await server.serve_forever()



if __name__ == "__main__":
    parser = ap.ArgumentParser(description="serversocket")
    parser.add_argument("-p", "--port", type=int,
        help="Puerto deseado: ", required=True)
    args=parser.parse_args()
    asyncio.run(main(args.port))