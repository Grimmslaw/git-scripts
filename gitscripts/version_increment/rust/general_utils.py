import os, logging

LOGGER = logging.getLogger(__name__)


def _resolve_path_symbols(path: str) -> str:
    if path is None or path == '':
        LOGGER.error('Empty string passed in as a path')
        return ''
    to_resolve = path if '~' not in path else os.path.expanduser(path)
    return os.path.abspath(to_resolve)


def safe_get_dirpath(dirname: str) -> str:
    resolved = _resolve_path_symbols(dirname)
    LOGGER.debug(f'resolved file: {resolved}')
    if resolved != '' and os.path.isdir(resolved):
        return resolved
    LOGGER.error(f'Could not resolve directory named {dirname}; returning dirname')
    return dirname


def safe_strip(str_to_be_stripped: str, chars_to_strip: str = None):
    if str_to_be_stripped is None:
        return str_to_be_stripped
    if chars_to_strip is None:
        return str_to_be_stripped.strip()
    return str_to_be_stripped.strip(chars_to_strip)


def safe_str_to_int(target: str, default: int = None) -> int or None:
    if target is not None and target != '' and target.isnumeric():
        return int(target)
    if default is not None:
        return default
    return None


def str_is_empty(some_str: str) -> bool:
    return some_str is None or some_str.strip() == ''
