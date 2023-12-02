import asyncio
from websockets import WebSocketServerProtocol, serve
from utils import ws_logger as logger, get_reply


# Função assíncrona para receber e responder às requisições via WebSocket.
async def ws_handler(websocket: WebSocketServerProtocol, path: str):
    logger.info(f'Client connected on path: {path}. Requesting info...')
    logger.info(f'Client headers: {websocket.request_headers}')
    data = await websocket.recv()
    logger.info(f'Websocket received data: {data}')
    await websocket.send(get_reply(data))


def serve_ws(host: str, ws_port: int, **kwargs):
    logger.info(f'Starting WebSocket server at port: {ws_port}')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ws_server = serve(ws_handler, host, ws_port)
    loop.run_until_complete(ws_server)
    loop.run_forever()
