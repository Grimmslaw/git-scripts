import os
import logging
from types import FunctionType
from typing import Tuple

import in_place

from tools.git_ops import get_head_commit
from version_increment.tools.types_ import Version
from version_increment.rust.general_utils import safe_strip, str_is_empty

LOGGER = logging.getLogger(__name__)


def _is_empty_line(line: str) -> bool:
    return line is None or line.strip() == ''


def _parse_version_number(version: str) -> Version:
    major, minor, patch_raw = version.replace('"', '').split('.')
    LOGGER.debug(f'major={major}, minor={minor}, patch_raw={patch_raw}')
    alpha = None
    patch_split = patch_raw.split('-')
    LOGGER.debug(f'patch_split={patch_split}')
    if len(patch_split) == 2 and 'alpha' in patch_raw:
        patch, alpha_raw = patch_split
        alpha = alpha_raw.replace('alpha', '')
        LOGGER.debug(f'patch={patch}, alpha={alpha}')
    else:
        patch = patch_raw
    return Version.instance(safe_strip(major), safe_strip(minor), safe_strip(patch), safe_strip(alpha))


def get_toml_path(dirname: str = None) -> str:
    LOGGER.debug(f'dirpath={dirname}')
    dirpath = dirname if not str_is_empty(dirname) else __file__
    head_commit = get_head_commit(dirpath)
    tree = head_commit.tree
    files = [os.path.join(dirpath, x.path) for x in tree]
    LOGGER.debug(f'files={files}')
    return files[files.index(os.path.join(dirpath, 'Cargo.toml'))]


def parse_toml(toml_path: str) -> Tuple[int, Version]:
    LOGGER.debug(f'toml_path={toml_path}')
    assert os.path.isfile(toml_path), f'Not a file: {toml_path}'
    lineno = -1
    with open(toml_path, 'r') as toml:
        for line in toml:
            lineno += 1
            if not _is_empty_line(line) and line.strip()[0] != '[':
                split_on_equals = [x.strip() for x in line.split('=', 1)]
                if len(split_on_equals) == 2 and split_on_equals[0] == 'version':
                    _, value = split_on_equals
                    version = _parse_version_number(value)
                    LOGGER.debug(f'version={version}')
                    return lineno, version


def write_new_version(new_version: str, toml_path: str):
    with in_place.InPlace(toml_path) as fo:
        for line in fo:
            if line.startswith('version'):
                fo.write(f'version = "{new_version}"\n')
            else:
                fo.write(line)
        fo.write('\n')


def do_bump(bump_func: FunctionType, dirpath: str = None) -> Version:
    LOGGER.debug(f'do_bump: dirpath={dirpath}')
    toml_path = get_toml_path(dirpath)
    LOGGER.debug(f'do_bump: toml_path={toml_path}')
    lineno, old_version = parse_toml(toml_path)

    LOGGER.debug(f'version={old_version}')
    new_version = bump_func(old_version)
    write_new_version(str(new_version), toml_path)

    return new_version
