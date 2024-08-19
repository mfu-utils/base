import hashlib
import os
import tempfile
from enum import Enum
from typing import List, Optional

import img2pdf
import docx2pdf

from App.Core import Filesystem, Config, MimeType, Platform
from App.Core.Logger import Log
from App.Subprocesses import LibreofficePdfConvert

from App.Subprocesses.AsposeConvert import AsposeConvert


class MimeConvertor:
    class OfficeSuit(Enum):
        NONE = "none"
        MSWORD = "msword"
        LIBREOFFICE = "libreoffice"
        ASPOSE_LIBRAY = "aspose_lib"

    OFFICE_SUIT_NAMES = {
        OfficeSuit.MSWORD.value: "Microsoft Word",
        OfficeSuit.LIBREOFFICE.value: "Libreoffice",
        OfficeSuit.ASPOSE_LIBRAY.value: "Aspose (Restricted)"
    }

    def __init__(self, log: Log, _config: Config, mime: MimeType, platform: Platform):
        self.__mime_type = mime

        self.__libreoffice_convertor = LibreofficePdfConvert(log, _config, platform)
        self.__aspose_convertor = AsposeConvert(log, _config, platform)

        self.__tmp_path = tempfile.gettempdir()
        self.__mime_config: dict = _config.get('mime')
        self.__doc_mime_types = self.__mime_config["doc_mime_types"]
        self.__images_mime_types = self.__mime_config["images_mime_types"]

        self.__debug = _config.get("printing.debug")
        self.__check_previous = _config.get("printing.check_previous")

    @staticmethod
    def suits(none: bool = True) -> List[OfficeSuit]:
        suits = [MimeConvertor.OfficeSuit.NONE] if none else []

        suits += [
            MimeConvertor.OfficeSuit.LIBREOFFICE,
            MimeConvertor.OfficeSuit.ASPOSE_LIBRAY,
        ]

        if not Platform.system_is(Platform.LINUX):
            suits.append(MimeConvertor.OfficeSuit.MSWORD)

        return suits

    @staticmethod
    def suits_values(none: bool = True) -> List[str]:
        return list(map(lambda x: x.value, MimeConvertor.suits(none)))

    @staticmethod
    def __get_unique_filename(path: str) -> str:
        _hash = str(hashlib.md5((f := open(path, 'rb')).read()).hexdigest())
        f.close()

        return _hash

    def __get_unique_filepath(self, path_from: str, extension: str) -> str:
        filename = self.__get_unique_filename(path_from)
        return os.path.join(self.__tmp_path, filename + f".{extension}")

    def __exists_path(self, path: str) -> bool:
        if not self.__check_previous:
            return False

        return os.path.exists(path)

    def __get_converted_image_to_pdf(self, path_from: str) -> str:
        path_to = self.__get_unique_filepath(path_from, "pdf")

        if not self.__exists_path(path_to):
            Filesystem.write_file(path_to, img2pdf.convert(path_from))

        return path_to

    def __get_converted_doc_by_aspose(self, path_from: str, extension: str) -> str:
        path_to = self.__get_unique_filepath(path_from, extension)

        if not self.__exists_path(path_to):
            self.__aspose_convertor.convert(path_from, path_to)

        return path_to

    def __get_converted_doc_by_libreoffice(self, path_from: str, extension: str) -> str:
        path_to = os.path.join(self.__tmp_path, path_from.split('/')[-1].split('.')[0] + f".{extension}")

        if not self.__exists_path(path_to):
            self.__libreoffice_convertor.docx_convert(path_from, self.__tmp_path, extension)

        return path_to

    def __get_converted_doc_by_msword(self, path_from: str, extension: str) -> str:
        path_to = self.__get_unique_filepath(path_from, extension)

        if not self.__exists_path(path_to):
            docx2pdf.convert(path_from, path_to)

        return path_to

    def __get_converted_doc(self, path_from: str, extension: str, suit: OfficeSuit) -> Optional[str]:
        if suit == MimeConvertor.OfficeSuit.ASPOSE_LIBRAY:
            return self.__get_converted_doc_by_aspose(path_from, extension)

        if suit == MimeConvertor.OfficeSuit.MSWORD:
            return self.__get_converted_doc_by_msword(path_from, extension)

        if suit == MimeConvertor.OfficeSuit.LIBREOFFICE:
            return self.__get_converted_doc_by_libreoffice(path_from, extension)

        return None

    def convert_to_pdf(self, path: str, mime_type: str, suit: OfficeSuit) -> Optional[str]:
        if mime_type in self.__doc_mime_types:
            return self.__get_converted_doc(path, 'pdf', suit)

        if mime_type in self.__images_mime_types:
            return self.__get_converted_image_to_pdf(path)

    def get_pdf(self, path: str, suit: OfficeSuit = OfficeSuit.NONE) -> Optional[str]:
        mime_type = self.__mime_type.get_mime(path)

        if mime_type == 'application/pdf':
            return path

        return self.convert_to_pdf(path, mime_type, suit)
