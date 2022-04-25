__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step
import re


class HasPatterns(step.BooleanStep):
    """
    Determine if items match a pattern of interest
    """

    required = ["filters"]

    def _run(self, item, **kwargs) -> list:
        filters = kwargs.get("filters") or []
        if item and filters:
            for pattern in filters:
                if re.search(pattern, item):
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
