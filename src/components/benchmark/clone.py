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
This support module has the info necessary for downloading Google
Benchmark.
"""

from github import github

from util.mapping import Mapping


SOURCE = True
GITHUB = True
GITHUB_DATA = Mapping(
    owner="google",
    version_prefix="v"
)


def get_dependency(component):
    """Downloads the dependency."""
    github.get_dependency(component, GITHUB_DATA)
