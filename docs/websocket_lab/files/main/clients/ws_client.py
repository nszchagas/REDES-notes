import asyncio

from websocket import WebSocket
from websocket import create_connection

from utils import client_logger as logger


def ws_connect(host: str, ws_port: int, qt_pings: int = 5, **kwargs):
    logger.info("Playing ping pong with WebSocket:")
    url = f'ws://{host}:{ws_port}'
    logger.info(f'Creating connection on {url}.')
    ws: WebSocket = create_connection(url)
    sent = 0
    try:
        for x in range(qt_pings):
            if ws.connected:
                ws.send(f"Ping {x}!")
                result = ws.recv()
                logger.info(f"Received {result}.")
                sent += 1

        ws.close()
        assert sent == qt_pings
        logger.info(f'Sent {sent} pings. Closing connection.')
    except Exception as e:
        raise Exception(e)
