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
This support module has the info necessary for building Clara.
"""

import os

from support import data

from util import binaries, cmake, shell, workspace


def build(component):
    """Builds the dependency."""
    if binaries.exist(component, os.path.join("include", "clara.hpp")):
        return
    src_dir = workspace.source_dir(component)
    if not os.path.isdir(
        os.path.join(data.session.shared_build_dir, "include")
    ):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "include"))
    shell.copy(
        os.path.join(src_dir, "single_include", "clara.hpp"),
        os.path.join(data.session.shared_build_dir, "include", "clara.hpp")
    )
