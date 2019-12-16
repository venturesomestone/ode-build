# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem project.
#
# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License
#
# ------------------------------------------------------------- #

"""
This support module contains the functions for resolving and
building the dependencies required to by the project that this
script acts on.
"""

import json

from .support.dependency_data import create_dependency_data


def construct_dependencies_data(data_file):
    """
    Constructs a list of objects of type 'DependencyData'
    representing the dependecies of the project this script acts
    on. This function isn't pure as it gets data from a JSON file
    in project this script acts on and from various dependency
    modules.

    data_file -- The file in the project this script acts on that
    contains the data about the required versions of the
    dependencies.
    """
    json_data = None
    with open(data_file) as f:
        json_data = json.load(f)
    return [create_dependency_data(key, node)
            for key, node in json_data.items()]


def install_dependencies(
    dependencies_data,
    toolchain,
    cmake_generator,
    target,
    host_system,
    github_user_agent,
    github_api_token,
    dependencies_root,
    build_root,
    dry_run,
    print_debug
):
    """
    Installs the dependencies of the project.

    dependencies_data -- List of objects of type DependencyData
    that contain the functions for checking and building the
    dependencies.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated. It's used to determine which build system is
    checked for and built if necessary.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    github_user_agent -- The user agent used when accessing the
    GitHub API.

    github_api_token -- The GitHub API token that is used to
    access the API.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
