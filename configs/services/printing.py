import os

from App.helpers import env
from config import CACHE_PATH

__CONFIG__ = {
    "tmp_dir_path": env("PRINTING_TMP_DIR_PATH", os.path.join(CACHE_PATH, "printing")),
}
