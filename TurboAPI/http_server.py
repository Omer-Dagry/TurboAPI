import socket
import ssl
import threading
from typing import Tuple

from .http import recv_http_request
from .request import Request
from .turbo_api import TurboAPI


class HTTPServer:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._server_socket: socket.socket | None = None

    def _initiate_server(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        print(f"Server Started, Listening on port {self._host}:{self._port}")

    def _accept_connection(self) -> Tuple[socket.socket, Tuple[str, int]]:
        client_socket, client_address = self._server_socket.accept()
        return client_socket, client_address

    @staticmethod
    def _handle_client(app: TurboAPI, client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
        try:
            method, uri, headers, body = recv_http_request(client_socket)
            print(f"{client_address[0]}:{client_address[1]} - {method} - {uri}")
            request = Request(uri, method, body, headers)
            res = app.handle_request(request)
            client_socket.sendall(res)
        finally:
            client_socket.close()

    def _run(self, app: TurboAPI) -> None:
        self._initiate_server()
        while Tuple:
            try:
                client_socket, client_address = self._accept_connection()
                threading.Thread(target=self._handle_client, args=(app, client_socket, client_address,)).start()
            except (ssl.SSLError, ConnectionError, socket.timeout, socket.error):
                pass

    def run(self, app: TurboAPI, blocking: bool = True) -> None:
        if blocking:
            return self._run(app)
        threading.Thread(target=self._run, args=(app,)).start()
