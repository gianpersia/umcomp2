import asyncio
import os
import subprocess

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

async def main():
    server = await asyncio.start_server(ejecutor, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    #print(f'Serving on {addr} {asyncio.current_task()}')

    async with server:
        print(f"Tareas:\n{asyncio.all_tasks()}")
        await server.serve_forever()

asyncio.run(main())