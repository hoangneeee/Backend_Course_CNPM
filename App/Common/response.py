import http
import os
from typing import Any, Optional, Dict
from dotenv import load_dotenv

load_dotenv()

info = {
    'version': os.getenv('VERSION'),
    'app_name': os.getenv('APP_NAME'),
    'author': os.getenv('AUTHOR')
}

'''Response Section'''
class HTTPException(Exception):
    def __init__(self, status_code: int, status_message: str = None, data: str = None) -> None:
        if data is None:
            data = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.status_message = status_message
        self.data = data

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, " \
               f"status_message={self.status_message!r}, " \
               f"data={self.data!r})"


class ResponseData(HTTPException):
    def __init__(
        self,
        status_code: int,
        status_message: str = None,
        data: Optional[Dict[str, Any]] = None,
        info: Optional[Dict[str, Any]] = info,
    ) -> None:
        super().__init__(status_code=status_code, status_message=status_message, data=data)
        self.info = info
