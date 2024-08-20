from typing import List

from App.Core import Config
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log


class LPInfoSubprocess(AbstractSubprocess):
    def __init__(self, log: Log, config: Config):
        super(LPInfoSubprocess, self).__init__(log, config, "lpinfo")

    def get_printers_list(self) -> List[str]:
        ok, out = self.run(parameters={"v": True})

        if not ok:
            self._log.error(f"Cannot get list of printers. {out}")

        return [out]
