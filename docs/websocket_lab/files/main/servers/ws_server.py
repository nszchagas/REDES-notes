import asyncio

from websockets import WebSocketServerProtocol, serve
from utils import ws_logger as logger, get_reply, str_from_header


# Função assíncrona para receber e responder às requisições via
# WebSocket.
async def ws_handler(websocket: WebSocketServerProtocol, path: str):
    logger.info(
        f'Client connected. Request headers: '
        f'{str_from_header(websocket.request_headers)}')
    # Mantém a conexão ativa.
    while True:
        try:
            data = await websocket.recv()
            logger.info(f"Received data: {data}")
            await websocket.send(get_reply(data))

        except Exception as e:
            logger.info(f'Connection terminated. [{e}]')
            break


def serve_ws(host: str, ws_port: int, **kwargs):
    logger.info(
        f'Starting WebSocket server at port: {ws_port}')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ws_server = serve(ws_handler, host, ws_port)
    loop.run_until_complete(ws_server)
    loop.run_forever()
