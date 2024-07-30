import os
from typing import Dict

from App.Core import Filesystem
from App.helpers import platform
from config import ROOT
from tools.build import static, filtering_files


def copy_with_mkdirs(_from: str, _to: str):
    os.makedirs(os.path.dirname(_to), exist_ok=True)

    Filesystem.copy(_from, _to)


def get_disabled_before_build_items(build_type: str) -> Dict:
    items = static.DISABLED_BUILD_ITEMS['_'].copy()

    items.update(static.DISABLED_BUILD_ITEMS['build-types'][build_type])
    items.update(static.DISABLED_BUILD_ITEMS['platforms'][platform().name])

    return items


def create_files_struct_recursive(build_type: str, path: str = ROOT, struct: dict = None) -> Dict:
    _dir = os.listdir(path)
    struct = struct or {}

    disabled = get_disabled_before_build_items(build_type)

    for item in _dir:
        item_path = os.path.join(path, item)

        if item in disabled:
            sr = disabled[item]

            if sr == "*":
                continue

            if isinstance(sr, str):
                sr = [sr]

            if path in sr:
                continue

        uri = item_path.split(os.path.join(ROOT, ""))[1]

        if os.path.isdir(item_path):
            create_files_struct_recursive(build_type, item_path, struct)
            continue

        struct.update({item_path: uri})

    return struct


def copy_struct_to(build_type: str, struct: dict, path: str):
    for _from, uri in struct.items():
        _to = os.path.join(path, uri)
        uri: str

        if not Filesystem.exists(_dir := os.path.dirname(_to)):
            os.makedirs(_dir, exist_ok=True)

        if uri.split('.')[-1] in static.FILTERED_FILES_EXT:
            with open(_to, 'w') as f:
                f.write(filtering_files.load_filtered(build_type, _from))

            continue

        Filesystem.copy(_from, _to)
