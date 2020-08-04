#!/usr/bin/env python3

"""Command-line script that bumps the version of a Rust project and adds/commits all files in the index."""

import os
import logging

from tools.filesystem import safe_get_dirpath
from tools.setup_utils import parse_args
from tools.str_utils import str_is_empty
from version_increment.rust.lang_utils import do_bump
from version_increment.tools.types_ import Version
from tools.git import do_git_commit
from tools.logging_ import setup as log_init

LOGGER = logging.getLogger(__name__)


def main(arg):
    LOGGER.debug(f'args={arg}')
    to_resolve = arg.dirpath if 'dirpath' in arg and not str_is_empty(arg.dirpath) else os.getcwd()
    dirpath = safe_get_dirpath(to_resolve)
    LOGGER.debug(f'dirpath={dirpath}')

    version_func = getattr(Version, arg.version)
    new_version = do_bump(version_func, dirpath=dirpath)
    do_git_commit(message=f'Version incremented by git-rust to {new_version}', dirpath=dirpath)


if __name__ == "__main__":
    args = parse_args('rust')
    log_init(lvl=getattr(logging, args.level))
    LOGGER.debug('Starting rust versioning script')
    main(args)
