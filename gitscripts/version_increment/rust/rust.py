"""Utilities useful for dealing/reasoning with Rust-specific aspects of the version-increment script."""

import os
import logging
from types import FunctionType
from typing import Tuple

import in_place

from tools.git import get_head_commit
from version_increment.tools.parsing_utils import parse_config
from version_increment.tools.types_ import Version
from tools.str_utils import str_is_empty, remove_nonalphanumeric

LOGGER = logging.getLogger(__name__)


def get_toml_path(dirname: str = None) -> str:
    """
    Retrieve the path to the Rust project's Cargo.toml file.

    :param str dirname:
        [Opt] the name of the directory containing the Rust project's Cargo.toml file, as a string, or nothing to use
        the directory of the current file
    :return:
        the full path to the Cargo.toml file
    """
    LOGGER.debug(f'dirpath={dirname}')
    dirpath = dirname if not str_is_empty(dirname) else __file__
    head_commit = get_head_commit(dirpath)
    tree = head_commit.tree
    files = [os.path.join(dirpath, x.path) for x in tree]
    LOGGER.debug(f'files={files}')
    return files[files.index(os.path.join(dirpath, 'Cargo.toml'))]


def _list_filter(elem: str) -> bool:
    val = remove_nonalphanumeric(elem, ['.'])
    return not str_is_empty(val)


def config_filter_func(line: str, line_number: int = None) -> Tuple[int, bool, Version]:
    next_line = line_number + 1 if line_number else 0
    found = False
    version = None
    if not str_is_empty(line):
        line_split: list = [
            remove_nonalphanumeric(x, ['.'])
            for x in line.split('=')
            if _list_filter(x)
        ]
        if 'version' in line_split:
            found = True
            version_str_index = line_split.index('version')
            version = Version.from_str(line_split[version_str_index + 1])
    return next_line, found, version


def write_new_version(new_version: str, toml_path: str):
    """
    Write the incremented version number of the Rust project to the given path to its Cargo.toml file.

    :param str new_version:
        the project's new, incremented version number
    :param str toml_path:
        the full path to the Rust project's Cargo.toml file, as a string
    """
    with in_place.InPlace(toml_path) as fo:
        for line in fo:
            if line.startswith('version'):
                fo.write(f'version = "{new_version}"\n')
            else:
                fo.write(line)
        fo.write('\n')


def do_bump(bump_func: FunctionType, dirpath: str = None) -> Version:
    """
    Execute all of the inner functions to find a rust project's Cargo.toml, read and parse its version number,
    increment it, and write the new version to the same file.

    :param FunctionType bump_func:
        the function to be applied to the old version number in order to write the new version number to the
        Cargo.toml file
    :param str dirpath:
        [Opt] the full path to the directory that Cargo.toml file should be found in, or nothing if it
        should be inferred
    :return:
        a `Version` object representing the incremented version number
    """
    LOGGER.debug(f'do_bump: dirpath={dirpath}')
    toml_path = get_toml_path(dirpath)
    LOGGER.debug(f'do_bump: toml_path={toml_path}')

    lineno, old_version = parse_config(toml_path, config_filter_func)
    LOGGER.debug(f'version={old_version}')
    new_version = bump_func(old_version)
    write_new_version(str(new_version), toml_path)

    return new_version
