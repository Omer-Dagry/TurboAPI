from pathlib import Path

from TurboAPI import TurboAPI, Request, Response
from TurboAPI.http import ContentTypes, HTTPHeaders
from TurboAPI import HTTPSSLServer

app = TurboAPI()
app.mount_folder("/webroot")


@app.get("/")
def index(response: Response) -> str:
    response.headers[HTTPHeaders.CONTENT_TYPE] = ContentTypes.HTML.value
    return Path("webroot/index.html").read_text()


@app.get("/test")
def test(request: Request, response: Response) -> bytes:
    print(request)
    print(response)
    return b"hello world!"


def main() -> None:
    HTTPSSLServer("0.0.0.0", 443, Path("certificate.crt"), Path("privateKey.key")).run(app)


if __name__ == '__main__':
    main()
