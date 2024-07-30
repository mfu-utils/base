from abc import ABC, abstractmethod
from typing import Union


class AbstractResponse(ABC):
    def __init__(self, data: Union[str, dict, list, bytes]):
        self._data = data

    def data(self) -> Union[str, dict, list, bytes]:
        return self._data

    @staticmethod
    @abstractmethod
    def type() -> int:
        pass
