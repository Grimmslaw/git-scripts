import os
import logging
from typing import Tuple

import in_place

from tools.git_ops import get_head_commit
from version_increment.rust.general_utils import safe_strip
from version_increment.rust.types_ import Version, ArgTypes

LOGGER = logging.getLogger(__name__)


def _is_empty_line(line: str) -> bool:
    return line is None or line.strip() == ''


def _parse_version_number(version: str) -> Version:
    major, minor, patch_raw = version.replace('"', '').split('.')
    LOGGER.debug(f'major={major}, minor={minor}, patch_raw={patch_raw}')
    alpha = ''
    patch_split = patch_raw.split('-')
    LOGGER.debug(f'patch_split={patch_split}')
    if len(patch_split) == 1 and 'alpha' in patch_raw:
        patch, alpha = patch_split
        LOGGER.debug(f'patch={patch}, alpha={alpha}')
    else:
        patch = patch_raw
    return Version(safe_strip(major), safe_strip(minor), safe_strip(patch), safe_strip(alpha))


def get_toml_path(dirpath: str = None) -> str:
    LOGGER.debug(f'dirpath={dirpath}')
    head_commit = get_head_commit(dirpath) if dirpath is not None else get_head_commit(__file__)
    tree = head_commit.tree
    files = [x.path for x in tree]
    return os.path.abspath(files[files.index('Cargo.toml')])


def parse_toml(toml_path: str) -> Tuple[int, Version]:
    LOGGER.debug(f'toml_path={toml_path}')
    assert os.path.isfile(toml_path)
    lineno = -1
    with open(toml_path, 'r') as toml:
        for line in toml:
            lineno += 1
            if not _is_empty_line(line) and line.strip()[0] != '[':
                split_on_equals = [x.strip() for x in line.split('=', 1)]
                if len(split_on_equals) == 2 and split_on_equals[0] == 'version':
                    _, value = split_on_equals
                    version = _parse_version_number(value)
                    return lineno, version


def write_new_version(new_version: str, toml_path: str):
    with in_place.InPlace(toml_path) as fo:
        for line in fo:
            if line.startswith('version'):
                fo.write(f'version = "{new_version}"\n')
            else:
                fo.write(line)
        fo.write('\n')


def do_bump(bump_type: ArgTypes, dirpath: str = None) -> Version:
    LOGGER.debug(f'dirpath={dirpath}')
    toml_path = get_toml_path(dirpath)
    lineno, version = parse_toml(toml_path)
    LOGGER.debug(f'version={version}')
    version.incr_from_argtype(bump_type)
    write_new_version(str(version), toml_path)
    return version
