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
This support module has the set up functions used to create the
mapping of the build components.
"""

import json
import os

from support import data

from support.variables import ODE_SOURCE_ROOT, ODE_REPO_NAME

from util import diagnostics


__all__ = ["run"]


def run(bootstrap):
    """
    Create the mappings of the dependencies and components of the
    build.

    bootstrap -- whether or not this is called from the bootstrap
    script and not the build script
    """
    with open(os.path.join(
            ODE_SOURCE_ROOT, ODE_REPO_NAME, "util", "build",
            "dependencies.json")) as f:
        components = json.load(f)

    for key, component in components.items():
        diagnostics.trace("Creating a mapping for the component {}".format(key))
