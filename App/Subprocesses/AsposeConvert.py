import os

from App.Core import Config, Platform
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log
from config import CWD


class AsposeConvert(AbstractSubprocess):
    def __init__(self, log: Log, config: Config, platform: Platform):
        self.__platform = platform

        super(AsposeConvert, self).__init__(log, config, os.path.join(CWD, 'aspose_convert'), False)

    def convert(self, path_from: str, path_to) -> bool:
        ok, out = self.run([path_from, path_to])

        if (not ok) or (not os.path.exists(path_to)):
            self._log.error(f"Aspose failed to convert. {out}", {"object": self})
            return False

        return True
