__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from . import step

# Filters take some string and return true/false if a condition passes


class AllLowercase(step.Step):
    """
    Convert the item to all lowercase.
    """

    def _run(self, item, **kwargs) -> list:
        return item.lower()
