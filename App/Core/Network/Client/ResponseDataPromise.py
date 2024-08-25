import time
from typing import Optional, Callable, Tuple, Union

from App.Core.Network.Protocol import RCL
from App.Core.Network.Protocol.Responses.AbstractResponse import AbstractResponse


class ResponseDataPromise:
    STATUS_WAIT = 1
    STATUS_SUCCESS = 2
    STATUS_ERROR = 3

    def __init__(self, rcl: RCL):
        self.__rcl = rcl
        self.__status = self.STATUS_WAIT
        self.__data: bytes = b""
        self.__error: Optional[str] = None
        self.__on_success: Optional[Callable[[AbstractResponse], None]] = None
        self.__on_error: Optional[Callable[[Optional[str]], None]] = None

    def wait_result(self) -> Tuple[bool, Union[Optional[str], AbstractResponse]]:
        while self.__status == self.STATUS_WAIT:
            time.sleep(0.05)
            continue

        if self.__status == self.STATUS_SUCCESS:
            return True, self.__rcl.parse_response(self.__data)

        if self.__status == self.STATUS_ERROR:
            return False, self.__error

    def set_result(self, data: bytes):
        self.__data = data

        if self.__on_success:
            self.__on_success(self.__rcl.parse_response(data))

        self.__status = ResponseDataPromise.STATUS_SUCCESS

    def set_error(self, message: str) -> None:
        self.__error = message

        if self.__on_error:
            self.__on_error(message)

        self.__status = ResponseDataPromise.STATUS_ERROR

    def then(self, callback: Callable[[AbstractResponse], None]):
        self.__on_success = callback

        return self

    def catch(self, callback: Callable[[Optional[str]], None]):
        self.__on_error = callback

        return self

    def status(self) -> int:
        return self.__status

    def data(self) -> bytes:
        return self.__data

    def error(self) -> str:
        return self.__error
