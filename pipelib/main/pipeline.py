__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.logger import logger


class Pipeline:
    """
    A pipeline holds or more steps to complete in a comparison process.
    """

    def __init__(self, steps=None):
        self.steps = []
        [self.add_step(s) for s in steps or []]

    def _validate_step(self, previous, step):
        """
        Validate that a step has the correct classes and can interact with
        the previous step.
        """
        for required in ["run", "_run"]:
            if not hasattr(step, required):
                logger.exit(f"Step {step} is missing required attribute {required}")

        # The new step must return something
        if not step.return_type:
            logger.error(f"Step {step} does not return anything.")
            return False

        return True

    def add_step(self, step):
        """
        Add a step to the pipeline, validating it first
        """
        if isinstance(step, (list, tuple)) and len(step) > 2:
            logger.warning(f"Step {step} cannot have length > 2, skipping.")
            return

        # Length == 1 is only a step no kwargs
        kwargs = {}
        if isinstance(step, (list, tuple)) and len(step) == 1:
            step = step[0]

        elif isinstance(step, (list, tuple)) and len(step) == 2:
            kwargs = step[1]
            step = step[0]

        # The final thing has to be a step!
        if "pipelib.main.steps" in step.__class__.__module__:
            self._add_step(step, kwargs)
        else:
            logger.warning(f"Malformed step {step}, not adding to pipeline!")

    def _add_step(self, step, kwargs=None):
        """
        Adding a step means checking that kwargs are provided
        """
        kwargs = kwargs or {}

        addstep = True
        if self.steps:
            addstep = self._validate_step(self.steps[-1][0], step)
        if addstep:
            logger.info(f"Adding step {step}")
            self.steps.append((step, kwargs))

    def run(self, items):
        """
        Run the pipeline to parse the items.
        """
        for step, kwargs in self.steps:
            if not items:
                break
            items = step.run(items=items, **kwargs)
        return items
