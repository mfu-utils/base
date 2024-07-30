from abc import ABC, abstractmethod


class AbstractConnectionHandler(ABC):

    @abstractmethod
    def handle(self, address: str, port: str) -> bool:
        pass
