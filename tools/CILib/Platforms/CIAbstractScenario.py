import os
import subprocess
from abc import ABC, abstractmethod

from tools.CILib.CIBuildType import CIBuildType
from tools.CILib.CIHelpers import copy_with_replace, copy_many, rewrite_target
from tools.CILib.CIPlatform import CIPlatform
from tools.CILib.CIVersionData import CIVersionData


class CIAbstractScenario(ABC):
    def __init__(self, config: dict):
        self._build_type: CIBuildType = config['build_type']
        self._target_path: str = config['target_path']
        self._source_path: str = config['source_path']
        self._machine_name: str = config['machine_name']
        self._config: dict = config['CILib']
        self._test: bool = config['test']

    @abstractmethod
    def _build_type_scenario(self):
        pass

    @abstractmethod
    def _platform(self) -> CIPlatform:
        pass

    @staticmethod
    def _call(*args: str):
        subprocess.run(args)

    def get_version_data(self) -> CIVersionData:
        return CIVersionData(self._config['version'])

    def copy_file(self, filename: str, target_filename: str = None, data: dict = None):
        copy_with_replace(self._source_path, self._target_path, filename, target_filename, data)

    def rewrite_target(self, file: str = None, data: dict = None):
        rewrite_target(self._target_path, file, data)

    def copy_platform_file(self, filename: str, target_filename: str = None, data: dict = None):
        copy_with_replace(
            os.path.join(self._source_path, 'tools', 'build', self._platform().value),
            self._target_path,
            filename,
            target_filename,
            data,
        )

    def copy_platform_many(self, files: list):
        copy_many(
            os.path.join(self._source_path, 'tools', 'build', self._platform().value),
            self._target_path,
            files,
        )

    def build(self):
        if copy_target := self._config['copy']:
            self.copy_platform_many(copy_target)

        self.__create_files()

        if not (scenario := self._build_type_scenario()[self._build_type]):
            raise Exception(
                f'Cannot run build type ({self._build_type.name}) not build fot platform {self._platform().name}.'
            )

        scenario()

        if scenario := self._config.get('commands'):
            self.__run_scenario(scenario)

    def __create_files(self):
        files: dict = self._config.get('files') or {}

        for file_name, content in files.items():
            with open(os.path.join(self._target_path, file_name), 'w') as f:
                f.write('\n'.join(line or "" for line in content))

    def __run_scenario(self, commands: list):
        for command in commands:
            print(command)

            if not self._test:
                self._call(command)
