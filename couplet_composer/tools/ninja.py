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
This support module contains the functions related to the
building and finding Ninja.
"""

import os

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.cache import cached


def _get_ninja_version_info():
    """
    Gives a tuple containing the version information of Ninja,
    i.e. (major, minor, patch).
    """
    return 1, 9, 0


@cached
def get_required_ninja_version():
    """
    Gives the version of Ninja that is donwloaded when it isn't
    found.
    """
    return ".".join([str(n) for n in _get_ninja_version_info()])


@cached
def get_local_ninja_executable(tools_root, version, system):
    """
    Gives the path to the local Ninja executable.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full Ninja version number.

    system -- The system for which the wanted Ninja build is for.
    """
    def _resolve_executable():
        return os.path.join("bin", "ninja.exe") \
            if system == get_windows_system_name() \
            else os.path.join("bin", "ninja")

    return os.path.join(
        tools_root,
        "ninja",
        version,
        system,
        _resolve_executable()
    )


################################################################
# TOOLDATA FUNCTIONS
################################################################

@cached
def get_tool_type():
    """Returns the type of the tool for the toolchain."""
    return "build_system"


@cached
def get_version(target, host_system):
    """
    Returns a string that represents the version of the tool that
    is downloaded when it isn't found.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
    return get_required_ninja_version()


@cached
def get_local_executable(tools_root, version, target, host_system):
    """
    Returns path to the local executable of the tool.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full version number of the tool.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
    return get_local_ninja_executable(
        tools_root=tools_root,
        version=version,
        system=host_system
    )


def install_tool(
    build_root,
    tools_root,
    version,
    target,
    host_system,
    github_user_agent,
    github_api_token,
    dry_run=None,
    print_debug=None
):
    """
    Installs the tool by downloading and possibly building it.
    Returns the path to the built tool executable.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full version number of the tool.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    github_user_agent -- The user agent used when accessing the
    GitHub API.

    github_api_token -- The GitHub API token that is used to
    access the API.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
