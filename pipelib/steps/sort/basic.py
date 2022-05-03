__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step

# Filters take some string and return true/false if a condition passes


class BasicSort(step.Step):
    """
    Sort the list of items

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(BasicSort())
    >>> pipeline.run([3, 2, 1])
    ['1', '2', '3']
    >>> pipeline = Pipeline(BasicSort(reverse=True))
    >>> pipeline.run([1, 2, 3])
    ['3', '2', '1']
    """

    defaults = {"reverse": False}

    def run(self, items, **kwargs):
        """
        This run happens for the top level of items.
        """
        reverse = self.kwargs["reverse"]
        return sorted(items, reverse=reverse)
