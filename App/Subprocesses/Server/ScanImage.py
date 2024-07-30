import os
from typing import Optional

from App.Core import Config, Filesystem
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log
from config import CWD


class ScanImage(AbstractSubprocess):
    OUTPUT_PARAMETER_NAME = 'output'
    FORMAT_DEVICE_LIST_PARAMETER_NAME = 'formatted-device-list'
    DONT_SCAN_PARAMETER_NAME = 'dont-scan'

    def __init__(self, log: Log, config: Config):
        super().__init__(log, config, 'scanimage')

        self.__file_path = config.get('scan.tmp_file')
        self.__scan_debug = config.get('scan.debug')

        self.set_multi_character_parameters_delimiter('=')

    def scan(self, parameters: dict) -> Optional[bytes]:
        if self.__scan_debug:
            self._log.warning(f'Scan debug mode enabled. Return test data. Scanning parameters: {parameters}')

            return Filesystem.read_file(str(os.path.join(CWD, "tests", "images", f"demo.{parameters['format']}")), True)

        if not Filesystem.exists(_dir := os.path.dirname(self.__file_path)):
            self._log.warning(f"Create scan tmp directory '{_dir}'")
            os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)

        parameters.update({ScanImage.OUTPUT_PARAMETER_NAME: self.__file_path})

        ok, message = self.run([], parameters)

        if ok:
            return Filesystem.read_file(self.__file_path, True)

        self._log.error(f'Failed to scan: {message}')

        return None

    def device_list(self) -> list:
        ok, content = self.run(parameters={
            self.DONT_SCAN_PARAMETER_NAME: True,
            self.FORMAT_DEVICE_LIST_PARAMETER_NAME: ','.join([
                '%i', '%d', '%v', '%m', '%t%n'
            ])
        })

        devices = []

        if not ok:
            return devices

        for device_data in content.split('\n'):
            parameters = device_data.split(',')

            devices.append({
                'model': parameters[3],
                'vendor': parameters[2],
                'device': parameters[1],
                'index': parameters[0],
                'type': parameters[4].split(' '),
            })

        return devices
