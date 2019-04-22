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
This support module has the info necessary for downloading CMake.
"""

import os
import platform

from support import data

from util import diagnostics, http, shell, workspace


SOURCE = False
GITHUB = False


def _resolve_linux(component):
    version_data = component.version_data
    # Starting at CMake 3.1.0 'Linux-x86_64' variant is
    # available, before that the only option is 'Linux-i386'
    if version_data.major < 3:
        return "Linux-i386"
    if version_data.minor < 1:
        return "Linux-i386"
    return "Linux-x86_64"


def _resolve_darwin(component):
    version_data = component.version_data
    # Starting at CMake 3.1.1 'Darwin-x86_64' variant is
    # available, before that the only option is
    # 'Darwin-universal'
    if version_data.major < 3:
        return "Darwin-universal"
    if version_data.minor <= 1:
        if version_data.patch < 1:
            return "Darwin-universal"
        return "Darwin-x86_64"
    return "Darwin-x86_64"


def resolve_platform(component):
    """
    Resolve the platform that is used in the URL when CMake is
    downloaded.
    """
    if platform.system() == "Windows":
        return "win32-x86"
    elif platform.system() == "Linux":
        return _resolve_linux(component)
    elif platform.system() == "Darwin":
        return _resolve_darwin(component)
    diagnostics.warn("{} isn't supported on this platform".format(
        component.repr))
    return None


def _move_files(component):
    subdir = "cmake-{}-{}".format(
        component.version, resolve_platform(component))
    shell.rmtree(workspace.source_dir(component))
    diagnostics.debug("The name of the {} subdirectory is {}".format(
        component.repr, subdir))

    if platform.system() == "Darwin":
        cmake_app = os.listdir(os.path.join(
            workspace.temporary_dir(component), subdir))[0]

        shell.copytree(
            os.path.join(
                workspace.temporary_dir(component), subdir, cmake_app),
            os.path.join(workspace.source_dir(component), "CMake.app"))
    else:
        shell.copytree(
            os.path.join(workspace.temporary_dir(component), subdir),
            workspace.source_dir(component))


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_directory(component):
        url = "{}://cmake.org/files/v{}/cmake-{}-{}.{}".format(
            data.session.connection_protocol,
            "{}.{}".format(
                component.version_data.major, component.version_data.minor),
            component.version, resolve_platform(component),
            "zip" if platform.system() == "Windows" else "tar.gz")
        dest = os.path.join(
            workspace.temporary_dir(component), "cmake.{}".format(
                "zip" if platform.system() == "Windows" else "tar.gz"))
        http.stream(url, dest)
        shell.tar(dest, workspace.temporary_dir(component))
        _move_files(component)
