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
This support module has the info necessary for downloading Ninja.
"""

from util.mapping import Mapping


SOURCE = False
GITHUB = True
GITHUB_DATA = Mapping(
    owner="ninja-build",
    version_prefix="v",
    asset=Mapping(
        darwin="ninja-mac.zip",
        windows="ninja-win.zip",
        linux="ninja-linux.zip"
    )
)


def get_dependency(component):
    """Downloads the dependency."""
