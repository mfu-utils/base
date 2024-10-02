from abc import ABC, abstractmethod


class AbstractReceiveDataHandler(ABC):
    @abstractmethod
    def handle(self, data: bytes) -> bytes:
        pass
