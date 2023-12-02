import requests

from utils import http_logger as logger


def http_connect(host, http_port: int, qt_pings: int, **kwargs):

    logger.info("Playing ping pong with HTTP.")
    url = f'http://{host}:{http_port}'

    r = requests.get(url)
    logger.info(f'Verifying if server is up... {r}')
    for x in range(qt_pings):
        r = requests.post(url, f"Ping{x}")
        result = r.content.decode()
        logger.info(f"Received {result}.")
