import asyncio
import websockets
import socket

connected = set()

async def server(websocket, path):

    global json
    # Register.
    connected.add(websocket)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 9010))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                # async for message in websocket:
                json = conn.recv(1024)
                for connection in connected:
                    await connection.send(str(json)[1:])
                    print(json)
    finally:
        # Unregister.
        connected.remove(websocket)
    

def main():

    start_server = websockets.serve(server, "localhost", 9000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

main()