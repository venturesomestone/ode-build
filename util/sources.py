# ------------------------------------------------------------- #
#                 Obliging Ode & Unsung Anthem
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""
This support module has common source code related utilities.
"""

import os

from . import diagnostics, workspace


def exist(component):
    """Check if the source for the product exists."""
    src_dir = workspace.source_dir(component)
    if not os.path.exists(src_dir):
        diagnostics.fatal(
            "Cannot find source directory for {} (tried {})".format(
                component.repr,
                src_dir
            )
        )
