from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer

from utils import http_logger as logger, get_reply, str_from_header


# Classe que recebe e responde às requisições HTTP, com métodos GET e POST
# implementados.
class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._log_request_info('GET')
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, HTTP!')

    def do_POST(self):
        self._log_request_info('POST')
        # Recupera a quantidade de caracteres para ler do quadro
        # enviado.
        content_length = int(
            self.headers.get('Content-Length'))
        data = self.rfile.read(
            content_length).decode('utf-8')
        logger.info(f"Received POST data: {data}")
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(get_reply(data).encode('utf-8'))

    def _log_request_info(self, method: str):
        logger.info(
            f'Method: {method}. Request headers: '
            f'{str_from_header(self.headers)}')


def serve_http(host: str, http_port: int, **kwargs):
    httpd = TCPServer((host, http_port), HTTPHandler)
    logger.info(
        f'Starting HTTP server at port: {http_port}')
    httpd.serve_forever()
