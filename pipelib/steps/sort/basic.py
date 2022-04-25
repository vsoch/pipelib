__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step

# Filters take some string and return true/false if a condition passes


class BasicSort(step.Step):
    """
    Sort the list of items
    """

    def run(self, items, **kwargs):
        reverse = kwargs.get("reverse", False)
        return sorted(items, reverse=reverse)
