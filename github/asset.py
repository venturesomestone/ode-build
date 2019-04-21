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
This support module has functions for downloading content from
GitHub.
"""

import os
import platform

from util import diagnostics, shell, workspace

from . import tag


def basic_asset(component, github_data):
    """
    Downloads a basic asset from GitHub.
    """
    diagnostics.trace("Going to download an asset of")
    diagnostics.trace_head(component.repr)
    tag.download(component, github_data)
    if platform.system() != "Windows":
        source_dir = workspace.source_dir(component)
        version_dir = os.path.dirname(source_dir)
        shell.rmtree(source_dir)
        shell.rmtree(version_dir)
        shell.copytree(
            os.path.join(workspace.temporary_dir(component), component.key),
            workspace.source_dir(component))
