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
This support module has the info necessary for downloading Clara.
"""

from github import release

from util import workspace

from util.mapping import Mapping

# TODO Clara shall be got rid of


SOURCE = True
GITHUB = True
GITHUB_DATA = Mapping(
    owner="catchorg",
    version_prefix="v"
)


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_directory(component):
        release.basic_tag(component, GITHUB_DATA)
