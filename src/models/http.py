from __future__ import annotations

from typing import Union
from aiohttp import ClientSession

from .errors import RequestException

class HTTPType:
    JSON = 0
    TEXT = 1
    BYTES = 2

class HTTPClient(ClientSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }

    async def get(self, url, rtype = HTTPType.JSON, *args, **kwargs) -> Union[dict, str, bytes]:
        if args:
            args['User-Agent'] = self.user_headers['User-Agent']
        else:
            args = ({'User-Agent': self.user_headers['User-Agent']},)
        response = super().get(url, *args, **kwargs)
        if response.ok:
            if rtype == HTTPType.JSON:
                return await response.json()
            elif rtype == HTTPType.TEXT:
                return await response.text()
            elif rtype == HTTPType.BYTES:
                return await response.read()
        raise RequestException(response.status, response.reason)
