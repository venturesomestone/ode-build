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
building and finding CMake.
"""

import os

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.cache import cached


def _get_cmake_version_info():
    """
    Gives a tuple containing the version information of CMake,
    i.e. (major, minor, patch).
    """
    return 2, 8, 12


@cached
def get_required_cmake_version():
    """
    Gives the version of CMake that is donwloaded when CMake
    isn't found.
    """
    return ".".join([str(n) for n in _get_cmake_version_info()])


@cached
def get_local_cmake_executable(tools_root, version, system):
    """
    Gives the path to the local CMake executable.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full CMake version number.

    system -- The system for which the wanted CMake build is for.
    """
    def _resolve_executable():
        if system == get_darwin_system_name():
            return os.path.join("CMake.app", "Contents", "bin", "cmake")
        elif system == get_linux_system_name():
            return os.path.join("bin", "cmake")
        elif system == get_windows_system_name():
            return os.path.join("bin", "cmake.exe")
        raise NotImplementedError

    return os.path.join(
        tools_root,
        "cmake",
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
    return "cmake"


@cached
def get_version(target, host_system):
    """
    Returns a string that represents the version of the tool that
    is downloaded when it isn't found.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
    return get_required_cmake_version()


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
    return get_local_cmake_executable(
        tools_root=tools_root,
        version=version,
        system=host_system
    )


@cached
def install_tool(tools_root, version, target, host_system):
    """
    Installs the tool by downloading and possibly building it.
    Returns the path to the built tool executable.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full version number of the tool.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
