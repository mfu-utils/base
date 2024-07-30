from App.helpers import env
from config import CACHE_PATH

__CONFIG__ = {
    'tmp_file': env('SCAN_TMP_FILE_PATH', f"{CACHE_PATH}/scan"),

    'debug': env('SCAN_DEBUG', False),
}
