import asyncio
import json
import ssl
import pathlib

import aioconsole
import websockets
from websockets.asyncio.client import connect


__version__ = "0.1.0a" # Use for later version checking


async def client():
    uri = "ws://localhost:8989"

    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    #ssl_context.load_verify_locations("cert.pem")

    print("Attempting to connect to server...")
    async for websocket in connect(uri):#, ssl=ssl_context):
        print("Connected to server...")
        await websocket.send(json.dumps({'version': __version__}))

        async for message_json in websocket:
            try:
                message = json.loads(message_json)
            except json.decoder.JSONDecodeError:
                raise Exception('Broke the server code prob lol') # TODO: Replace w/ better handling

            msg_status = message.get('status')
            msg_data = message.get('message')
            if msg_status == 'command':
                msg_data = msg_data
                print(f'COMMAND: {msg_data}')
                await websocket.send(json.dumps({'status': 'command_response', 'message': 'i downloaded it already, let my family go!'}))

            elif msg_status == 'error':
                print(f'ERROR: {msg_data}')
                ...
            elif msg_status == 'info':
                print(f'MESSAGE: {msg_data}')
            else:
                ... # idk



if __name__ == "__main__":
    asyncio.run(client())
