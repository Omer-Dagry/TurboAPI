from dataclasses import dataclass
from typing import Dict

from .http import HTTPHeaders, HTTPHeader


@dataclass
class Response:
    status_code: str
    headers: Dict[HTTPHeaders | str, str]

    def _dump_headers(self) -> str:
        headers = ""
        for k, v in self.headers.items():
            headers += f"{k.value if type(k) is HTTPHeaders else k}: {v}{HTTPHeader.RN.value}"
        return headers if headers else HTTPHeader.RN.value

    def generate_response(self) -> str:
        return (
                HTTPHeader.HTTP_1_1.value + self.status_code + HTTPHeader.RN.value +
                self._dump_headers() + HTTPHeader.RN.value
        )
