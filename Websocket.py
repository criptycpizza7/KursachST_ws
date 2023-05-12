import asyncio
import websockets

connected = set()

async def websocket_handler(websocket, path):
    print('ws handler')
    connected.add(websocket)
    # while True:
    #     print('while true')
    #     for connection in connected:
    #         try:
    #             await connection.ensure_open()
    #         except websockets.exceptions.ConnectionClosed:
    #             print("WebSocket connection closed")
    #             connected.remove(websocket)
    #         except websockets.exceptions.ConnectionClosedOK:
    #             print('Closed ok')
    #             await connected.remove(websocket)
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            # Handle the WebSocket message as needed
            # ...
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")
    finally:
        # Remove the client from the connected set when the connection is closed
        connected.remove(websocket)


# Start WebSocket server
async def start_websocket_server():
    print('start ws')

    async with websockets.serve(websocket_handler, 'localhost', 9000):
        print('9000 started')
        await asyncio.Future()  # Keep the WebSocket server running indefinitely


async def handle_grpc(reader, writer):

    print('handle grpc')

    data = await reader.read(1024)
    print(data)

    await send_data_via_websocket(data=data)
    writer.close()


async def start_grpc_server():
    print('start grpc')
    server = await asyncio.start_server(handle_grpc, 'localhost', 9010)

    async with server:
        print('9010 started')
        await server.serve_forever()


async def send_data_via_websocket(data):
    for connection in connected:
        # Send multiple messages over the same WebSocket connection
        await connection.send(str(data)[2 : -1])


# Start the WebSocket server in a separate task
async def run_websocket_server():
    print('run_ws')
    await start_websocket_server()


# Start both servers concurrently
async def start_servers_concurrently():
    print(2)
    # await asyncio.gather(
    #     start_servers(),
    #     run_websocket_server()
    # )

    server_grpc = asyncio.create_task(start_grpc_server())
    server_ws = asyncio.create_task(start_websocket_server())

    await asyncio.gather(server_grpc, server_ws)



print('run')
main_loop = asyncio.get_event_loop()
# asyncio.run(start_servers_concurrently())
main_loop.run_until_complete(start_servers_concurrently())
main_loop.run_forever()
print('no')