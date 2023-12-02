from websocket import create_connection

from files.main.utils import ws_logger


def ws_connect(host: str, ws_port: int, qtd_pings: int = 5):
    ws_logger.info("Playing ping pong with WebSocket:")
    url = f'ws://{host}:{ws_port}'
    ws_logger.info(f'Creating connection on {url}.')
    ws = create_connection(url)
    for x in range(qtd_pings):
        ws.send(f"Ping {x}!")
        result = ws.recv()
        ws_logger.info(f"Received {result}.")
    ws.close()
