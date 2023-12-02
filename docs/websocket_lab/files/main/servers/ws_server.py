import asyncio

import websockets
from websockets import WebSocketServerProtocol, serve
from utils import ws_logger as logger, get_reply, format_header_as_str


# Função assíncrona para receber e responder às requisições via WebSocket.
async def ws_handler(websocket: WebSocketServerProtocol, path: str):
    # Mantém a conexão ativa.
    logger.info(f'Client connected. Request headers: {format_header_as_str(websocket.request_headers)}')
    while True:
        try:
            data = await websocket.recv()
            logger.info(f"Received data: {data}")
            await websocket.send(get_reply(data))
        except websockets.ConnectionClosedError as e:
            logger.debug(f'Connection terminated. [{e}]')
            break


def serve_ws(host: str, ws_port: int, **kwargs):
    logger.info(f'Starting WebSocket server at port: {ws_port}')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ws_server = serve(ws_handler, host, ws_port)
    loop.run_until_complete(ws_server)
    loop.run_forever()
