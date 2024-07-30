#: BUILD_TYPE:server
from App.Core.Abstract import AbstractConnectionHandler, AbstractReceiveDataHandler
from App.Core.Network import TcpServer
#: END:BUILD_TYPE:server
#: BUILD_TYPE:!server
from App.Core.Network import TcpClient
from App.Core.Network.Client import ResponseDataPromise, ClientConfig
from App.Core.Utils.ExecLater import ExecLater
from App.Core.Network.Protocol.Requests import AbstractRequest
#: END:BUILD_TYPE:!server
from App.Core import Config
from App.Core.Logger import Log
from App.Core.Network.Protocol import RCL


class NetworkManager:
    def __init__(self, log: Log, config: Config, rcl: RCL):
        self.__logger = log
        self.__config = config
        self.__protocol = rcl

    def __debug(self, message: str):
        self.__logger.debug(message, {'object': self})

    #: BUILD_TYPE:server
    def start_server(self, connection_handler: AbstractConnectionHandler, receive_handler: AbstractReceiveDataHandler):
        debug = self.__config.get('server.debug')

        server = TcpServer(self.__config, self.__logger, connection_handler, receive_handler)

        server.daemon = self.__config.get('server.daemon')

        server.start()

        if debug:
            self.__debug('Server started.')

        try:
            server.join()
        except (KeyboardInterrupt, SystemExit):
            if debug:
                message = f"Server stopped{' by timeout' if server.is_alive() else ''}"

                self.__logger.debug(message, {'object': self})
    #: END:BUILD_TYPE:server

    #: BUILD_TYPE:!server
    def request(self, request: AbstractRequest, config: ClientConfig) -> ResponseDataPromise:
        try:
            client = TcpClient(config, self.__protocol, self.__logger)

            client.start()

            if config.debug:
                self.__debug(f"Client started")

            return client.send(self.__protocol.create_request(request))
        except KeyboardInterrupt:
            if config.debug:
                self.__logger.debug(f"Client stopped.")
        except (ConnectionRefusedError, TimeoutError) as e:
            self.__logger.error(f'Cannot connect to server. {str(e)}')

            promise = ResponseDataPromise(self.__protocol)

            ExecLater(10, lambda: promise.set_error('Cannot connect to server.')).start()

            return promise

    #: END:BUILD_TYPE:!server
