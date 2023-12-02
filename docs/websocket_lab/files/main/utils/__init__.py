import logging
import socket
from os import environ

# Setup logger
logging.basicConfig(format="[%(levelname)s %(asctime)s] (%(name)s): %(message)s",
                    level=logging.INFO,
                    datefmt="%H:%M:%S")

logger = logging.getLogger('main')
http_logger = logging.getLogger('HTTP')
ws_logger = logging.getLogger('WS')
client_logger = logging.getLogger('CLIENT')


def get_reply(data: str):
    if "ping" in data.lower():
        return 'Pong!'
    return f'Data {data} received successfully.'


def format_header_as_str(headers) -> str:
    h = dict(headers)
    return '; '.join([f'{k}: {h.get(k)}' for k in h.keys()])


def get_env() -> dict:
    try:
        host = str(environ['host'])

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('', 0))
        ws_port = soc.getsockname()

        soc_http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc_http.bind(('', 0))
        http_port = soc_http.getsockname()

        return {'host': host,
                'ws_port': ws_port[1],
                'http_port': http_port[1],
                'log_level': environ['log_level'].upper()}
    except KeyError as e:
        logger.error(f'Provide value for {e}.')
