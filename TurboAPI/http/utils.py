import socket
import ssl
from typing import Tuple, Dict, List

from .consts import HTTPHeader, HTTPHeaders


def parse_headers(headers: List[str]) -> Dict[str, str]:
    headers_dict = {}
    for header in headers:
        header_name, header_value = header.split(":", 1)
        headers_dict[header_name.strip()] = header_value.strip()
    return headers_dict


def recv_http_request(client_socket: socket.socket) -> Tuple[str, str, Dict[str, str], bytes]:
    header = b""
    while b"\r\n\r\n" not in header:
        res = client_socket.recv(1)
        if res == b"":
            raise ConnectionError("Connection closed")
        header += res

    header = header.decode()
    headers_split = header[:-len(HTTPHeader.RNRN.value)].split(HTTPHeader.RN.value)
    method, uri = headers_split[0].split()[:2]
    parsed_headers = parse_headers(headers_split[1:])

    body = b""
    content_length = int(parsed_headers.get(HTTPHeaders.CONTENT_LENGTH.value, 0))
    while len(body) < content_length:
        res = client_socket.recv(content_length - len(body))
        if res == b"":
            raise ConnectionError("Connection closed")
        body += res

    return method.upper(), uri, parsed_headers, body


def create_ssl_socket(
        server_side: bool,
        certfile: str,
        keyfile: str
) -> ssl.SSLSocket:
    sock = socket.socket()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) if server_side else ssl.create_default_context()
    if server_side:
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    else:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    return context.wrap_socket(sock, server_side=server_side)
