import os
import subprocess
from typing import Union, List

REPLACE_SYMBOL = '@'


def read_file(path: str) -> bytes:
    if not os.path.exists(path):
        raise Exception(f'File ({path}) not found')

    if not os.path.isfile(path):
        raise Exception(f'{path} - is not a file')

    with open(path, 'rb') as f:
        return f.read()


def write_file(path: str, content: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb') as f:
        f.write(content)


def replace(content: str, data: dict):
    for key, value in data.items():
        content = content.replace(f"{REPLACE_SYMBOL}{key}{REPLACE_SYMBOL}", str(value))

    return content


def call(cmd: Union[List[str], str]):
    if isinstance(cmd, list):
        cmd = ' '.join(cmd)

    subprocess.run(cmd)


def rewrite_target(target_path: str, file: str = None, data: dict = None):
    path = os.path.join(target_path, file)

    content = read_file(path)

    if data:
        content = replace(content.decode(), data).encode('utf-8')

    write_file(path, content)


def copy_with_replace(source_path: str, target_path: str, file: str, target_file: str = None, data: dict = None):
    source_path = os.path.join(source_path, file)
    target_path = os.path.join(target_path, target_file or file)

    content = read_file(source_path)

    if data:
        content = replace(content.decode(), data).encode('utf-8')

    write_file(target_path, content)


def copy_many(source_path: str, target_path: str, files: list):
    for file in files:
        source_name = target_name = file

        if isinstance(file, list):
            source_name, target_name = file

        os.makedirs(os.path.dirname(os.path.join(target_path, target_name)), exist_ok=True)

        write_file(os.path.join(target_path, target_name), read_file(os.path.join(source_path, source_name)))
