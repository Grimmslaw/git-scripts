from typing import Tuple

import in_place

from tools.str_utils import str_is_empty, remove_nonalphanumeric
from version_increment.tools.types_ import Version

config_name = 'setup.py'


def _list_filter(elem: str) -> bool:
    val = remove_nonalphanumeric(elem, ['.'])
    return not str_is_empty(val)


def write(new_version: str, file_out: in_place.InPlace) -> None:
    file_out.write(f'    version=\'{new_version}\',\n')


def config_filter(line: str, line_number: int = 0) -> Tuple[int, bool, Version]:
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
