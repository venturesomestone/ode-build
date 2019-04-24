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
This support module has the info necessary for building
stb_image.
"""

import os

from support import data

from util import binaries, shell, workspace


def skip_build(component, has_correct_version):
    """Whether the build is skippped."""
    return binaries.exist(component, os.path.join("include", "stb_image.h")) \
        and has_correct_version


def build(component):
    """Builds the dependency."""
    bin_name = os.path.join("include", "stb_image.h")
    if not os.path.isdir(
        os.path.join(data.session.shared_build_dir, "include")
    ):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "include"))
    if os.path.exists(os.path.join(data.session.shared_build_dir, bin_name)):
        shell.rmtree(os.path.join(data.session.shared_build_dir, bin_name))
    shell.copy(
        os.path.join(workspace.source_dir(component), "stb_image.h"),
        os.path.join(data.session.shared_build_dir, bin_name)
    )
