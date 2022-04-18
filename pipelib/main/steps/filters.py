__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from . import step
import typing
import re

# Filters take some string and return true/false if a condition passes


class ExcludeFilter(step.BooleanStep):
    """
    Don't include items that match the filters of interest.
    """

    required = ["filters"]

    def _inner_run(self, item, **kwargs) -> list:
        filters = kwargs.get("filters") or []
        if item and filters:
            for pattern in filters:
                if re.search(pattern, item):
                    return True
        return False

    def _run(self, item, **kwargs) -> list:
        return self._inner_run(item, **kwargs) == False


class IncludeFilter(ExcludeFilter):
    """
    Only include items that match the filters of interest.
    """

    def _run(self, item, **kwargs) -> list:
        return self._inner_run(item, **kwargs) == True


class IncludeAllLetters(step.BooleanStep):
    """
    Keep items with all letters (no numbers or special characters)
    """

    def _run(self, item, **kwargs) -> typing.Type:
        return re.sub("([a-zA-Z])+", "", item) == ""


class ExcludeAllLetters(step.BooleanStep):
    """
    Exclude items with all letters (no numbers or special characters)
    """

    def _run(self, item, **kwargs) -> typing.Type:
        return re.sub("([a-z])+", "", item) != ""


class IncludeLowercaseLettersNumbers(step.BooleanStep):
    """
    Keep the string if it's the string is only lowercase letters and numbers.
    """

    def _run(self, item, **kwargs) -> typing.Type:
        # If we remove all letters and nothing left, filter out
        return re.sub("([0-9]|[a-z])+", "", item) == ""


class ExcludeLowercaseLettersNumbers(step.BooleanStep):
    """
    Exclude the string if it doesn't have only lowercase letters and numbers.
    """

    def _run(self, item, **kwargs) -> typing.Type:
        # If we remove all letters and nothing left, filter out
        return re.sub("([0-9]|[a-z])+", "", item) != ""
