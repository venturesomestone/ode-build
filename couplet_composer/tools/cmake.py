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

from ..support.environment import get_temporary_directory

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.cache import cached

from ..util import http, shell


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


def _resolve_cmake_download_target(version, system):
    """
    Gives the target used in the name of the CMake archive
    downloaded for installation.

    version -- The full version number of CMake.

    system -- The system for which the wanted CMake build is for.
    """
    major_version, minor_version, patch_version = tuple(map(
        int,
        version.split(".")
    ))

    if system == get_darwin_system_name():
        # Starting at CMake 3.1.1 'Darwin-x86_64' variant is
        # available, before that the only option is
        # 'Darwin-universal'.
        if major_version < 3:
            return "Darwin-universal"
        if minor_version <= 1:
            if patch_version < 1:
                return "Darwin-universal"
            return "Darwin-x86_64"
        return "Darwin-x86_64"
    elif system == get_linux_system_name():
        def _resolve_linux():
            # Starting at CMake 3.1.0 'Linux-x86_64' variant is
            # available, before that the only option is
            # 'Linux-i386'.
            if major_version < 3:
                return "Linux-i386"
            if minor_version < 1:
                return "Linux-i386"
            return "Linux-x86_64"
        return _resolve_linux()
    elif system == get_windows_system_name():
        return "win32-x86"


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


def install_tool(
    build_root,
    tools_root,
    version,
    target,
    host_system,
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

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """

    temp_dir = get_temporary_directory(build_root=build_root)
    tool_temp_dir = os.path.join(temp_dir, "cmake")

    shell.makedirs(temp_dir)
    shell.makedirs(tool_temp_dir)

    major_version, minor_version, patch_version = tuple(map(
        int,
        version.split(".")
    ))

    url = "https://cmake.org/files/v{major}.{minor}/cmake-" \
        "{major}.{minor}.{patch}-{target}.{archive}".format(
            major=major_version,
            minor=minor_version,
            patch=patch_version,
            target=_resolve_cmake_download_target(
                version=version,
                system=host_system
            ),
            archive="zip" if host_system == "Windows" else "tar.gz"
        )
    dest = os.path.join(
        tool_temp_dir,
        "cmake.{}".format("zip" if host_system == "Windows" else "tar.gz")
    )

    http.stream(
        url=url,
        destination=dest,
        host_system=host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )
    shell.tar(dest, tool_temp_dir)
