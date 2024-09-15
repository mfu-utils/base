import hashlib
from datetime import datetime
from typing import Tuple

from App.Core import Config, MimeTypeConfig, Platform, Filesystem
from App.Core.Abstract import AbstractSubprocess
from App.Core.Logger import Log
from App.Core.Utils import MimeType
from App.Core.Utils.DocumentPagesUtil import DocumentPagesUtil
from App.Core.Utils.OfficeSuite import OfficeSuite
from App.Services.MimeConvertor import MimeConvertor


class PrintingSubprocess(AbstractSubprocess):
    COMMAND = 'lp'

    DEVICE_PRINTING_PARAMETER_PRINTER = "d"
    DEVICE_PRINTING_PARAMETER_COPIES = "n"
    DEVICE_PRINTING_PARAMETER_MEDIA = "media"
    DEVICE_PRINTING_PARAMETER_PAGE_RANGES = "page-ranges"
    DEVICE_PRINTING_PARAMETER_JOB_SHEETS = "job-sheets"
    DEVICE_PRINTING_PARAMETER_OUTPUT_ORDER = "outputorder"
    DEVICE_PRINTING_PARAMETER_MIRROR = "mirror"
    DEVICE_PRINTING_PARAMETER_LANDSCAPE = "landscape"

    _DEVICE_PRINTING_PARAMETER_FILE = "file"
    _DEVICE_PRINTING_PARAMETER_PAPER_SIZE = "paper-size"
    _DEVICE_PRINTING_PARAMETER_PAPER_TRAY = "paper-tray"
    _DEVICE_PRINTING_PARAMETER_TRANSPARENCY = "transparency"
    _DEVICE_PRINTING_PARAMETER_MIME_TYPE = "mime-type"

    DEVICE_DOCUMENT_PARAMETERS = {
        DEVICE_PRINTING_PARAMETER_MEDIA: "media",
        DEVICE_PRINTING_PARAMETER_PRINTER: "device",
        DEVICE_PRINTING_PARAMETER_COPIES: "copies",
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

    def __init__(self, log: Log, _config: Config, mime: MimeTypeConfig, platform: Platform):
        super(PrintingSubprocess, self).__init__(log, _config, self.COMMAND)

        self._mime = mime
        self._platform = platform

        self._convertor = MimeConvertor(self._log, _config, self._mime, self._platform)

        self.set_multi_character_parameters_prefix('-o ')
        self.set_multi_character_parameters_delimiter('=')

        self._convert_tool = _config.get('printing.server_side_convert_tool')

    def __resolve_media_type(self, parameters: dict):
        items = []

        if media := parameters.get(self._DEVICE_PRINTING_PARAMETER_PAPER_SIZE):
            items.append(media)

        if paper_tray := parameters.get(self._DEVICE_PRINTING_PARAMETER_PAPER_TRAY):
            items.append(paper_tray)

        if parameters.get(self._DEVICE_PRINTING_PARAMETER_TRANSPARENCY):
            items.append('Transparency')

        if len(items):
            parameters.update({self.DEVICE_PRINTING_PARAMETER_MEDIA: ','.join(items)})

    def __convert(self, path: str, mime_type: MimeType) -> Tuple[bool, str]:
        suite = OfficeSuite(self._convert_tool)

        path = MimeConvertor(self._log, self._config, self._mime, self._platform).convert_to_pdf(path, mime_type, suite)

        if not path:
            return False, "Failed to convert to pdf"

        return True, path

    def __resolve_file(self, parameters: dict) -> Tuple[bool, str]:
        path = Filesystem.create_tmp_path(hashlib.md5(str(datetime.now()).encode()).hexdigest() + '.pdf')

        content = parameters.get(self._DEVICE_PRINTING_PARAMETER_FILE)

        if not Filesystem.write_file(path, content):
            return False, "Failed to write file"

        mime_type = parameters[self._DEVICE_PRINTING_PARAMETER_MIME_TYPE]

        if not MimeType.is_server_side_convert_type(mime_type):
            return False, path

        return self.__convert(path, MimeType[mime_type])

    def __resolve_page_ranges(self, parameters: dict):
        page_ranges = parameters.get(self.DEVICE_PRINTING_PARAMETER_PAGE_RANGES)

        if (page_ranges is not None) and len(page_ranges):
            parameters.update({self.DEVICE_PRINTING_PARAMETER_PAGE_RANGES: DocumentPagesUtil.cups_pack(page_ranges)})

    def print(self, parameters: dict) -> dict:
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

        ok, res = self.__resolve_file(parameters)

        if not ok:
            return {"result": True, "message": res}

        ok, message = self.run(parameters=cli, options={"additional": res})

        if self._config['debug']:
            return {"result": True, "message": "Debug mode enabled"}

        if not ok:
            self._log.error(message, {"object": self})

        return {"result": ok, "message": message}
