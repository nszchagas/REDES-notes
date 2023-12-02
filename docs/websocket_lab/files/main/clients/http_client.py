import requests

from utils import client_logger as logger


def http_connect(host, http_port: int, qt_pings: int, **kwargs):
    logger.info("Playing ping pong with HTTP.")
    url = f'http://{host}:{http_port}'
    sent = 0
    r = requests.get(url)
    logger.info(f'Verifying if server is up... {r}')
    for x in range(qt_pings):
        r = requests.post(url, f"Ping{x}")
        result = r.content.decode()
        logger.info(f"Received {result}.")
        sent += 1

    assert sent == qt_pings
    logger.info(f'Sent {sent} pings. Finishing test.')
