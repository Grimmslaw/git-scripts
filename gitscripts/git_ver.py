#!/usr/bin/env python3

import logging
import os
from importlib import import_module

from tools.filesystem import safe_get_dirpath
from tools.git import do_git_commit
from tools.logging_ import setup as init_log
from tools.setup_ import parse_args
from tools.str_utils import str_is_empty
from version_increment.tools.lang_utils import do_bump
from version_increment.tools.types_ import Version

LOGGER = logging.getLogger(__name__)

PROJECT_TYPES = ['python', 'rust']


def main(argv):
    LOGGER.debug(f'argv={argv}')
    to_resolve = argv.dirpath if 'dirpath' in argv and not str_is_empty(argv.dirpath) else os.getcwd()
    dirpath = safe_get_dirpath(to_resolve)
    LOGGER.debug(f'dirpath={dirpath}')

    if argv.project not in PROJECT_TYPES:
        print(f'project with type={argv.project} is not a supported project type')
        print('Quitting...')
        quit()

    project_module = import_module(f'.{argv.project}', f'version_increment.{argv.project}')
    write_func = getattr(project_module, 'write')
    config_filter_func = getattr(project_module, 'config_filter')
    config_name = getattr(project_module, 'config_name')
    version_func = getattr(Version, argv.version)

    new_version = do_bump(version_func, write_func, config_filter_func, config_name, dirpath)
    do_git_commit(f'Version incremented to {new_version}', dirpath)


if __name__ == '__main__':
    args = parse_args()
    init_log(lvl=getattr(logging, args.level))
    LOGGER.debug(f'Starting {args.project} versioning script')
    main(args)
