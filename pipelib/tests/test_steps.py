#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pipelib.steps import iter_steps
import pipelib.utils


@pytest.mark.parametrize("step_type,step_name,step_module", list(iter_steps()))
def test_step(tmp_path, step_type, step_name, step_module):
    """
    Test step basic functionality
    """
    # This will fail if not defined
    docs = pipelib.utils.get_docstring(step_module)

    has_code = False
    for line in docs:
        if ">>>" in line:
            has_code = True
    assert has_code
