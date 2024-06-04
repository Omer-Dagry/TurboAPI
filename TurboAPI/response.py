from dataclasses import dataclass
from typing import Dict

from TurboAPI.http import HTTPHeaders


@dataclass
class Response:
    status_code: str
    headers: Dict[HTTPHeaders | str, str]

    def dump_headers(self) -> str:
        headers = ""
        for k, v in self.headers.items():
            headers += f"{k.value if type(k) is HTTPHeaders else k}: {v}\r\n"
        return headers
