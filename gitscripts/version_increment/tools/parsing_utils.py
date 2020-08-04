import os
import logging
from typing import Tuple, Callable, Optional

from version_increment.tools.types_ import Version

LOGGER = logging.getLogger(__file__)


def parse_config(config_path: str,
                 filter_func: Callable[[str, Optional[int]], Tuple[int, bool, Version]]) -> Tuple[int, Version]:
    if not os.path.isfile(config_path):
        path = os.path.abspath(config_path)
        if not os.path.isfile(path):
            raise ValueError(f'Could not find a file with the path "{config_path}"')
    else:
        path = config_path

    with open(path, 'r') as fo:
        lineno = -1
        for line in fo:
            lineno, found, version = filter_func(line, lineno)
            if found:
                return lineno, version
        raise RuntimeWarning(f'version number not found in {config_path}')
