__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step


class CleanCommit(step.Step):
    """
    Given a container tag that has -- and _ separating some commit and version,
    remove and return just the version string. E.g.,:

    0.9.10--hdbcaa40_3 -> 0.9.10.3

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(CleanCommit())
    >>> pipeline.run(["0.9.10--hdbcaa40_3"])
    ['0.9.10.3']
    >>> pipeline.run(["abcde"])
    ['abcde']
    """

    def _run(self, item, **kwargs):
        if "--" in item and "_" in item:
            start, rest = item.split("--", 1)
            ending = rest.split("_", 1)[-1]

            # '0.1.19.10'
            item = "%s.%s" % (start, ending)

        # If we get here and still have -- replace with .
        for token in ["--", "-"]:
            if token in item:
                item = item.replace(token, ".")
        return item
