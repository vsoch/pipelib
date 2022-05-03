__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step


class ToInteger(step.Step):
    """
    Convert the item to an integer

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(ToInteger())
    >>> pipeline.run(['1'])
    ['1']
    """

    def _run(self, item, **kwargs):
        return str(item)
