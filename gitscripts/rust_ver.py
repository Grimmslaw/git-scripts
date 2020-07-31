#!/usr/bin/env python3

import os
import argparse
import logging

from version_increment.rust.general_utils import safe_get_dirpath
from version_increment.rust.rustlang_utils import do_bump
from version_increment.rust.types_ import ARGTYPE_LOOKUP
from tools.git_ops import do_git_commit
from tools.logging_ import setup as log_init

LOGGER = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description='A tool for incrementing the version number of a rust project before committing any changes.'
    )

    parser.add_argument(
        'version', choices=['MAJOR', 'MINOR', 'PATCH', 'ALPHA', 'UNALPHA'], type=str.upper,
        help='Which part of the version should be incremented: ["MAJOR", "MINOR", "PATCH", "ALPHA", "UNALPHA"]. '
             'NOTE: an increment, zeroes out all lower slots, and "UNALPHA" moves to a release version by removing the '
             '"alpha" and its version.'
    )
    parser.add_argument(
        '-C', '--no-commit', action='store_true',  dest='should_not_commit',
        help='Indicates that the script should not commit the changes after updating the version'
    )
    parser.add_argument(
        '-c', '--only-commit', action='store_true', dest='should_only_commit',
        help='Indicates that the version number should not be bumped before committing the changes'
    )
    parser.add_argument(
        '-s', '--separate', action='store_true', dest='separate_commit',
        help='Indicates that the version increment should be a separate commit from the rest of the index'
    )
    parser.add_argument(
        '-d', '--dir', dest='dirpath',
        help='The path to the directory containing the files you would like to commit, '
             'if not the current working directory.'
    )
    parser.add_argument(
        '-m', '--message', type=str, dest='commit_message',
        help='The message to provide with this commit. This is required unless the -C/--no-commit option is provided.'
    )

    return parser.parse_args()


def main(arg):
    LOGGER.info(f'args={arg}')
    version_argtype = ARGTYPE_LOOKUP[arg.version]
    to_resolve = arg.dirpath if 'dirpath' in arg and arg.dirpath is not None else os.getcwd()
    dirpath = safe_get_dirpath(to_resolve)
    LOGGER.debug(f'dirpath={dirpath}')

    # message must be provided in all cases except when there is no commit being made
    assert 'commit_message' in arg or arg.should_not_commit

    if 'should_not_commit' in arg and arg.should_not_commit:
        LOGGER.debug(f'dirpath={dirpath}')
        do_bump(version_argtype, dirpath)
    elif 'should_only_commit' in arg and arg.should_only_commit:
        LOGGER.debug(f'dirpath={dirpath}')
        do_git_commit(message=arg.commit_message, dirpath=dirpath)
    elif 'separate_commit' in arg and arg.separate_commit:
        LOGGER.debug(f'dirpath={dirpath}')
        do_git_commit(message=arg.commit_message, dirpath=dirpath)
        new_version = do_bump(version_argtype, dirpath)
        do_git_commit(message=f'Version incremented to {new_version}', dirpath=dirpath)
    else:
        LOGGER.debug(f'dirpath={dirpath}')
        new_version = do_bump(version_argtype, dirpath=dirpath)
        do_git_commit(message=f'Version incremented to {new_version}', dirpath=dirpath)


if __name__ == "__main__":
    args = parse_args()
    log_init(lvl=logging.DEBUG)
    LOGGER.debug(f'Starting rust versioning script')
    main(args)

