__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import pipelib.steps as step
import pipelib.pipeline as pipeline

# not commit like will filter out items that look like commits
# (minimum length of 8) and all letters numbers
RemoveCommits = pipeline.Pipeline(
    steps=(
        step.filters.HasMinLength(length=8) & ~step.filters.HasAllLowerLettersNumbers(),
    )
)
