from App.Core import Config
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log
from App.Core.Utils.DocumentPagesUtil import DocumentPagesUtil


class PrintingSubprocess(AbstractSubprocess):
    COMMAND = 'lp'

    DEVICE_PRINTING_PARAMETER_PRINTER = "d"
    DEVICE_PRINTING_PARAMETER_NUM_COPIES = "n"
    DEVICE_PRINTING_PARAMETER_MEDIA = "media"
    DEVICE_PRINTING_PARAMETER_PAGE_RANGES = "page-ranges"
    DEVICE_PRINTING_PARAMETER_JOB_SHEETS = "job-sheets"
    DEVICE_PRINTING_PARAMETER_OUTPUT_ORDER = "outputorder"
    DEVICE_PRINTING_PARAMETER_MIRROR = "mirror"
    DEVICE_PRINTING_PARAMETER_LANDSCAPE = "landscape"

    _DEVICE_PRINTING_PARAMETER_MEDIA_OPTIONS = "media-options"
    _DEVICE_PRINTING_PARAMETER_FILE = "file"

    DEVICE_DOCUMENT_PARAMETERS = {
        DEVICE_PRINTING_PARAMETER_PRINTER: "device",
        DEVICE_PRINTING_PARAMETER_NUM_COPIES: "copies",
        DEVICE_PRINTING_PARAMETER_MEDIA: "media",
        DEVICE_PRINTING_PARAMETER_PAGE_RANGES: "pages",
        DEVICE_PRINTING_PARAMETER_JOB_SHEETS: "banner",
        DEVICE_PRINTING_PARAMETER_OUTPUT_ORDER: "order",
        DEVICE_PRINTING_PARAMETER_MIRROR: "mirror",
        DEVICE_PRINTING_PARAMETER_LANDSCAPE: "landscape",
    }

    DEVICE_DOCUMENT_FLAGS = [
        DEVICE_PRINTING_PARAMETER_MIRROR,
        DEVICE_PRINTING_PARAMETER_LANDSCAPE,
    ]

    DEVICE_PRINTING_PARAMETERS_REQUIRED = {
        DEVICE_PRINTING_PARAMETER_PRINTER: 'Device parameter is missing',
    }

    def __init__(self, log: Log, _config: Config):
        super(PrintingSubprocess, self).__init__(log, _config, self.COMMAND)

        self.set_multi_character_parameters_prefix('-o ')
        self.set_multi_character_parameters_delimiter('=')

    def __resolve_media_type(self, parameters: dict):
        media_options = parameters.get(self._DEVICE_PRINTING_PARAMETER_MEDIA_OPTIONS)
        media = parameters.get(self.DEVICE_PRINTING_PARAMETER_MEDIA)

        if not media or not len(media_options):
            return

        parameters.update({self.DEVICE_PRINTING_PARAMETER_MEDIA: ','.join([media, *media_options])})

    def __resolve_file(self, parameters: dict) -> str:
        return parameters.get(self._DEVICE_PRINTING_PARAMETER_FILE)

    def __resolve_page_ranges(self, parameters: dict):
        page_ranges = parameters.get(self.DEVICE_PRINTING_PARAMETER_PAGE_RANGES)

        if len(page_ranges):
            parameters.update({self.DEVICE_PRINTING_PARAMETER_PAGE_RANGES: DocumentPagesUtil.cups_pack(page_ranges)})

    def print(self, parameters: dict):
        cli = {}

        self.__resolve_media_type(parameters)
        self.__resolve_page_ranges(parameters)

        for key, name in self.DEVICE_DOCUMENT_PARAMETERS.items():
            option = parameters.get(name)

            if not option and (key in self.DEVICE_PRINTING_PARAMETERS_REQUIRED):
                self._log.error(self.DEVICE_PRINTING_PARAMETERS_REQUIRED[key], {"object": self})

            if option in self.DEVICE_DOCUMENT_FLAGS:
                cli.update({key: True})
                continue

            cli.update({key: option})

        self.run(parameters=parameters, options={"input": self.__resolve_file(parameters)})
