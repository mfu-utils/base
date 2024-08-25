from tools.CILib.CIBuildType import CIBuildType
from tools.CILib.CIPlatform import CIPlatform
from tools.CILib.Platforms.CIAbstractScenario import CIAbstractScenario


class CIWindowsScenario(CIAbstractScenario):
    def _build_type_scenario(self):
        return {
            CIBuildType.CLIENT_UI: self.__client_ui_scenario,
        }

    def _platform(self) -> CIPlatform:
        return CIPlatform.WINDOWS

    def __create_spec(self):
        spec = self._config['spec']
        ffi = self._config['ffi']

        self.copy_platform_file(spec['source'], spec.get('target') or spec['source'], {
            'FFI': ffi.get('target') or ffi['source'],
            'SCRIPT_NAME': spec['build_script'],
            'LOGO': spec['logo'],
            'EXE_NAME': spec['exe_name'],
            'TEST_BOOL': 'True' if self._test else 'False',
        })

    def __create_ffi(self):
        version = self.get_version_data()

        ffi = self._config['ffi']
        company = self._config['company']

        major = str(version.major)
        minor = str(version.minor)
        patch = str(version.patch)
        number = str(version.number)

        str_version = '.'.join([major, minor, patch, number])

        self.copy_platform_file(ffi['source'], ffi.get('target') or ffi['source'], {
            ''
            'V_MAJOR': major,
            'V_MINOR': minor,
            'V_PATCH': patch,
            'V_NUMBER': number,
            'FILE_VERSION': ffi.get('file_version') or str_version,
            'PRODUCT_VERSION': ffi.get('product_version') or str_version,
            'COMPANY_NAME': company['name'],
            'COPYRIGHT': company['copyright'],
            'FILE_DESCRIPTION': ffi['file_description'],
            'INTERNAL_NAME': ffi['internal_name'],
            'ORIGINAL_FILENAME': ffi['original_filename'],
            'PRODUCT_NAME': ffi['product_name'],
        })

    def __client_ui_scenario(self):
        self.__create_ffi()
        self.__create_spec()
