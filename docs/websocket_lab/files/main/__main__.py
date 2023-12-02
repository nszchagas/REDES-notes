import logging
import sys
import time
from multiprocessing import Process

from os import environ as getenv
from threading import Thread

from utils import logger

from http_module import http_connect, serve_http


# from ws import ws_connect, serve_ws

#


def main():
    pass


#
#         ws_tests = [Thread(target=f, args=[host, ws_port], kwargs={'qtd_pings': qt_pings}) for f in
#                     [serve_ws, ws_connect]]
#         [t.start() for t in ws_tests]
#
#
#
#         for i, t in enumerate(ws_tests + http_tests):
#             t.join()
#             logger.info(f'Finished server {i}.')

def get_input(prompt: str) -> str:
    global arg, args
    try:
        arg += 1
        return args[arg - 1]
    except IndexError:
        return input(prompt)


if __name__ == '__main__':
    d = {}
    arg = 1
    args = sys.argv

    try:
        d['host'] = str(getenv['host'])
        d['ws_port'] = int(getenv['ws_port'])
        d['http_port'] = int(getenv['http_port'])

    except KeyError as e:
        logger.error(f'Provide value for {e}.')
    logger.setLevel(logging.DEBUG)
    logger.debug(f'Starting with args: {d}')
    ops = [
        {
            'desc': 'Play ping pong with HTTP.',
            'server': serve_http,
            'client': http_connect
        },
        {
            'desc': 'Play ping pong with WS.',
            # 'server': serve_ws,
            # 'client': ws_connect
        },
    ]
    for i, x in enumerate(ops):
        print(f'[{i + 1}] {x["desc"]}')

    op = int(get_input('Choose test to run: ')) - 1
    play = ops[op]["desc"].lower()
    logger.debug(f'Starting server to {play}')

    server = Process(target=ops[op]['server'], kwargs=d)
    server.start()

    d['qt_pings'] = int(get_input("How many pings should I send?\n"))

    logger.debug(f'Starting client to {play}')

    client = Process(target=ops[op]['client'], kwargs=d)
    client.start()

    client.join()
    server.kill()
