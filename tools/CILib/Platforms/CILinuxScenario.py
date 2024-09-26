from tools.CILib.CIBuildType import CIBuildType
from tools.CILib.CIPlatform import CIPlatform
from tools.CILib.Platforms.CIAbstractScenario import CIAbstractScenario


class CILinuxScenario(CIAbstractScenario):
    def _build_type_scenario(self):
        return {
            CIBuildType.SERVER: self.__build_server,
        }

    def _platform(self) -> CIPlatform:
        return CIPlatform.LINUX

    def __build_server(self):
        pass
