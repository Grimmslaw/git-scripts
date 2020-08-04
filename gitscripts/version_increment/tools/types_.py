"""Types used to accomplish the functionality of the version-increment scripts."""

import logging
from dataclasses import dataclass

from tools.str_utils import safe_strip

LOGGER = logging.getLogger(__name__)
VERSION_PATTERN = 'x.y.za'


@dataclass
class Alpha:
    """
    A dataclass wrapping the data and functionality of the "alpha" portion of a version number (e.g. "-alpha1").

    It consists of a version number and a switch representing if it exists or not.
    """

    exists: bool = True
    version: int = -1

    def __str__(self):
        """
        Format the alpha version (if it exists) as `-alpha{version}`

        :return:
            the formatted string
        """
        return f'-alpha{self.version}' if self.exists else ''

    def incr(self):
        """
        Increments the version of this "alpha" if it currently exists.
        """
        self.version += int(self.exists)

    def remv(self):
        """
        "Zeroes-out" this alpha object if it already exists
        :return:
        """
        if self.exists:
            self.exists = False
            self.version = -1


@dataclass
class Version:
    """
    Represents a project's semantic-versioning version number (e.g. X.X.X-alphaX)
    """

    _major: int
    _minor: int
    _patch: int
    _alpha: Alpha

    def __str__(self):
        """
        Format the Version using the semantic versioning pattern: `{major}.{minor}.{patch}(-alpha{subpatch})?`

        :return:
            the formatted Version number
        """
        return VERSION_PATTERN.replace('x', str(self._major))\
            .replace('y', str(self._minor))\
            .replace('z', str(self._patch))\
            .replace('a', str(self._alpha))

    def major(self) -> 'Version':
        """
        Increments this version's major portion and zeroes out lower portions.

        :return:
            this version object
        """
        self._major += 1
        self._minor = 0
        self._patch = 0
        self._alpha.remv()
        return self

    def minor(self) -> 'Version':
        """
        Increments this version's minor portion and zeroes out lower portions.

        :return:
            this version object
        """
        self._minor += 1
        self._patch = 0
        self._alpha.remv()
        return self

    def patch(self) -> 'Version':
        """
        Increments this version's patch portion and zeroes out lower portions.

        :return:
            this version object
        """
        self._patch += 1
        self._alpha.remv()
        return self

    def subpatch(self) -> 'Version':
        """
        Increments this version's subpatch portion and zeroes out lower portions.

        :return:
            this version object
        """
        self._alpha.incr()
        return self

    alpha = subpatch

    def unalpha(self) -> 'Version':
        """
        Removes the alpha from this version

        :return:
            this version object
        """
        self._alpha.remv()
        return self

    @classmethod
    def from_str(cls, version: str) -> 'Version':
        prepped_major, prepped_minor, patch_raw = version.replace('"', '').split('.')
        alpha_raw = None
        patch_split = patch_raw.split('-')
        if len(patch_split) == 2 and 'alpha' in patch_raw:
            prepped_patch, alpha_raw = patch_split
            prepped_alpha = alpha_raw.replace('alpha', '')
        else:
            prepped_patch = patch_raw
            prepped_alpha = alpha_raw
        return Version.instance(safe_strip(prepped_major), safe_strip(prepped_minor),
                                safe_strip(prepped_patch), safe_strip(prepped_alpha))

    @classmethod
    def instance(cls, major: str = None, minor: str = None, patch: str = None, alpha: str = None):
        """
        Safely creates a Version object given any of its portions (defaulting to 0)

        :param major:
        :param minor:
        :param patch:
        :param alpha:
        :return:
            a new Version object
        """
        s_major = int(major) or 0
        s_minor = int(minor) or 0
        s_patch = int(patch) or 0
        if alpha is None:
            s_subpatch = Alpha()
        else:
            s_subpatch = alpha
        return Version(s_major, s_minor, s_patch, s_subpatch)


####
# The following are convenience methods for increasing their namesake portion of the given version.
####


def major(version: Version) -> Version:
    """
    Increases the major portion of this version number.

    :param Version version:
        the version whose major portion should be bumped
    :return:
        the version after bumping its major portion
    """
    return version.major()


def minor(version: Version) -> Version:
    """
    Increases the major portion of this version number.

    :param Version version:
        the version whose major portion should be bumped
    :return:
        the version after bumping its major portion
    """
    return version.minor()


def patch(version: Version) -> Version:
    """
    Increases the major portion of this version number.

    :param Version version:
        the version whose major portion should be bumped
    :return:
        the version after bumping its major portion
    """
    return version.patch()


def subpatch(version: Version) -> Version:
    """
    Increases the major portion of this version number.

    :param Version version:
        the version whose major portion should be bumped
    :return:
        the version after bumping its major portion
    """
    return version.subpatch()


alpha = subpatch


def unalpha(version: Version) -> Version:
    """
    Increases the major portion of this version number.

    :param Version version:
        the version whose major portion should be bumped
    :return:
        the version after bumping its major portion
    """
    return version.unalpha()
