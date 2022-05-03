__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step


class HasMinLength(step.BooleanStep):
    """
    Keep items (return true) given a minimum length

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(HasMinLength(length=9))
    >>> pipeline.run(["tooshort"])
    []
    >>> pipeline.run(["muchlonger"])
    ['muchlonger']
    """

    required = ["length"]
    defaults = {"length": 10}

    def _run(self, item, **kwargs) -> bool:
        length = kwargs["length"]
        if item and len(item) >= length:
            return True
        return False


class HasMaxLength(step.BooleanStep):
    """
    Keep items (return true) given a maximum length

    >>> from pipelib.pipeline import Pipeline
    >>> pipeline = Pipeline(HasMaxLength(length=6))
    >>> pipeline.run(["short"])
    ['short']
    >>> pipeline.run(["toolong"])
    []
    """

    required = ["length"]
    defaults = {"length": 10}

    def _run(self, item, **kwargs) -> bool:
        length = kwargs["length"]
        if item and len(item) <= length:
            return True
        return False
