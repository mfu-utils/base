from tools.CILib.CIPlatform import CIPlatform
from tools.CILib.Platforms.CIAbstractScenario import CIAbstractScenario


class CILinuxScenario(CIAbstractScenario):
    def _build_type_scenario(self):
        return {}

    def _platform(self) -> CIPlatform:
        return CIPlatform.MACOS
