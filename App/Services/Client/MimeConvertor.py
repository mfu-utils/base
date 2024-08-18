import hashlib
import os
import tempfile

import img2pdf
import docx2pdf

from App.Core import Filesystem
from App.helpers import config, mime
from PIL import Image as PILImage


class MimeConvertor:
    def __init__(self):
        self.__tmp_path = tempfile.gettempdir()
        self.__mime_config: dict = config('mime')
        self.__doc_mime_types = self.__mime_config["doc_mime_types"]
        self.__images_mime_types = self.__mime_config["images_mime_types"]

    def __get_unique_filename(self, path: str, extension: str) -> str:
        _hash = str(hashlib.md5((f := open(path, 'rb')).read()).hexdigest())
        f.close()

        return os.path.join(self.__tmp_path, _hash + f".{extension}")

    def __get_converted_image_to_pdf(self, file: str) -> str:
        if not os.path.exists(path := self.__get_unique_filename(file, "pdf")):
            data = img2pdf.convert(img := PILImage.open(file).filename)
            img.close()
            Filesystem.write_file(path, data)

        return path

    def __get_converted_doc(self, path_from: str, to: str) -> str:
        if not os.path.exists(path_to := self.__get_unique_filename(path_from, to)):
            docx2pdf.convert(path_from, path_to)

        return path_to

    def convert_to_pdf(self, path: str, mime_type: str) -> str:
        if mime_type in self.__doc_mime_types:
            return self.__get_converted_doc(path, 'pdf')

        if mime_type in self.__images_mime_types:
            return self.__get_converted_image_to_pdf(path)

    def get_pdf(self, path: str) -> str:
        mime_type = mime().get_mime(path)

        if mime_type == 'application/pdf':
            return path

        return self.convert_to_pdf(path, mime_type)
