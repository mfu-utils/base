from socket import socket, error
from threading import Thread
from typing import Tuple, Callable, Optional

from App.Core.Abstract import AbstractReceiveDataHandler


class Connection(Thread):
    def __init__(self, sock: socket, client: Tuple[str, int], handler: AbstractReceiveDataHandler, recv_bytes: int):
        super().__init__()

        self.__client = client

        self.__socket: socket = sock
        self.__handler = handler
        self.__received_data: bytes = b""
        self.__opened: bool = True
        self.__max_bytes_receive: int = recv_bytes

        self.__close_callback: Optional[Callable[[Tuple[str, int]], None]] = None

    def opened(self) -> bool:
        return self.__opened

    def client(self) -> Tuple[str, int]:
        return self.__client

    def set_close_callback(self, callback: Callable[[Tuple[str, int]], None]):
        self.__close_callback = callback

    def close(self) -> None:
        if self.__close_callback:
            self.__close_callback(self.__client)

        self.__opened = False

        self.__socket.close()

    def run(self):
        while True:
            if not self.__opened:
                break

            if self.__wait_receive():
                self.__socket.sendall(self.__handler.handle(self.__received_data))

                self.close()

    def __wait_receive(self) -> bool:
        try:
            data = self.__socket.recv(self.__max_bytes_receive)

            if not data:
                return False

            self.__received_data = data
            return True

        except error:
            self.close()

        return False
