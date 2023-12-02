import requests

from utils import http_logger


def http_connect(**kwargs):
    host: str = kwargs["host"]
    http_port: int = int(kwargs["http_port"])
    qt_pings: int = int(kwargs["qt_pings"])

    http_logger.info("Playing ping pong with HTTP.")
    url = f'http://{host}:{http_port}'

    r = requests.get(url)
    http_logger.info(f'Verifying if server is up... {r}')
    for x in range(qt_pings):
        r = requests.post(url, f"Ping{x}")
        result = r.content.decode()
        http_logger.info(f"Received {result}.")
