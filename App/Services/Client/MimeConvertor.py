import hashlib
import os
import tempfile
from datetime import datetime

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

    @staticmethod
    def __get_unique_filename(extension: str) -> str:
        seed = str(datetime.now().timestamp()).replace('.', '')

        return hashlib.md5(seed.encode()).hexdigest() + f".{extension}"

    def __get_converted_image_to_pdf(self, file: str) -> str:
        data = img2pdf.convert(img := PILImage.open(file).filename)
        img.close()

        path = self.__get_unique_filename("pdf")

        Filesystem.write_file(path, data)

        return path

    def __get_converted_doc(self, path_from: str, to: str) -> str:
        path_to = os.path.join(self.__tmp_path, self.__get_unique_filename(to))

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
