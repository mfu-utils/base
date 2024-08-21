from App.Core import Config
from App.Core.Logger import Log
from App.Subprocesses import LpstatSubprocess


class LpstatController:
    # noinspection PyMethodMayBeStatic

    def devices(self, log: Log, config: Config):
        return LpstatSubprocess(log, config).get_printers_list()
