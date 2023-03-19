import os
import sys

from helpers import generate_rst_table

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../"))
import pipelib.utils as utils  # noqa
from pipelib.steps import all_steps  # noqa

steps = [("type", "name", "module", "description")]
for step_type, lookup in all_steps.items():
    for step_name, step_module in lookup.items():
        # Get the description from first line of docstring
        docstring = utils.get_docstring(step_module)[0]
        steps.append((step_type, step_name, step_module.__name__, docstring[0]))

with open("steps.inc", "w") as fd:
    fd.write(generate_rst_table(steps))
