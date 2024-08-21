import json
import os
from typing import List
import re

from App.Core import Config, Cache, Filesystem
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log
from App.Subprocesses.LpinfoSubprocess import LpinfoSubprocess
from config import CWD


class LpstatSubprocess(AbstractSubprocess):
    REGEX_DEVICES = re.compile("device for ([^:]+): ([^\n]+)")
    NO_DESTINATION_ADDED = "lpstat: No destinations added."

    def __init__(self, log: Log, config: Config, cache: Cache):
        super(LpstatSubprocess, self).__init__(log, config, "lpstat")

        self.__cache = cache

    def __get_cached_device_index(self, name: str) -> int:
        indexes = self.__cache.get('printers_indexes')

        if name not in indexes:
            idx = len(indexes)

            self.__cache.set(f'printers_indexes.{name}', idx)

        return self.__cache.get(f'printers_indexes.{name}')

    def create_device_object(self, parameters: tuple, direct_devices: list) -> dict:
        return {
            "index": self.__get_cached_device_index(parameters[0]),
            "display_name": parameters[0].replace("_", " "),
            "name": parameters[0],
            "device": parameters[1],
            "connected": parameters[1] in direct_devices
        }

    def get_printers_list(self) -> List[dict]:
        ok, out = self.run(parameters={"v": True})

        if self._config['debug']:
            return Filesystem.read_json(os.path.join(CWD, 'tests', 'dictionaries', 'devices.json'))

        if not ok:
            self._log.error(f"Cannot get list of printers. {out}", {"object": self})
            # TODO: add failed response
            return []

        if out == self.NO_DESTINATION_ADDED:
            return []

        direct_devices = LpinfoSubprocess(self._log, self._config).get_direct_devices()

        return list(map(lambda x: self.create_device_object(x, direct_devices), self.REGEX_DEVICES.findall(out)))
