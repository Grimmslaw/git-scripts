import logging
from types import FunctionType
from typing import Callable, Optional, Tuple

import in_place

from tools.filesystem import seek_file, write_new_version
from version_increment.tools.parsing_utils import parse_config
from version_increment.tools.types_ import Version

LOGGER = logging.getLogger(__name__)


def do_bump(bump_func: FunctionType, write_func: Callable[[str, in_place.InPlace], None],
            config_filter_func: Callable[[str, Optional[int]], Tuple[int, bool, Version]],
            config_name: str, dirpath: str = None) -> Version:
    LOGGER.debug(f'do_bump: dirpath={dirpath}')
    config_path = seek_file(config_name, dirpath)
    LOGGER.debug(f'do_bump: config_path={config_path}')

    lineno, old_version = parse_config(config_path, config_filter_func)
    new_version = bump_func(old_version)
    write_new_version(new_version, lineno, config_path, write_func=write_func)

    return new_version
