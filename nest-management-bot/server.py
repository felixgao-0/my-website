import asyncio
import json
import ssl
from typing import Literal, Optional

from websockets.asyncio.server import serve
import websockets

# Maintain a list of connected clients
clients: dict = {}


async def send_error(websocket, error_msg, *, possible=True, disconnect=True) -> None:
    """
    Formats an error message in json to be sent to the client.
    :param websocket: Websocket instance to use
    :param error_msg: The message to be formatted
    :param possible: If this error is possible with a correct client
    :param disconnect: Disconnect the server after the error message is sent
    :return:
    """
    await websocket.send(json.dumps(
            {
                'message': f'{error_msg}{' This shouldn\'t happen, send a message in #slack-management-bot for help.' if not possible else ''}',
                'status': 'error'
            }
        ))
    if disconnect:
        await websocket.close()


async def server(websocket):
    try:
        # Client info validation
        try:
            first_message_json = await asyncio.wait_for(websocket.recv(), timeout=60)
        except asyncio.TimeoutError:
            await send_error(websocket, 'Authentication message was not received.', possible=False)
            return

        try:
            first_message = json.loads(first_message_json)
        except json.decoder.JSONDecodeError:
            await send_error(websocket, 'Authentication message isn\'t json.', possible=False)
            return

        if first_message.get('version') != "0.1.0a":
            await send_error(websocket, 'Invalid client version or malformed data.', possible=False)
            return

        await websocket.send(json.dumps({'status': 'info', 'message': 'Authenticated :D'}))

        # End client authentication :D

        # Add client to list to use for sending messages later
        clients[f'{websocket.id}']: websocket = websocket
        print("ACTIVE CLIENTS:", clients.keys())


        try:
            cmd_response = await asyncio.wait_for(
                send_message('download raid shadow legends!', f'{websocket.id}', message_type='command'),
                5
            )
        except asyncio.TimeoutError:
            await send_error(websocket, 'Did not receive a response in time', possible=False)
            return

        print(f"RESPONSE: {cmd_response}")


        async for message in websocket:
            print(f"Received message: {message}")
            if message == "close":
                await websocket.close()
                return

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        clients.pop(f'{websocket.id}')
        print("ACTIVE CLIENTS:", clients.keys())


async def send_message(message: str, user_uuid: str, *, message_type: Literal['info', 'command']) -> Optional[dict]:
    """
    Sends a message of either "info" or "command" type
    :param message: The message to send
    :param user_uuid: The client to send a message to
    :param message_type: The type of message, a response will be returned if the type is "command"
    :return:
    """
    await clients[user_uuid].send(json.dumps({'status': message_type, 'message': message}))
    response_json = await clients[f'{user_uuid}'].recv()

    if message_type == 'command':
        try:
            response = json.loads(response_json)
        except json.decoder.JSONDecodeError:
            await send_error(await clients[f'{user_uuid}'], 'Invalid Response', possible=False)
            return

        if response.get('status') == 'command_response':
            return response
        else:
            await send_error(await clients[f'{user_uuid}'], 'Invalid Response type', possible=False)


async def main():
    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #ssl_context.load_cert_chain("cert.pem", "private_key.pem")

    async with serve(server, "localhost", 8989):#, ssl=ssl_context):
        print("server running...")
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())