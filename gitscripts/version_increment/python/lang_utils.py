import os
import logging
from types import FunctionType
from typing import Tuple

import in_place

from tools.filesystem import maybe_make_abspath, seek_file, write_new_version
from tools.str_utils import str_is_empty, remove_nonalphanumeric
from version_increment.tools.parsing_utils import parse_config
from version_increment.tools.types_ import Version

LOGGER = logging.getLogger(__file__)


def get_root(directory: str = None):
    if not directory:
        directory = os.getcwd()
    path = maybe_make_abspath(directory)
    if '.git' in os.listdir(path):
        return os.path.join(path, '.git')
    return seek_file('.git', path)


def _list_filter(elem: str) -> bool:
    val = remove_nonalphanumeric(elem, ['.'])
    return not str_is_empty(val)


def config_filter_func(line: str, line_number: int = 0) -> Tuple[int, bool, Version]:
    next_line = line_number + 1
    found = False
    version = None
    if not str_is_empty(line):
        line_split: list = [
            remove_nonalphanumeric(x, ['.'])
            for x in line.split('=')
            if _list_filter(x)
        ]
        if 'version' in line_split:
            version_str_index = line_split.index('version')
            version = Version.from_str(line_split[version_str_index + 1])
            found = True
    return next_line, found, version


def write_func(new_version: str, file_out: in_place.InPlace) -> None:
    file_out.write(f'    version=\'{new_version}\',\n')


def do_bump(bump_func: FunctionType, dirpath: str = None) -> Version:
    LOGGER.debug(f'do_bump: dirpath={dirpath}')
    setup_path = seek_file('setup.py', dirpath)
    LOGGER.debug(f'do_bump: setup_path={setup_path}')

    lineno, old_version = parse_config(setup_path, config_filter_func)
    new_version = bump_func(old_version)
    write_new_version(new_version, lineno, setup_path, write_func=write_func)

    return new_version
