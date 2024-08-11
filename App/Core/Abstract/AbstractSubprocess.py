from abc import ABC
from typing import Optional, List, Tuple

from App.Core import Config
from App.Core.Logger import Log
import subprocess


class AbstractSubprocess(ABC):
    def __init__(self, log: Log, config: Config, command: str):
        self._command = command

        self._log = log
        self._config = config.get('subprocesses')

        self._multi_character_parameters_delimiter = ' '
        self._multi_character_parameters_prefix = '--'
        
        self._once_character_parameters_delimiter = ' '
        self._once_character_parameters_prefix = '-'

    def set_multi_character_parameters_delimiter(self, delimiter: str):
        self._multi_character_parameters_delimiter = delimiter

        return self

    def set_multi_character_parameters_prefix(self, prefix: str):
        self._multi_character_parameters_prefix = prefix

        return self

    def set_once_character_parameters_delimiter(self, delimiter: str):
        self._once_character_parameters_delimiter = delimiter

        return self

    def set_once_character_parameters_prefix(self, prefix: str):
        self._once_character_parameters_prefix = prefix

        return self

    def __create_multi_character_parameter_name(self, parameter: str) -> str:
        return f"{self._multi_character_parameters_prefix}{parameter}"

    def __create_once_character_parameter_name(self, parameter: str) -> str:
        return f"{self._once_character_parameters_prefix}{parameter}"

    def __create_multi_character_parameter(self, parameter: str, value: str) -> List[str]:
        parameter = self.__create_multi_character_parameter_name(parameter)

        if type(value) is bool:
            return [parameter] if value else []

        value = str(value)

        if not self._multi_character_parameters_delimiter:
            return [parameter, value]
    
        return [f"{parameter}{self._multi_character_parameters_delimiter}{str(value)}"]

    def __create_once_character_parameter(self, parameter: str, value: str) -> List[str]:
        parameter = self.__create_once_character_parameter_name(parameter)

        if type(value) is bool:
            return [parameter] if value else []

        value = str(value)

        if not self._once_character_parameters_delimiter:
            return [parameter, value]

        return [f"{parameter}{self._once_character_parameters_delimiter}{str(value)}"]

    def _create_parameter(self, name: str, value: str) -> List[str]:
        if len(name) > 1:
            return self.__create_multi_character_parameter(name, value)

        return self.__create_once_character_parameter(name, value)

    def __create_parameters(self, parameters: dict) -> list:
        formated = []

        for key, value in parameters.items():
            list(map(lambda x: formated.append(x), self._create_parameter(key, value)))

        return formated

    def run(self, subcommands: Optional[list] = None, parameters: Optional[dict] = None, options: dict = None) -> Tuple[bool, str]:
        options = options or {}

        if subcommands is None:
            subcommands = []

        if parameters is None:
            parameters = {}

        cmd = ' '.join([self._command, *subcommands, *self.__create_parameters(parameters)])

        self._log.debug(f"Running subprocess: '{cmd}'")

        if self._config['debug']:
            self._log.warning(f'Subprocess debug mode enabled. Command NOT EXECUTED!!!.')

            return False, ""

        result = subprocess.run(
            [self._command, *subcommands, *self.__create_parameters(parameters), *(options.get('additional') or [])],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=options.get('input'),
        )

        data = result.__getattribute__('stderr' if result.returncode > 0 else 'stdout').decode("utf-8").strip()

        if result.returncode > 0:
            self._log.debug('Success', {'object': self})
            return False, data

        self._log.debug(data, {'object': self})
        return True, data
