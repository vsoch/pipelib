__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step

# Filters take some string and return true/false if a condition passes


class ToLowercase(step.Step):
    """
    Convert the item to all lowercase.

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(ToLowercase())
    >>> pipeline.run(["Mango"])
    ['mango']
    >>> pipeline.run(["avocado"])
    ['avocado']
    """

    def _run(self, item, **kwargs):
        return item.lower()


class ToString(step.Step):
    """
    Convert the item to a string (typically from a wrapper)

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(ToString())
    >>> pipeline.run([1])
    ['1']
    >>> pipeline.run(["abcde"])
    ['abcde']
    """

    def _run(self, item, **kwargs):
        return str(item)


class SplitAndJoinN(step.Step):
    """
    Split a string by one delimiter, join by another.
    Both are required. By default, we split and join for ALL
    but this can be customized with split_n.

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(SplitAndJoinN(split_by='-', join_by='_'))
    >>> pipeline.run(["one-two-three"])
    ['one_two_three']
    >>> pipeline = Pipeline(SplitAndJoinN(split_by='-', join_by='_', split_n=1))
    >>> pipeline.run(["one-two-three"])
    ['one_two-three']
    """

    required = ["split_by", "join_by"]
    defaults = {"split_n": -1}

    def _run(self, item, **kwargs):
        split_by = kwargs.get("split_by")
        split_n = kwargs.get("split_n")
        join_by = kwargs.get("join_by")
        return join_by.join(item.split(split_by, split_n))
