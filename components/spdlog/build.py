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
This support module has the info necessary for building spdlog.
"""

import os

from support import data

from util import binaries, shell, workspace


def build(component):
    """Builds the dependency."""
    bin_name = os.path.join("include", "spdlog")
    if binaries.exist(component, bin_name):
        return
    if not os.path.isdir(
        os.path.join(data.session.shared_build_dir, "include")
    ):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "include"))
    if os.path.isdir(os.path.join(data.session.shared_build_dir, bin_name)):
        shell.rmtree(os.path.join(data.session.shared_build_dir, bin_name))
    shell.copytree(
        os.path.join(workspace.source_dir(component), "include", "spdlog"),
        os.path.join(data.session.shared_build_dir, bin_name)
    )
