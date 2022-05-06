__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step
import pipelib.wrappers as wrappers

# Container tag specific steps


class ContainerTagSort(step.BaseStep):
    """
    Parse container tag versions and return a filtered and sorted set.

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(ContainerTagSort(ascending=True))
    >>> pipeline.run(["1.2.3", "1.2.1"])
    ['1.2.1', '1.2.3']
    >>> pipeline = Pipeline(ContainerTagSort(ascending=False))
    >>> pipeline.run(["1.2.3", "1.2.1"])
    ['1.2.3', '1.2.1']
    >>> pipeline = Pipeline(ContainerTagSort(unique_major=True))
    >>> pipeline.run(["1.2.3", "1.2.1"])
    ['1.2.3']
    """

    required = ["unique_patch", "unique_minor", "unique_major", "ascending"]
    defaults = {
        "unique_patch": False,
        "unique_minor": False,
        "unique_major": False,
        "ascending": False,
    }

    """
    Parse container tag versions and return a filtered and sorted set.
    This is a special step that uses a LooseVersionWrapper to ensure we
    parse out weird commits, and can return a list sorted regular or reverse,
    and also honor the user's request to keep unique patches, major, or minor
    versions. By default we return unique patches.

    Parameters
    ==========
    unique_patch (bool): keep latest patch versions (e.g., 9.4.2)
    unique_minor (bool): only keep latest major + minor version (e.g., 9.4)
    unique_major (bool): only keep latest major version (e.g., 9)
    ascending (bool) : return ascending ordered results
    """

    def run(self, items: list) -> list:
        """
        Wrap in a LooseVersion to allow sort and filter of tags.
        """
        unique_major = self.kwargs.get("unique_major")
        unique_minor = self.kwargs.get("unique_minor")
        unique_patch = self.kwargs.get("unique_patch")
        ascending = self.kwargs.get("ascending")

        # We must choose one convention, default to patch
        if not any([unique_major, unique_minor, unique_patch]):
            unique_patch = True

        # Convert to LooseVersionWrapper
        items = [wrappers.VersionWrapper(x) for x in items]

        # The sorting will tag a subset with "remove" that aren't sortable
        # This has latest at the top so we grab newest versions of each
        items.sort(reverse=True)

        # Now only take the top major / minor of each
        filtered = []
        seen = set()

        for version in items:

            # Keep all that don't have any kind of versioning we understand
            if (
                not version.major_minor
                and not version.major
                and not version.major_minor_patch
                and version.version not in seen
            ):
                filtered.append(version)
                continue

            # Patch takes preference to minor, then major
            if unique_patch and (
                version.major_minor_patch is not None
                and version.major_minor_patch not in seen
            ):
                filtered.append(version)
                seen.add(version.major_minor_patch)
                seen.add(version.major_minor)
                seen.add(version.major)

            elif unique_minor and (
                version.major_minor is not None and version.major_minor not in seen
            ):
                filtered.append(version)
                seen.add(version.major_minor)
                seen.add(version.major)

            elif unique_major and (
                version.major is not None and version.major not in seen
            ):
                filtered.append(version)
                seen.add(version.major)

        # By default from above they are decending, greatest (newest) to least (oldest)
        if ascending:
            filtered.sort()
        return filtered
