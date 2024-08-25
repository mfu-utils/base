import os
from typing import List, Tuple
import re

from App.Core import Config, Filesystem
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log
from config import CWD


class LpstatSubprocess(AbstractSubprocess):
    REGEX_DEVICES = re.compile(r"[^:]+ ([^:]+): ([^\n]+)")

    def __init__(self, log: Log, config: Config):
        super(LpstatSubprocess, self).__init__(log, config, "lpstat")

    def get_printers_list(self) -> Tuple[bool, List[str]]:
        ok, out = self.run(parameters={"v": True})

        if self._config['debug']:
            return True, Filesystem.read_json(os.path.join(CWD, "tests", "dictionaries", "devices.json"))

        if not ok:
            self._log.error(f"Cannot get list of printers. {out}", {"object": self})
            return False, []

        return True, self.REGEX_DEVICES.findall(out)
