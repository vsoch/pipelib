from . import filters
from . import transform
from . import container
from . import sort
from . import release

all_steps = {
    "filter": filters._lookup,
    "transform": transform._lookup,
    "container": container._lookup,
    "sort": sort._lookup,
    "release": release._lookup,
}


def iter_steps():
    """
    Convenince function to iterate over steps.
    """
    for step_type, lookup in all_steps.items():
        for step_name, step_module in lookup.items():
            yield step_type, step_name, step_module
