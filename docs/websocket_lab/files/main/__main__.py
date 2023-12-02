import logging
import sys
import time
from multiprocessing import Process
from typing import Callable

from utils import logger, get_env
from http_module import http_connect, serve_http


# from ws_module import ws_connect, serve_ws

def get_input(prompt: str) -> str:
    global arg, args
    try:
        arg += 1
        return args[arg - 1]
    except IndexError:
        return input(prompt)


def get_option() -> int:
    for i, x in enumerate(ops):
        print(f'[{i + 1}] {x["desc"]}')
    y = int(get_input('Choose test to run [-1 to exit]: '))
    if y == -1:
        return y
    return y - 1


def start_server(s: Process):
    retries = 5
    while retries:
        try:
            s.start()
        except OSError as e:
            s.kill()
            logger.warn(f'Retrying... [{e}]')
            time.sleep(1)
            retries -= 1
        else:
            break

        logger.error('Failed to start server after retries.')


def run_option(desc: str, server: Process, client: Callable):
    global d
    play = desc.lower()
    logger.debug(f'Starting server to {play}')

    if not server.is_alive():
        server.start()

    d['qt_pings'] = int(get_input("How many pings should I send?\n"))
    c = Process(target=client, kwargs=d)

    logger.debug(f'Starting client to {play}')
    c.start()
    c.join()


if __name__ == '__main__':
    arg = 1
    args = sys.argv
    d = get_env()

    logger.setLevel(logging.DEBUG)
    logger.debug(f'Starting with args: {d}')

    ops = [
        {
            'desc': 'Play ping pong with HTTP.',
            'server': Process(target=serve_http, kwargs=d, name='HTTP Server'),
            'client': http_connect
        },
        # {
        # 'desc': 'Play ping pong with WS.',
        # 'server': serve_ws,
        # 'client': ws_connect
        # },
    ]
    try:
        op = get_option()
        while op != -1:
            run_option(**ops[op])
            op = get_option()
        for s in [d['server'] for d in ops]:
            logger.info(f'Stopping process: {s.name}.')
            s.kill()
    except Exception as e:
        logger.error(e)
