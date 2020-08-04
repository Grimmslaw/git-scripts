#!/usr/bin/env python3

"""Command-line script that bumps the version of a Python project and adds/commits all files in the index."""

import logging
import os

from tools.filesystem import safe_get_dirpath
from tools.git import do_git_commit
from tools.logging_ import setup as log_init
from tools.setup_utils import parse_args
from tools.str_utils import str_is_empty
from version_increment.python.lang_utils import do_bump
from version_increment.tools.types_ import Version

LOGGER = logging.getLogger(__name__)


def main(argv):
    LOGGER.debug(f'argv={argv}')
    to_resolve = argv.dirpath if 'dirpath' in argv and not str_is_empty(argv.dirpath) else os.getcwd()
    dirpath = safe_get_dirpath(to_resolve)
    LOGGER.debug(f'dirpath={dirpath}')

    version_func = getattr(Version, argv.version)
    new_version = do_bump(version_func, dirpath=dirpath)
    do_git_commit(message=f'Version incremented by git-py to {new_version}', dirpath=dirpath)


if __name__ == '__main__':
    args = parse_args('python')
    log_init(lvl=getattr(logging, args.level))
    LOGGER.debug('Starting python versioning script')
    main(args)
