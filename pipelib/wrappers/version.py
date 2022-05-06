__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from packaging.version import Version
from .base import Wrapper
import re

# https://discuss.python.org/t/pep-632-deprecate-distutils-module/5134/129?page=7


class LooseVersion(Version):
    def __init__(self, vstring=None):
        if vstring:
            self.parse(vstring)

    component_re = re.compile(r"(\d+ | [a-z]+ | \.)", re.VERBOSE)


class VersionWrapper(Wrapper, LooseVersion):
    """
    Loose version comparison.

    Given that a comparison fails, we simply tag it for removal. We also
    do custom parsing of the version string for common patterns of container
    tags to derive a more meaningful version.
    """

    @property
    def major_minor(self):
        if self._major_minor:
            return ".".join(str(x) for x in self._major_minor)

    @property
    def major_minor_patch(self):
        if self._major_minor_patch:
            return ".".join(str(x) for x in self._major_minor_patch)

    @property
    def major(self):
        if self._major:
            return ".".join(str(x) for x in self._major)

    def __init__(self, item=None):
        super().__init__(item)
        self.tags = set()
        self.version = []
        if item:
            self.parse(item)

    def parse(self, vstring):
        """
        Parse a version string (vstring) into pieces. Strings are added as tags.
        """
        self.vstring = vstring
        contenders = [x for x in self.component_re.split(vstring) if x and x != "."]
        components = []

        # Add non-numerical components as tags
        for obj in contenders:
            try:
                components.append(int(obj))
            except ValueError:
                self.tags.add(obj)
                pass

        # Save parsed major.minor.patch in different lengths
        self._major_minor_patch = None
        self._major_minor = None
        self._major = None

        # more strict considers duplicate of major "the same"
        if len(components) >= 1:
            self._major = components[0:1]
        if len(components) >= 2:
            self._major_minor = components[0:2]
        if len(components) >= 3:
            self._major_minor_patch = components[0:3]
        self.version = components

    def _cmp(self, other):
        if isinstance(other, str):
            other = LooseVersion(other)

        # We can only compare matching types
        shortest = min(len(other.version), len(self.version))

        for i in range(shortest):
            this_version = self.version[i]
            other_version = other.version[i]

            if type(this_version) != type(other_version):
                continue

            if this_version == other_version:
                continue
            elif this_version < other_version:
                return -1
            elif this_version > other_version:
                return 1

        # If we get to the bottom, consider equal
        return 0
