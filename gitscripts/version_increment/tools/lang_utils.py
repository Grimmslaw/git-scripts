import logging
from typing import Callable, Optional, Tuple

from in_place import InPlace

from tools.filesystem import seek_file, write_new_version
from version_increment.tools.parsing import parse_config
from version_increment.tools.types_ import Version

LOGGER = logging.getLogger(__name__)


def do_bump(version_func: Callable[[Version], Version],
            write_func: Callable[[str, InPlace], None],
            config_filter_func: Callable[[str, Optional[int]], Tuple[int, bool, Version]],
            config_name: str, dirpath: str = None):
    LOGGER.debug(f'do_bump: dirpath={dirpath}')
    config_path = seek_file(config_name, dirpath)
    LOGGER.debug(f'do_bump: config_path={config_path}')

    lineno, old_version = parse_config(config_path, config_filter_func)
    new_version = version_func(old_version)
    write_new_version(str(new_version), lineno, config_path, write_func)

    return new_version
