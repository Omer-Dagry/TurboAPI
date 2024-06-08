import socket
from pathlib import Path

from .http.utils import create_ssl_socket
from .http_server import HTTPServer


class HTTPSSLServer(HTTPServer):
    def __init__(self, host: str, port: int, certfile: Path, keyfile: Path) -> None:
        super().__init__(host, port)
        self._certfile = certfile
        self._keyfile = keyfile
        self._sock = None

    def _initiate_server(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket = create_ssl_socket(
            server_side=True,
            certfile=str(self._certfile),
            keyfile=str(self._keyfile)
        )
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        print(f"Server Started, Listening on port {self._host}:{self._port}")
