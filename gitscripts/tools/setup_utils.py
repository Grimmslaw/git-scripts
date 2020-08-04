import argparse


def parse_args(project_type: str):
    parser = argparse.ArgumentParser(
        description=f'A tool for incrementing the version number of a {project_type} '
                    f'project before committing any changes.'
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
