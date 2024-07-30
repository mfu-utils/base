from App.Subprocesses.Server.ScanImage import ScanImage
from App.Core import Config
from App.Core.Logger import Log

from App.helpers import cache


class ScanController:
    # noinspection PyMethodMayBeStatic
    def invoke(self, parameters: dict, log: Log, config: Config):
        if data := ScanImage(log, config).scan(parameters):
            return data

        return None

    # noinspection PyMethodMayBeStatic
    def devices(self, log: Log, config: Config, parameters: dict):
        update = parameters.get('update') or False

        if update or not cache().has('devices'):
            cache('devices', ScanImage(log, config).device_list())

        return cache('devices')
