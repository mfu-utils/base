import subprocess
from typing import List

from App.helpers import config, logger


class OCR:
    image_path_replace = "$p"
    out_file_path_replace = "$o"
    languages_replace = "$l"

    @staticmethod
    def convert(executed: str, template: str, path: str, out: str, langs_sep: str, langs: List[str]) -> int:
        langs = langs_sep.join(langs)

        cmd = " ".join([
            f'"{executed}"',
            template
            .replace(OCR.image_path_replace, path)
            .replace(OCR.out_file_path_replace, out)
            .replace(OCR.languages_replace, langs),
        ]).replace('\\', '\\\\')

        if config('convertor.debug_command'):
            logger().debug(f"Execute convertor: `{cmd}`", {'object': OCR})
            return 0

        return subprocess.call(cmd)
