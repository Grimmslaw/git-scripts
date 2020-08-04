"""Utilities for safely dealing with strings, especially those that may or may not be `None` or empty."""

import re
from typing import List


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


def remove_nonalphanumeric(some_str: str, exclusions: List[str] = None) -> str:
    excl_str = ''.join(exclusions) if exclusions and len(exclusions) > 0 else ''
    return re.sub(fr'[^\w1-9{excl_str}]+', '', some_str)
