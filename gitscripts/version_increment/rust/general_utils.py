"""General utility functions useful for Rust version incrementing scripts."""

import os
import logging

LOGGER = logging.getLogger(__name__)


def _resolve_path_symbols(path: str) -> str:
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
    resolved = _resolve_path_symbols(dirname)
    LOGGER.debug(f'resolved file: {resolved}')
    if resolved != '' and os.path.isdir(resolved):
        return resolved
    LOGGER.error(f'Could not resolve directory named {dirname}; returning dirname')
    return dirname


def safe_strip(str_to_be_stripped: str, chars_to_strip: str = None):
    """
    Strip the given string of the given characters, handling None-values safely.

    :param str str_to_be_stripped:
        the string to strip the given characters of
    :param str chars_to_strip:
        [Opt] the characters to strip from either side of the given string, or `None` to only strip whitespaces
    :return:
        the resulting stripped string or None if the original string was None
    """
    if str_to_be_stripped is None:
        return str_to_be_stripped
    if chars_to_strip is None:
        return str_to_be_stripped.strip()
    return str_to_be_stripped.strip(chars_to_strip)


def safe_str_to_int(target: str, default: int = None) -> int or None:
    """
    Convert the given string to an int, safely handling None-values with either a default int
    or None, itself.

    :param str target:
        the string to be converted into an int
    :param int default:
        [Opt] the value to return if an error occurs, or nothing to use `None` as the default
    :return:
        and int representing the given str or the default int, or None
    """
    if target is not None and target != '' and target.isnumeric():
        return int(target)
    if default is not None:
        return default
    return None


def str_is_empty(some_str: str) -> bool:
    """
    Determine whether the given string is None or an empty string.

    :param str some_str:
        the string to check
    :return:
        `True` if the string is None or an empty string, `False` otherwise
    """
    return some_str is None or some_str.strip() == ''
