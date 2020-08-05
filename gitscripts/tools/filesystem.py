"""Utilities useful for finding, resolving, and handling paths and files in the current filesystem."""

import os
import logging
from typing import Callable

import in_place

from tools.str_utils import str_is_empty

LOGGER = logging.getLogger(__file__)


def resolve_path_symbols(path: str) -> str:
    """
    Safely resolve the given path by expanding the user symbol ('~') and building the absolute path.

    :param str path:
        the (possibly-relative) path to be resolved
    :return:
        an absolute path from the given path, or an empty string if given path is None or empty
    """
    if path is None or path == '':
        LOGGER.error('Empty string passed in as a path')
        return ''
    to_resolve = path if '~' not in path else os.path.expanduser(path)
    return os.path.abspath(to_resolve)


def safe_get_dirpath(dirname: str) -> str:
    """
    Safely get the path to the directory with the given name.

    :param str dirname:
        the directory to resolve the path for
    :return:
        the absolute path to the given directory
    """
    resolved = resolve_path_symbols(dirname)
    LOGGER.debug(f'resolved file: {resolved}')
    if resolved != '' and os.path.isdir(resolved):
        return resolved
    LOGGER.error(f'Could not resolve directory named {dirname}; returning dirname')
    return dirname


def maybe_make_abspath(maybe_path: str, file=False) -> str:
    if str_is_empty(maybe_path):
        raise ValueError('Given path was None or an empty string.')

    check_func = os.path.isfile if file else os.path.isdir
    if check_func(maybe_path):
        return maybe_path

    abspathed = os.path.abspath(maybe_path)
    if check_func(abspathed):
        return abspathed

    raise ValueError(f'No file could be found with the path "{maybe_path}"')


def _seek_to_depth(filename: str, dirpath: str, maxdepth: int) -> str or None:
    for root, dirs, files in os.walk(dirpath):
        if filename in files:
            return os.path.join(root, filename)
        if root.count(os.sep) >= maxdepth:
            return None
    LOGGER.debug(f'filename={filename} not found in dirpath={dirpath} within (total) depth={maxdepth}')
    return None


def _seek_all(filename: str, dirpath: str) -> str or None:
    for root, dirs, files in os.walk(dirpath):
        if filename in files:
            return os.path.join(root, filename)
    LOGGER.debug(f'filename={filename} not found in dirpath={dirpath}')
    return None


def seek_file(filename: str, start_dir: str, maxdepth: int = None) -> str:
    dirpath = maybe_make_abspath(start_dir)
    if maxdepth:
        depth = dirpath.count(os.sep) + maxdepth
        return _seek_to_depth(filename, dirpath, depth)
    return _seek_all(filename, dirpath)


def write_new_version(new_version: str, lineno: int, cfg_path: str,
                      write_func: Callable[[str, in_place.InPlace], None]) -> None:
    with in_place.InPlace(cfg_path) as fo:
        count = -1
        for line in fo:
            count += 1
            if count == lineno:
                write_func(new_version, fo)
            else:
                fo.write(line)
        # fo.write('\n')
