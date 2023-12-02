import asyncio
from websockets import WebSocketServerProtocol, serve
from files.main.utils import ws_logger, get_reply


# Função assíncrona para receber e responder às requisições via WebSocket.
async def ws_handler(websocket: WebSocketServerProtocol, path: str):
    ws_logger.info(f'[WS] Client connected on path: {path}. Requesting info...')
    ws_logger.info(f'[WS] Client headers: {websocket.request_headers}')
    data = await websocket.recv()
    ws_logger.info(f'[WS] Websocket received data: {data}')
    await websocket.send(get_reply(data))


def serve_ws(host: str, ws_port: int):
    ws_logger.info(f'Starting WebSocket server at port: {ws_port}')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ws_server = serve(ws_handler, host, ws_port)
    loop.run_until_complete(ws_server)
    loop.run_forever()
