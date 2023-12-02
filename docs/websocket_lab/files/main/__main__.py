import datetime
import sys
import time
from multiprocessing import Process
from typing import Callable

from utils import logger, get_env
from servers import serve_ws, serve_http
from clients import http_connect, ws_connect


def get_input(prompt: str) -> str:
    global arg, args
    try:
        arg += 1
        return args[arg - 1]
    except IndexError:
        return input(prompt)


def get_option() -> int:
    return int(get_input('Choose quantity of pings to run [-1 to exit]: '))


def run_option(desc: str, server: Process, client: Callable) -> dict:
    global d, pings
    d['qt_pings'] = pings
    play = desc.lower()

    if not server.is_alive():
        logger.debug(f'Starting server to {play}')
        server.start()

    c = Process(target=client, kwargs=d)

    logger.debug(f'Starting client to {play[:-2]} with {pings} pings.')
    start = datetime.datetime.now()

    c.start()
    c.join()

    end = datetime.datetime.now()
    result = {
        'server': server.name,
        'qt_pings': d['qt_pings'],
        'start': start.isoformat(),
        'end': end.isoformat(),
        'duration': end - start,
    }
    logger.info(f'Finished run. Results: {result}')
    return result


def format_results(results: list[dict]):
    if not len(results):
        return

    table = []
    max_widths = [max(len(str(k)), len(str(v))) for k, v in results[0].items()]
    headers = [key.replace("_", " ")
               .capitalize()
               .ljust(max_widths[i])
               for i, key in enumerate(results[0].keys())]
    header = '|' + ' | '.join(headers) + '|'
    separators = '|' + ' | '.join(['-' * x for x in max_widths]) + '|'

    print(header)
    print(separators)
    table += [header, separators]
    for r in results:
        row = '|' + ' | '.join(str(value).ljust(max_widths[i]) for i, value in enumerate(r.values())) + '|'
        print(row)
        table.append(row)

    return table


def main():
    global d
    results = []
    logger.setLevel(d['log_level'])
    logger.debug(f'Running with args: {" ".join([f"{k}={v}" for k, v in d.items()])}.')
    ops = [
        {
            'desc': 'Play ping pong with WS.',
            'server': Process(target=serve_ws, kwargs=d, name=' WS '),
            'client': ws_connect
        },
        {
            'desc': 'Play ping pong with HTTP.',
            'server': Process(target=serve_http, kwargs=d, name='HTTP'),
            'client': http_connect
        },
    ]

    try:
        global pings
        pings = get_option()
        while pings != -1:
            for op in ops:
                results.append(run_option(**op))
            pings = get_option()

    except Exception as e:
        logger.error(e)
        raise Exception(e)
    finally:
        for s in [d['server'] for d in ops if d['server'].is_alive()]:
            logger.info(f'Stopping process: {s.name}.')
            s.kill()
        return results


if __name__ == '__main__':
    arg = 1
    pings = 50
    args = sys.argv
    d = get_env()
    rs = main()
    table = format_results(rs)

    with open('report.md', 'w', encoding='utf-8') as results:
        results.write('\n'.join(table))
