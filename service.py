from config import settings
from fastapi import HTTPException

class Service:
    def __init__(self):
        self._base_url = ""

    def _build_base_url(
        self,
        host: str = None,
        port: str = None,
        endpoint: str = None,
        param: str = None
    ):
        url = "http://"
        if host is not None:
            url += host
        if port is not None:
            url += ':' + port
        if endpoint is not None:
            url += '/' + endpoint
        if param is not None:
            url += '/' + param
        print(url)
        self._base_url = url

    def _check_response(
        self,
        response
    ):
        if not response.is_success:
            raise HTTPException(
                status_code=response.status_code, 
                detail=response.text
            )
        

    def _build_endpoint_url(
        self,
        endpoint: str = None,
        param: str = None
    ):
        url = self._base_url
        if endpoint is not None:
            url += '/' + endpoint
        if param is not None:
            url += '/' + param
        print(url)
        return url