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
This support module has the info necessary for building CMake.
"""

import os
import platform

from support import data

from util import binaries, cmake, diagnostics, shell, workspace


def skip_build():
    """Whether the build is skippped."""
    return data.session.toolchain.cmake is not None
    # and not data.session.args.build_cmake


def _bin_name(component):
    if platform.system() == "Windows":
        return os.path.join("bin", "cmake.exe")
    elif platform.system() == "Linux":
        return os.path.join("bin", "cmake")
    elif platform.system() == "Darwin":
        return os.path.join("CMake.app", "Contents", "bin", "cmake")
    diagnostics.fatal("{} on {} is not supported".format(
        component.repr,
        platform.system()
    ))


def build(component):
    """Builds the dependency."""
    bin_name = _bin_name(component)
    data.session.toolchain.cmake = os.path.join(
        data.session.shared_build_dir,
        bin_name
    )
    if binaries.exist(component, bin_name):
        return
    src_dir = workspace.source_dir(component)
    if platform.system() == "Darwin":
        shell.copytree(
            os.path.join(src_dir, "CMake.app"),
            os.path.join(data.session.shared_build_dir, "CMake.app")
        )
    else:
        shell.copytree(
            os.path.join(src_dir, "bin"),
            os.path.join(data.session.shared_build_dir, "bin")
        )
        shell.copytree(
            os.path.join(src_dir, "doc"),
            os.path.join(data.session.shared_build_dir, "doc")
        )
        shell.copytree(
            os.path.join(src_dir, "man"),
            os.path.join(data.session.shared_build_dir, "man")
        )
        shell.copytree(
            os.path.join(src_dir, "share"),
            os.path.join(data.session.shared_build_dir, "share")
        )
