from App.Core import Config, MimeTypeConfig, Platform
from App.Core.Logger import Log
from App.Core.Network.Protocol.Responses.ResponseInternalError import ResponseInternalError
from App.Subprocesses import PrintingSubprocess


class PrintController:
    # noinspection PyMethodMayBeStatic
    def invoke(self, parameters: dict, log: Log, config: Config, mime: MimeTypeConfig, platform: Platform):
        ok, message = PrintingSubprocess(log, config, mime, platform).print(parameters)

        if not ok:
            return ResponseInternalError(message)

        return None
