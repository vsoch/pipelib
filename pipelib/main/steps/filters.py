__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from . import step
import re

# Filters take some string and return true/false if a condition passes


class HasFilter(step.BooleanStep):
    """
    Determine if items have a filter of interest
    """

    required = ["filters"]

    def _run(self, item, **kwargs) -> list:
        filters = kwargs.get("filters") or []
        if item and filters:
            for pattern in filters:
                if re.search(pattern, item):
                    return True
        return False


class HasMinLength(step.BooleanStep):
    required = ["length"]
    defaults = {"length": 10}
    """
    Keep items with all letters (no numbers or special characters)
    """

    def _run(self, item, **kwargs) -> bool:
        length = kwargs["length"]
        if item and len(item) >= length:
            return True
        return False


class HasMaxLength(step.BooleanStep):
    required = ["length"]
    defaults = {"length": 10}
    """
    Keep items with all letters (no numbers or special characters)
    """

    def _run(self, item, **kwargs) -> bool:
        length = kwargs["length"]
        if item and len(item) <= length:
            return True
        return False


class HasAllLetters(step.BooleanStep):
    """
    Keep items with all letters (no numbers or special characters)
    """

    def _run(self, item, **kwargs) -> bool:
        return re.sub("([a-zA-Z])+", "", item) == ""


class HasAllLowerLettersNumbers(step.BooleanStep):
    """
    Keep the string if it's the string is only lowercase letters and numbers.
    """

    def _run(self, item, **kwargs) -> bool:
        return re.sub("([0-9]|[a-z])+", "", item) == ""
