__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step
import pipelib.wrappers as wrappers

# Major tags sort

class MajorTagSort(step.BaseStep):
    """
    Parse versions that have only major versions (e.g., v3)
    An example of this is GitHub releases - e.g., we often just want @v3.

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(MajorTagSort(ascending=True))
    >>> pipeline.run(["1.2.3", "1.2.1"])
    []
    >>> pipeline = Pipeline(MajorTagSort(ascending=False))
    >>> pipeline = Pipeline(ContainerTagSort(ascending=False))
    >>> pipeline.run(["v3", "1.2.3", "v2"])
    ['v1', 'v3']
    >>> pipeline = Pipeline(MajorTagSort(ascending=True))
    >>> pipeline.run(["v3", "1.2.3", "v2"])
    ['v3', 'v1']
    """
    def run(self, items: list) -> list:
        """
        Wrap in a LooseVersion to allow sort and filter of tags.
        """
        ascending = self.kwargs.get("ascending")

        # Convert to LooseVersionWrapper
        items = [wrappers.VersionWrapper(x) for x in items]

        # The sorting will tag a subset with "remove" that aren't sortable
        # This has latest at the top so we grab newest versions of each
        items.sort(reverse=True)

        # Now only take the top major / minor of each
        filtered = []
        seen = set()

        for version in items:

            # Keep all that are only major versions
            if version.major and not version.major_minor and version not in seen:
                filtered.append(version)
                seen.add(version)
                continue

        # By default from above they are decending, greatest (newest) to least (oldest)
        if ascending:
            filtered.sort()
        return filtered
