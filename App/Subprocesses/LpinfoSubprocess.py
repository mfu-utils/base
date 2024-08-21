import re
from typing import List

from App.Core import Config
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log


class LpinfoSubprocess(AbstractSubprocess):
    REGEX_DEVICES = re.compile('direct ([^\n]+)')

    def __init__(self, log: Log, config: Config):
        super(LpinfoSubprocess, self).__init__(log, config, "lpinfo")

    def get_direct_devices(self) -> List[str]:
        ok, out = self.run(parameters={"v": True})

        if not ok:
            self._log.error(f"Failed to get devices info. {out}", {"object": self})
            return []

        return self.REGEX_DEVICES.findall(out)
