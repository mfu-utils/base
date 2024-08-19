import json
from typing import List, Type, Dict, Union
from enum import Enum


class Casts:
    @staticmethod
    def enum2dict(enum: Union[Type[Enum], List[Enum]], names: Dict[str, str] = None) -> dict:
        if not names:
            names = {}

        return dict(map(lambda x: (x.value, names.get(x.value) or x.name), enum))

    @staticmethod
    def str2bool(value: str) -> bool:
        value = value.lower()

        if value in ['yes', 'true', 't', 'y', '1']:
            return True
        elif value in ['no', 'false', 'f', 'n', '0']:
            return False

        raise ValueError(f'Value {value} is not a boolean')

    @staticmethod
    def bool2str(value: bool) -> str:
        return "True" if value else "False"

    @staticmethod
    def str2int(value: str) -> int:
        if value.isdigit():
            return int(value)

        return 0

    @staticmethod
    def str_to(value: str, _type: type):
        if _type == bool:
            return Casts.str2bool(value)

        if _type == int:
            return Casts.str2int(value)

        if _type == list:
            return Casts.str2list(value)

        return _type(value)

    @staticmethod
    def str2list(value: str) -> List[str]:
        return json.loads(value or '[]')

    @staticmethod
    def str2int_list(value: str) -> list:
        return list(map(lambda x: int(x), Casts.str2list(value)))
