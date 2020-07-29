from dataclasses import dataclass
from enum import Enum

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

    exists: bool
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

    def __str__(self):
        return VERSION_PATTERN.replace('x', str(self.major))\
            .replace('y', str(self.minor))\
            .replace('z', str(self.patch))\
            .replace('a', str(self.alpha))

    def incr(self, major: bool = False, minor: bool = False, patch: bool = False,
             alpha: bool = False, unalpha: bool = False) -> None:
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
        major = bump_type == ArgTypes.MAJOR
        minor = bump_type == ArgTypes.MINOR
        patch = bump_type == ArgTypes.PATCH
        alpha = bump_type == ArgTypes.ALPHA
        unalpha = bump_type == ArgTypes.UNALPHA
        self.incr(major, minor, patch, alpha, unalpha)
