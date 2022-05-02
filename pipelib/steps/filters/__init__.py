import pipelib.utils as utils
import os

here = os.path.abspath(os.path.dirname(__file__))
for obj, imported in utils.dynamic_import(__name__, here):
    globals()[obj] = imported
