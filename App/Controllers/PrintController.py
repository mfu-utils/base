from App.Core import Config
from App.Core.Logger import Log
from App.Subprocesses import PrintingSubprocess


class PrintController:
    # noinspection PyMethodMayBeStatic
    def invoke(self, parameters: dict, log: Log, config: Config):
        PrintingSubprocess(log, config).print(parameters)
