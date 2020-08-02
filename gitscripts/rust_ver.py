#!/usr/bin/env python3

"""Command-line script that bumps the version of a Rust project and adds/commits all files in the index."""

import os
import argparse
import logging

from version_increment.rust.general_utils import safe_get_dirpath, str_is_empty
from version_increment.rust.rustlang_utils import do_bump
from version_increment.tools.types_ import Version
from tools.git_ops import do_git_commit
from tools.logging_ import setup as log_init

LOGGER = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description='A tool for incrementing the version number of a rust project before committing any changes.'
    )

    parser.add_argument(
        'version', choices=['major', 'minor', 'patch', 'subpatch', 'alpha', 'unalpha'], type=str.lower,
        help='Which part of the version should be incremented: '
             '["major", "minor", "patch", "subpatch", "alpha", "unalpha"]. '
             'NOTE: an increment, zeroes out all lower slots, and "unalpha" moves to a release version by removing the '
             '"alpha" and its version.'
    )
    parser.add_argument(
        '-d', '--dir', dest='dirpath',
        help='The path to the directory containing the files you would like to commit, '
             'if not the current working directory.'
    )
    parser.add_argument(
        '-l', '--log-level', type=str.upper, choices=['CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'NOTSET'],
        dest='level', default='INFO',
        help='The lowest level of log statements to log; default is INFO. [CRITICAL, ERROR, WARN, INFO, DEBUG, NOTSET]'
    )

    return parser.parse_args()


def main(arg):
    LOGGER.debug(f'args={arg}')
    to_resolve = arg.dirpath if 'dirpath' in arg and not str_is_empty(arg.dirpath) else os.getcwd()
    dirpath = safe_get_dirpath(to_resolve)
    LOGGER.debug(f'dirpath={dirpath}')

    version_func = getattr(Version, arg.version)
    new_version = do_bump(version_func, dirpath=dirpath)
    do_git_commit(message=f'Version incremented by git-rust to {new_version}', dirpath=dirpath)


if __name__ == "__main__":
    args = parse_args()
    log_init(lvl=getattr(logging, args.level))
    LOGGER.debug('Starting rust versioning script')
    main(args)
