__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat"
__license__ = "MPL 2.0"


def is_wrapped(item):
    """
    Determine if an item is wrapped based on finding the parent class
    """
    return Wrapper in item.__class__.__mro__


class Wrapper(str):
    """
    A base wrapper provides the same functionality as a string.
    """

    def __init__(self, item=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The wrapper always holds the original
        if hasattr(item, "_original"):
            self._original = item._original
        else:
            self._original = item
