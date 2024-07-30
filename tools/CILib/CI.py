import os

from tools.CILib.CIBuildType import CIBuildType
from tools.CILib.CIPlatform import CIPlatform
from tools.CILib.Platforms import CIMacOSScenario
from tools.CILib.Platforms.CILinuxScenario import CILinuxScenario
from tools.CILib.Platforms.CIWindowsScenario import CIWindowsScenario

PLATFORM_SCENARIO = {
    CIPlatform.WINDOWS: CIWindowsScenario,
    CIPlatform.LINUX: CILinuxScenario,
    CIPlatform.MACOS: CIMacOSScenario,
}


class CI:
    def __init__(self, config: dict):
        config['platform_name'] = CIPlatform(config['platform_name'])
        config['build_type'] = CIBuildType(config['build_type'])

        self.__test: bool = config['test']

        self._build_type: CIBuildType = config['build_type']
        self._platform: CIPlatform = config['platform_name']

        self._target_path: str = config['target_path']
        self._source_path: str = config['source_path']
        self._machine_name: str = config['machine_name']
        self._config: dict = config['CILib']
        self._scenario = PLATFORM_SCENARIO[self._platform](config)

    def __create_config_py(self):
        version = self._scenario.get_version_data()

        os.makedirs(os.path.join(self._target_path, 'var', 'db'), exist_ok=True)

        self._scenario.rewrite_target('config.py', data={
            'APP_NAME': self._config['app_name'],
            'V_MAJOR': str(version.major),
            'V_MINOR': str(version.minor),
            'V_PATH': str(version.patch),
            'V_NUMBER': str(version.number),
            'V_SHOW': version.show,
            'V_BRANCH': version.branch,
            'V_BUILD_DATE': version.build_date,

            'LICENSE_NAME': self._config['license_name'],
            'LICENSE_URL': self._config['license_url'],
            'REPO_NAME': self._config['repo_name'],
            'REPO_URL': self._config['repo_url'],
        })

    def create_update_scenario(self):
        pass

    def build(self):
        self.__create_config_py()

        self._scenario.build()
