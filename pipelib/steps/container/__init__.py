import os

import pipelib.utils as utils

_lookup = {}
here = os.path.abspath(os.path.dirname(__file__))
for obj, imported in utils.dynamic_import(__name__, here):
    globals()[obj] = imported
    _lookup[obj] = imported
