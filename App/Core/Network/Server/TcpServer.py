from socket import socket, SOL_SOCKET, SOCK_STREAM, AF_INET
from threading import Thread
from typing import List

from App.Core.Abstract import AbstractConnectionHandler, AbstractReceiveDataHandler
from App.Core.Logger import Log
from App.Core import Config

from App import Application
from App.Core import Platform

from .Connection import Connection

platform: Platform = Application().get('platform')

if not platform.is_windows():
    from socket import SO_REUSEPORT


class TcpServer(Thread):
    def __init__(
            self,
            config: Config,
            logger: Log,
            connection_handler: AbstractConnectionHandler,
            receive_data_handler: AbstractReceiveDataHandler,
    ):
        super().__init__()

        self.__logger = logger
        self.__connection_handler = connection_handler
        self.__receive_data_handler = receive_data_handler

        self.__config = config.get('server')
        self.__max_bytes = self.__config["max_bytes_receive"]

        self.__connections: List[Connection] = []

        self.__socket = self.create(self.__config)
        self.__is_running = True

    @staticmethod
    def create(config: dict) -> socket:
        sock = socket(AF_INET, SOCK_STREAM)

        if config['reuse_socket'] and not platform.is_windows():
            sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, True)

        sock.bind((config['address'], config['port']))
        sock.listen(config['max_incoming_connections'])

        return sock

    def close(self):
        self.__socket.close()

    def terminate(self):
        self.__socket.close()
        self.__is_running = False

    def __close_connection_handler(self, connection: Connection, addr: tuple):
        if connection in self.__connections:
            self.__connections.remove(connection)

        self.__logger.debug(f"Close connection. Address: {addr[0]}; Port: {addr[1]};", {"object": self})

    def run(self):
        while self.__is_running:
            try:
                sock, (address, port) = self.__socket.accept()
            except OSError:
                break

            if not self.__connection_handler.handle(address, port):
                self.__logger.debug(f"Connection refused: {address}, {port}")
                continue

            connection = Connection(sock, (address, port), self.__receive_data_handler, self.__max_bytes)
            connection.set_close_callback(lambda x: self.__close_connection_handler(connection, x))

            self.__connections.append(connection)

            connection.start()

            self.__logger.debug(f"Open connection. Address: {address}; Port: {port};", {
                "object": self
            })
