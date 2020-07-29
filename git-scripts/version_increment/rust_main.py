#!/usr/bin/env python3

import argparse

import sys
for path in sys.path:
    print(path)

from version_increment.rust.rustlang_utils import do_bump
from version_increment.rust.types_ import ARGTYPE_LOOKUP
from tools.git_ops import do_git_commit


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
        '-m', '--message', type=str, dest='commit_message',
        help='The message to provide with this commit. This is required unless the -C/--no-commit option is provided.'
    )

    return parser.parse_args()


def main(arg):
    version_argtype = ARGTYPE_LOOKUP[arg.version]

    # message must be provided in all cases except when there is no commit being made
    assert 'commit_message' in arg or arg.should_not_commit

    if arg.should_not_commit:
        do_bump(version_argtype)
    elif arg.should_only_commit:
        do_git_commit(message=arg.commit_message)
    elif arg.separate_commit:
        do_git_commit(message=arg.commit_message)
        new_version = do_bump(version_argtype)
        do_git_commit(message=f'Version incremented to {new_version}')
    else:
        new_version = do_bump(version_argtype)
        do_git_commit(message=f'Version incremented to {new_version}')


if __name__ == "__main__":
    args = parse_args()
    main(args)

