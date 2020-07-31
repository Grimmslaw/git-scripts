import logging
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)
VERSION_PATTERN = 'x.y.za'


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
        if self.exists:
            self.exists = False
            self.version = -1


@dataclass
class Version:

    _major: int
    _minor: int
    _patch: int
    _alpha: Alpha

    def __str__(self):
        return VERSION_PATTERN.replace('x', str(self._major))\
            .replace('y', str(self._minor))\
            .replace('z', str(self._patch))\
            .replace('a', str(self._alpha))

    def major(self) -> 'Version':
        self._major += 1
        self._minor = 0
        self._patch = 0
        self._alpha.remv()
        return self

    def minor(self) -> 'Version':
        self._minor += 1
        self._patch = 0
        self._alpha.remv()
        return self

    def patch(self) -> 'Version':
        self._patch += 1
        self._alpha.remv()
        return self

    def subpatch(self) -> 'Version':
        self._alpha.incr()
        return self

    alpha = subpatch

    def unalpha(self) -> 'Version':
        self._alpha.remv()
        return self

    @classmethod
    def instance(cls, major: str = None, minor: str = None, patch: str = None, alpha: str = None):
        s_major = int(major) or 0
        s_minor = int(minor) or 0
        s_patch = int(patch) or 0
        s_subpatch = Alpha(version=int(alpha.replace('alpha', ''))) if alpha else Alpha()
        return Version(s_major, s_minor, s_patch, s_subpatch)


def major(version: Version) -> Version:
    return version.major()


def minor(version: Version) -> Version:
    return version.minor()


def patch(version: Version) -> Version:
    return version.patch()


def subpatch(version: Version) -> Version:
    return version.subpatch()


alpha = subpatch


def unalpha(version: Version) -> Version:
    return version.unalpha()
