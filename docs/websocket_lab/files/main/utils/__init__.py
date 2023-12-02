import logging
import socket
from os import environ

# Setup logger
logging.basicConfig(
    format="[%(levelname)s %(asctime)s] (%(name)s): %(message)s",
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


def str_from_header(headers) -> str:
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


def format_results(results: list[dict]):
    if not len(results):
        return

    table = []
    max_widths = [max(len(str(k)), len(str(v)))
                  for k, v in results[0].items()]
    headers = [key.replace("_", " ")
               .capitalize()
               .ljust(max_widths[i])
               for i, key in enumerate(results[0].keys())]
    header = '|' + ' | '.join(headers) + '|'
    separators = '|' + \
                 ' | '.join(['-' * x for x in max_widths]) + '|'

    print(header)
    print(separators)
    table += [header, separators]
    for r in results:
        row = '|' + \
              ' | '.join(str(value).ljust(max_widths[i])
                         for i, value in enumerate(r.values())) + '|'
        print(row)
        table.append(row)

    return table
