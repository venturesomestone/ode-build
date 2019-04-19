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

from util import shell, workspace


def get_dependency(component, github_data):
    """
    Download an asset from GitHub.

    component -- the dependency mapping
    github_data -- mapping containing data relevant for the
    download
    """
    shell.rmtree(workspace.source_dir(component))
    shell.rmtree(workspace.temporary_dir(component))
    shell.makedirs(workspace.source_dir(component))
    shell.makedirs(workspace.temporary_dir(component))
