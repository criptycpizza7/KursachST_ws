import asyncio
import websockets
import socket
import select

connected = set()

message = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9010))
s.listen()
print('9010 started')

async def websocket_handler(websocket, path):
    # while True:
    #     ws_message = await websocket.recv()
    #     print(f"Received message: {ws_message}")

    connected.add(websocket)


# Start WebSocket server
async def start_websocket_server():
    async with websockets.serve(websocket_handler, 'localhost', 9000):
        await asyncio.Future()  # Keep the WebSocket server running indefinitely

async def send_data_via_websocket(data):
    async for connection in connected:
        # Send multiple messages over the same WebSocket connection
        await connection.send(data)

def start_servers():
    socket_fd = s.fileno()
    socket_map = {socket_fd: s}

    global message

    while True:
        readable, _, _ = select.select([socket_fd], [], [])

        for sock in readable:
            if sock == socket_fd:
                client_socket, address = s.accept()
                # Handle the incoming socket connection as needed
                # ...
                print(f"Accepted connection from {address}")
                print(f"Received data: {client_socket.recv(65568)}")
                message = client_socket.recv(65568)
                send_data_via_websocket(message)
            else:
                data = sock.recv(1024)
                if data:
                    # Handle the incoming socket data as needed
                    # ...
                    print(f"Received data: {data}")

# Start the WebSocket server in a separate task
async def run_websocket_server():
    print('run_ws')
    await start_websocket_server()

# Start both servers concurrently
async def start_servers_concurrently():
    print(2)
    await asyncio.gather(
        start_servers(),
        run_websocket_server()
    )

print('run')
asyncio.run(start_servers_concurrently())
print('no')