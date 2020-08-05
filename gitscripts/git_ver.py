#!/usr/bin/env python3

import argparse
import logging
import os
from importlib import import_module

from tools.filesystem import safe_get_dirpath
from tools.git import do_git_commit
from tools.lang_utils import do_bump
from tools.logging_ import setup as log_init
from tools.str_utils import str_is_empty
from version_increment.tools.types_ import Version

from version_increment.python import python

LOGGER = logging.getLogger(__name__)

PROJECT_TYPES = ['python', 'rust']


def parse_args():
    parser = argparse.ArgumentParser(
        description='A tool for incrementing the version number of a project before committing any changes.'
    )

    parser.add_argument(
        'project', type=str.lower, help='The type of project the target is. Currently only ["python" and "rust" '
                                        'are available]. "list" here will list the project type options.'
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


def main(argv):
    LOGGER.debug(f'argv={argv}')
    to_resolve = argv.dirpath if 'dirpath' in argv and not str_is_empty(argv.dirpath) else os.getcwd()
    dirpath = safe_get_dirpath(to_resolve)
    LOGGER.debug(f'dirpath={dirpath}')

    if argv.project not in PROJECT_TYPES:
        print(f'project with type={argv.project} is not a supported project type')
        print('Quitting...')
        quit()

    project_module = import_module(f'{argv.project}', f'version_increment.{argv.project}')
    write_func = getattr(project_module, 'write_func')
    config_filter_func = getattr(project_module, 'config_filter_func')
    config_name = getattr(project_module, 'config_name')
    version_func = getattr(Version, argv.version)

    new_version = do_bump(version_func, write_func, config_filter_func, config_name)
    do_git_commit(message=f'Version incremented to {new_version}')


if __name__ == '__main__':
    args = parse_args()
    log_init(lvl=getattr(logging, args.level))
    LOGGER.debug(f'Starting {args.project} versioning script')
    main(args)
