# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""
This support module has the info necessary for downloading Ninja.
"""

import os
import platform

from github import release

from util import shell, workspace

from util.mapping import Mapping


SOURCE = False
GITHUB_DATA = Mapping(
    owner="ninja-build",
    version_prefix="v"
)


def get_dependency(component):
    """Downloads the dependency."""
    if platform.system() == "Darwin":
        asset_file = "ninja-mac.zip"
    elif platform.system() == "Linux":
        asset_file = "ninja-linux.zip"
    elif platform.system() == "Windows":
        asset_file = "ninja-win.zip"
    with workspace.clone_dir_context(component):
        release.basic_asset(component, GITHUB_DATA, asset_file)
        # source_dir = workspace.source_dir(component)
        shell.tar(
            os.path.join(workspace.temporary_dir(component), asset_file),
            workspace.source_dir(component)
        )
        # shell.copytree(
        #     os.path.join(workspace.temporary_dir(component), component.key),
        #     workspace.source_dir(component))
