import logging
from dataclasses import dataclass
from enum import Enum

from version_increment.rust.general_utils import safe_str_to_int, str_is_empty

LOGGER = logging.getLogger(__name__)
VERSION_PATTERN = 'x.y.za'

# TODO: this whole system should probably be refactored someday


class ArgTypes(Enum):

    MAJOR = 'MAJOR'
    MINOR = 'MINOR'
    PATCH = 'PATCH'
    ALPHA = 'ALPHA'
    UNALPHA = 'UNALPHA'


ARGTYPE_LOOKUP = {
    'MAJOR': ArgTypes.MAJOR,
    'MINOR': ArgTypes.MINOR,
    'PATCH': ArgTypes.PATCH,
    'ALPHA': ArgTypes.ALPHA,
    'UNALPHA': ArgTypes.UNALPHA
}


@dataclass
class Alpha:

    exists: bool = True
    version: int = -1

    def __str__(self):
        return f'-alpha{self.version}' if self.exists else ''

    def incr(self):
        # only increments if Alpha exists
        self.version += int(self.exists)

    def remv(self):
        if not self.exists:
            self.exists = False
            self.version = -1


@dataclass
class Version:

    major: int
    minor: int
    patch: int
    alpha: Alpha = Alpha(False)

    def __init__(self, major=None, minor=None, patch=None, alpha=None):
        self.major = safe_str_to_int(major, 0)
        self.minor = safe_str_to_int(minor, 0)
        self.patch = safe_str_to_int(patch, 0)
        LOGGER.debug(f'received alpha={alpha}, type={type(alpha)}')
        if str_is_empty(alpha) and not isinstance(alpha, (str, int)):
            self.alpha = alpha

    def __str__(self):
        return VERSION_PATTERN.replace('x', str(self.major))\
            .replace('y', str(self.minor))\
            .replace('z', str(self.patch))\
            .replace('a', str(self.alpha))

    def incr(self, major: bool = False, minor: bool = False, patch: bool = False,
             alpha: bool = False, unalpha: bool = False) -> None:
        LOGGER.debug(f'type(major)={type(self.major)}')
        LOGGER.debug(f'type(minor)={type(self.minor)}')
        LOGGER.debug(f'type(patch)={type(self.patch)}')
        LOGGER.debug(f'type(alpha)={type(self.alpha)}')
        if major:
            self.major += 1
            self.minor = self.patch = 0
            self.alpha.remv()
        elif minor:
            self.minor += 1
            self.patch = 0
            self.alpha.remv()
        elif patch:
            self.patch += 1
            self.alpha.remv()
        elif alpha:
            self.alpha.incr()
        elif unalpha:
            self.alpha.remv()

    def incr_from_argtype(self, bump_type: ArgTypes):
        major = bump_type == ArgTypes.MAJOR or self.major
        LOGGER.debug(f'major={major}, type={type(major)}')
        minor = bump_type == ArgTypes.MINOR or self.minor
        patch = bump_type == ArgTypes.PATCH or self.patch
        alpha = bump_type == ArgTypes.ALPHA or self.alpha
        unalpha = bump_type == ArgTypes.UNALPHA
        self.incr(major, minor, patch, alpha, unalpha)
