__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step

# Filters take some string and return true/false if a condition passes


class ToLowercase(step.Step):
    """
    Convert the item to all lowercase.
    """

    def _run(self, item, **kwargs):
        return item.lower()


class ToString(step.Step):
    """
    Convert the item to a string (typically from a wrapper)
    """

    def _run(self, item, **kwargs):
        return item.lower()


class SplitAndJoinN(step.Step):
    """
    Split a string by one delimiter, join by another.
    Both are required. By default, we split and join for ALL
    but this can be customized with split_n.
    """

    required = ["split_by", "join_by"]
    defaults = {"split_n": 1}

    def _run(self, item, **kwargs):
        split_by = kwargs.get("split_by")
        split_n = kwargs.get("split_n")
        join_by = kwargs.get("join_by")
        return join_by.join(item.split(split_by, split_n))
