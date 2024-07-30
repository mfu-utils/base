class CIVersionData:
    def __init__(self, version_parameters: dict):
        self.__major: int = version_parameters['major']
        self.__minor: int = version_parameters['minor']
        self.__patch: int = version_parameters['patch']
        self.__number: int = version_parameters['number']
        self.__branch: str = version_parameters['branch']
        self.__show: str = version_parameters['show']
        self.__build_date: str = version_parameters['build_date']

    @property
    def major(self) -> int:
        return self.__major

    @property
    def minor(self) -> int:
        return self.__minor

    @property
    def patch(self) -> int:
        return self.__patch

    @property
    def number(self) -> int:
        return self.__number

    @property
    def branch(self) -> str:
        return self.__branch

    @property
    def show(self) -> str:
        return self.__show

    @property
    def build_date(self) -> str:
        return self.__build_date
