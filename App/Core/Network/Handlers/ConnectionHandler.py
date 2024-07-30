from App.Core.Abstract import AbstractConnectionHandler


class ConnectionHandler(AbstractConnectionHandler):
    def handle(self, address: str, port: str) -> bool:
        return True
