import logging

# Setup logger
logging.basicConfig(format="[%(levelname)s %(asctime)s] (%(name)s): %(message)s",
                    level=logging.INFO,
                    datefmt="%H:%M:%S")

logger = logging.getLogger('main')
http_logger = logging.getLogger('HTTP')
ws_logger = logging.getLogger('WS')


def get_reply(data: str):
    if "ping" in data.lower():
        return 'Pong!'
    return f'Data {data} received successfully.'


def format_header_as_str(headers) -> str:
    h = dict(headers)
    # print(h.keys())
    infos = ['Connection', 'Host', 'User-Agent', 'Content-Length']
    return '; '.join([f'{k}: {h.get(k)}' for k in infos if h.get(k)])
