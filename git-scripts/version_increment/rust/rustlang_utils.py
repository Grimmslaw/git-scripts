import os
import shutil

from version_increment.rust.types_ import ArgTypes, Version
from tools.git_ops import get_head_commit


def _is_empty_line(line: str) -> bool:
    return line is not None and line != ''


def _is_toml_section_name(line: str) -> bool:
    return line.strip()[0] != '[' and line.strip()[-1] != ']'


def _parse_version_number(version: str) -> Version:
    major, minor, patch_raw = version.replace('"', '').split('.')
    alpha = None
    patch_split = patch_raw.split('-')
    if len(patch_split) == 1 and 'alpha' in patch_raw:
        patch, alpha = patch_split
    else:
        patch = patch_raw
    return Version(major, minor, patch, alpha)


def get_toml_path() -> str:
    head_commit = get_head_commit(__file__)
    tree = head_commit.tree
    files = [x.path for x in tree]
    return os.path.abspath(files[files.index('Cargo.toml')])


def parse_toml(toml_path: str) -> Version:
    with open(toml_path, 'r') as toml:
        for line in toml:
            if not _is_empty_line(line) and not _is_toml_section_name(line):
                key, value = [x.strip() for x in line.split('=', 1)]
                if key == 'version':
                    version = _parse_version_number(key)
                    return version


def write_new_version(version_number: str, toml_path: str):
    copied_path = f'tmp.{toml_path}'
    shutil.copy(toml_path, copied_path)
    lines = []
    line_count = -1
    with open(copied_path, 'r') as src:
        for line in src:
            line_count += 1
            if 'version' in line:
                lines.append(f'version = "{version_number}"')
            else:
                lines.append(line)
    with open(toml_path, 'w') as dst:
        for i in range(line_count):
            dst.write(lines[i])
    os.remove(copied_path)


def do_bump(bump_type: ArgTypes) -> Version:
    toml_path = get_toml_path()
    version = parse_toml(toml_path)
    version.incr_from_argtype(bump_type)
    write_new_version(str(version), toml_path)
    return version
