from App.Core import Config, MimeTypeConfig, Platform
from App.Core.Logger import Log
from App.Subprocesses import PrintingSubprocess


class PrintController:
    # noinspection PyMethodMayBeStatic
    def invoke(self, parameters: dict, log: Log, config: Config, mime: MimeTypeConfig, platform: Platform):
        return PrintingSubprocess(log, config, mime, platform).print(parameters)
