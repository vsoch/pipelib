__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.logger import logger
import inspect
import typing
import abc


class BaseStep:
    """
    A step is a named interaction in a pipeline. Items must be provided to parse.
    """

    required = []
    defaults = {}

    @property
    def name(self):
        return self.__class__.__name__.split(".")[-1]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    @property
    def return_type(self) -> typing.Type:
        """
        Return the return types for the run function.
        """
        sig = inspect.signature(self._run)
        return sig.return_annotation

    @property
    def arg_types(self) -> list:
        """
        Return the argument types (list)
        """
        return list(self.args.values())

    @property
    def args(self) -> dict:
        """
        Return the arguments in a named lookup
        """
        sig = inspect.signature(self._run)
        return {name: x.annotation for name, x in sig.parameters.items()}

    def check_kwargs(self, kwargs) -> dict:
        """
        Ensure required kwargs are provided, or go to defaults, return populated
        """
        for required in self.required:
            if required not in kwargs and required in self.defaults:
                kwargs = self.defaults[required]
            if required not in kwargs:
                logger.exit("%s argument missing for step %s" % (required, self.name))
        return kwargs


class Step(BaseStep):
    """
    A standard step returns a new item or None (indicative to not add)
    """

    def run(self, items: list, **kwargs) -> list:
        """
        Loop through items, keep items that are not None.
        """
        kwargs = self.check_kwargs(kwargs)

        keepers = []
        for item in items:

            # Keep the item if the outcome is True
            item = self._run(item, **kwargs)
            if item:
                keepers.append(item)
        return keepers

    @abc.abstractmethod
    def _run(self, item: typing.Any, **kwargs) -> bool:
        raise NotImplementedError("A step must have a _run function.")


class BooleanStep(BaseStep):
    """
    A boolean step must return true or false, and we keep the item if True.
    """

    def run(self, items: list, **kwargs) -> list:
        """
        Run is the main calling step for a pipeline step.

        All steps are required to have run functions to handle args/kwargs
        This function checks that required arguments are provided, and then
        calls the underlying _run that should be implemented by the step.
        """
        kwargs = self.check_kwargs(kwargs)

        keepers = []
        for item in items:

            # Keep the item if the outcome is True
            if self._run(item, **kwargs):
                keepers.append(item)
        return keepers

    @abc.abstractmethod
    def _run(self, item: typing.Any, **kwargs) -> bool:
        raise NotImplementedError("A step must have a _run function.")
