"""Utilities useful for dealing/reasoning with Rust-specific aspects of the version-increment script."""

import os
import logging
from types import FunctionType
from typing import Tuple

import in_place

from tools.git_ops import get_head_commit
from version_increment.tools.types_ import Version
from version_increment.rust.general_utils import safe_strip, str_is_empty

LOGGER = logging.getLogger(__name__)


def parse_version_number(version: str) -> Version:
    """
    Parse a string representing the version number of the Rust project into a :py:class:`Version` object.

    :param str version:
        a string representing the version number of the Rust project
    :return:
        a Version object representing the project's version number
    """
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


def parse_toml(toml_path: str) -> Tuple[int, Version]:
    """
    Read the Cargo.toml file of the Rust project and seek and produce it's version number.

    :param str toml_path:
        the path to the Rust project's Cargo.toml file, as a string
    :return:
        a tuple containing the line number that the version number is on and the version, itself, as a Version object
    """
    LOGGER.debug(f'toml_path={toml_path}')
    assert os.path.isfile(toml_path), f'Not a file: {toml_path}'
    lineno = -1
    with open(toml_path, 'r') as toml:
        for line in toml:
            lineno += 1
            if not str_is_empty(line) and line.strip()[0] != '[':
                split_on_equals = [x.strip() for x in line.split('=', 1)]
                if len(split_on_equals) == 2 and split_on_equals[0] == 'version':
                    _, value = split_on_equals
                    version = parse_version_number(value)
                    LOGGER.debug(f'version={version}')
                    return lineno, version


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
    _, old_version = parse_toml(toml_path)

    LOGGER.debug(f'version={old_version}')
    new_version = bump_func(old_version)
    write_new_version(str(new_version), toml_path)

    return new_version
