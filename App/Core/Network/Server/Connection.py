from socket import socket, error
from threading import Thread
from typing import Tuple, Callable, Optional

from App.Core.Abstract import AbstractReceiveDataHandler
from App.Core.Network.Protocol import RCLProtocol


class Connection(Thread):
    def __init__(self, sock: socket, client: Tuple[str, int], handler: AbstractReceiveDataHandler, recv_bytes: int):
        super().__init__()

        self.__client = client

        self.__socket: socket = sock
        self.__handler = handler
        self.__received_data: bytes = b""
        self.__opened: bool = True
        self.__max_bytes_receive: int = recv_bytes
        self.__accepted = False
        self.__receive_len = None

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

    def __recv_segment(self) -> bytes:
        return self.__socket.recv(self.__max_bytes_receive)

    def __determinate_len(self):
        start_index = RCLProtocol.RCL_HEADER_INDEX_DATA_LENGTH
        end_index = start_index + RCLProtocol.RCL_HEADER_LEN_DATA_LENGTH

        _len = int.from_bytes(self.__received_data[start_index:end_index], 'big')

        self.__receive_len = RCLProtocol.RCL_HEADERS_LENGTH + _len + 4

    def __try_accept(self):
        try:
            if segment := self.__recv_segment():
                self.__received_data += segment

                self.__determinate_len()

                while len(self.__received_data) < self.__receive_len:
                    self.__received_data += self.__recv_segment()

                self.__accepted = True

        except error as e:
            self.__error_message = str(e)

    def run(self):
        while True:
            if not self.__opened:
                break

            if self.__wait_receive():
                self.__socket.sendall(self.__handler.handle(self.__received_data))

                self.close()

    def __wait_receive(self) -> bool:
        try:
            self.__try_accept()

            return self.__accepted

        except error:
            self.close()

        return False
