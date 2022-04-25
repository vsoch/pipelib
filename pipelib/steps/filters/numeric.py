__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.steps import step


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
