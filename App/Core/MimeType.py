import platform
from typing import Union, Optional, List
from App.Core import Config

import magic


class MimeType:
    CONFIG_FILE = 'mime'

    def __init__(self, _config: Config):
        self.__config = _config
        self.__mime_types = {}

    def get_mime_types(self, key: str) -> List[str]:
        key = f"{MimeType.CONFIG_FILE}.{key}"

        if not (data := self.__mime_types.get(key)):
            self.__mime_types[key] = self.__config.get(key)

        return data or self.__mime_types[key]

    @staticmethod
    def get_mime(file: Union[str, bytes]) -> Optional[str]:
        _type = None

        if isinstance(file, bytes):
            _type = magic.from_buffer(file, mime=True)

        if platform.system() == 'Windows':
            with open(file, 'rb') as f:
                _type = magic.from_buffer(f.read(2048), mime=True)
        elif isinstance(file, str):
            _type = magic.from_file(file, mime=True)

        return _type

    def has_type(self, file: Union[str, bytes], types: str) -> bool:
        _type = MimeType.get_mime(file)

        if _type is None:
            return False

        return _type in self.get_mime_types(types)
