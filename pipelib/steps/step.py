__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.logger import logger
import pipelib.wrappers as wrappers
import inspect
import typing
import abc
import copy


class BaseStep:
    """
    A step is a named interaction in a pipeline. Items must be provided to parse.
    """

    required = []
    defaults = {}

    def __init__(self, **kwargs):
        self.kwargs = self.check_kwargs(kwargs)

    @property
    def name(self):
        return self.__class__.__name__.split(".")[-1]

    @property
    def baseclass(self):
        return self.__class__.__base__

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    @property
    def return_type(self) -> typing.Type:
        """
        Return the return types for the run function.
        """
        # Some steps operation on all items at top level (no need for _run)
        if not hasattr(self, "_run"):
            sig = inspect.signature(self.run)
        else:
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
        # Some steps operation on all items at top level (no need for _run)
        if not hasattr(self, "_run"):
            return {}
        sig = inspect.signature(self._run)
        return {name: x.annotation for name, x in sig.parameters.items()}

    def check_kwargs(self, kwargs) -> dict:
        """
        Ensure required kwargs are provided, or go to defaults, return populated
        """
        for required in self.required:
            if required not in kwargs and required in self.defaults:
                kwargs[required] = self.defaults[required]
            if required not in kwargs:
                logger.exit("%s argument missing for step %s" % (required, self.name))

        # Add all defaults
        for k, v in self.defaults.items():
            if k not in kwargs:
                kwargs[k] = v
        return kwargs


class Step(BaseStep):
    """
    A standard step returns a new item or None (indicative to not add)
    """

    def run(self, items: list, **kwargs) -> list:
        """
        Loop through items, keep items that are not None.
        """
        keepers = []
        for item in items:

            # Keep the item if the outcome is True
            updated = self._run(item, **self.kwargs)

            # A step can choose to preserve a wrappr (or not)
            # always pass the item through a wrapper to keep the original
            if updated and not wrappers.is_wrapped(updated):
                updated = wrappers.Wrapper(updated)

                # We could be handed an wrapped item
                if hasattr(item, "_original"):
                    updated._original = item._original

                # Or an uwrapped item
                else:
                    updated._original = item

            if updated:
                keepers.append(updated)
        return keepers

    @abc.abstractmethod
    def _run(self, item: typing.Any, **kwargs) -> bool:
        raise NotImplementedError("A step must have a _run function.")


class BooleanStep(BaseStep):
    """
    A boolean step must return true or false, and we keep the item if True.
    """

    def __init__(self, **kwargs):

        # Make sure we don't re-create anything!
        if not hasattr(self, "reverse"):
            self.reverse = False
        if not hasattr(self, "compose"):
            self.compose = []
        super().__init__(**kwargs)

    @property
    def operator_name(self):
        """
        Ensure the operator is represented in the class name
        """
        if self.reverse:
            return "Not" + self.name
        return self.name

    def __invert__(self):
        """
        We can say "~step" and reverse the logic.
        """
        self.reverse = True
        return self

    def check_compatibility(self, other):
        """
        Ensure that two steps have the same base class.
        """
        if self.baseclass != other.baseclass:
            logger.exit(
                f"{self} and {other} have different base classes and cannot be combined."
            )

    def __or__(self, other):
        """
        Combine boolean steps into a single step with OR. E.g.,

        steps.HasAllLower() | steps.HasMinLength()
        """
        return self._and_or(other, operator="OR")

    def __and__(self, other):
        """
        Combine boolean steps into a single step with AND. E.g.,

        steps.HasAllLower() & steps.HasMinLength()
        """
        return self._and_or(other)

    def _and_or(self, other, operator="AND"):
        """
        The base function to run a logical combination AND or OR
        """
        if operator not in ["AND", "OR"]:
            logger.exit("Operator %s is not supported." % operator)

        # The classes must be the same type
        self.check_compatibility(other)

        # We don't want to update the original class
        this = copy.deepcopy(self)

        # Previous _run functions added to the class by name
        run1_func = this.name + "_run"
        run2_func = other.name + "_run"

        # Combine kwargs to pass to both
        combined_kwargs = copy.deepcopy(this.kwargs)
        combined_kwargs.update(other.kwargs)

        # Assemble list of previously composed functions
        composed = copy.deepcopy(this.compose)
        composed += other.compose

        # Add each to composed
        for item in [(run1_func, this.reverse), (run2_func, other.reverse)]:
            composed.append(
                {"func": item[0], "reversed": item[1], "operator": operator}
            )

        # The custom run should run the first and second
        def _run(self, item: typing.Any, **kwargs) -> bool:
            result = None

            # Update the result with each check
            for entry in self.composed:

                # If we don't have a result, AND is True, OR is False
                if result == None:
                    result = True if operator == "AND" else False
                res = getattr(self, entry["func"])(item, **kwargs)
                if entry["reversed"]:
                    res = not res
                if operator == "AND":
                    result = result and res
                else:
                    result = result or res
            return result

        # Create a new Class named by the two classes we are combining
        classname = "%s_%s_%s" % (
            this.operator_name,
            operator.upper(),
            other.operator_name,
        )
        combined = type(
            classname,
            (this.baseclass,),
            {
                "_run": _run,
                run1_func: this._run,
                run2_func: other._run,
                "composed": composed,
                "kwargs": combined_kwargs,
            },
        )
        return combined(**combined_kwargs)

    def run(self, items: list) -> list:
        """
        Run is the main calling step for a pipeline step.

        All steps are required to have run functions to handle args/kwargs
        This function checks that required arguments are provided, and then
        calls the underlying _run that should be implemented by the step.
        """
        keepers = []
        for item in items:

            # Keep the item if the outcome is True
            outcome = self._run(item, **self.kwargs)

            # True == keep, and we don't want to reverse that logic
            if outcome and not self.reverse:
                keepers.append(item)

            # False == keep
            if not outcome and self.reverse:
                keepers.append(item)
        return keepers

    @abc.abstractmethod
    def _run(self, item: typing.Any, **kwargs) -> bool:
        raise NotImplementedError("A step must have a _run function.")
