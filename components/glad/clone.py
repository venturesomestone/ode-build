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
This support module has the info necessary for downloading Glad.
"""

from github import tag

from util import workspace

from util.mapping import Mapping


SOURCE = True
GITHUB_DATA = Mapping(
    owner="Dav1dde",
    version_prefix="v"
)


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_dir_context(component):
        tag.clone(component, GITHUB_DATA)
