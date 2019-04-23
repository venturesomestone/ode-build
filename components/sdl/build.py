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
This support module has the info necessary for building Simple
DirectMedia Layer.
"""

import os
import platform

from support import data

from util import binaries, cmake, shell, workspace


def _build_windows(component, src_dir, build_dir):
    if not os.path.isdir(os.path.join(
        data.session.shared_build_dir, "include"
    )):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "include"))
    include_dir = os.path.join(
        data.session.shared_build_dir,
        "include",
        "SDL2"
    )
    if os.path.isdir(include_dir):
        shell.rmtree(include_dir)
    shell.copytree(os.path.join(src_dir, "include"), include_dir)
    if not os.path.isdir(os.path.join(data.session.shared_build_dir, "lib")):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "lib"))
    for lib_file in os.listdir(os.path.join(
        data.session.shared_build_dir,
        "lib"
    )):
        if "SDL" in lib_file:
            shell.rm(
                os.path.join(data.session.shared_build_dir, "lib", lib_file)
            )
    for lib_file in os.listdir(os.path.join(src_dir, "lib", "x86")):
        shell.copy(
            os.path.join(src_dir, "lib", "x86", lib_file),
            os.path.join(data.session.shared_build_dir, "lib", lib_file)
        )


def _build(component, src_dir, build_dir):
    cmake.call(component, src_dir, build_dir)
    binaries.compile(component, build_dir)


def build(component):
    """Builds the dependency."""
    bin_name = os.path.join(
        "lib",
        "SDL2.lib" if platform.system() == "Windows" else "libSDL2d.a"
    )
    if binaries.exist(component, bin_name):
        return
    with workspace.build_directory(component) as build_dir:
        src_dir = workspace.source_dir(component)
        if platform.system() == "Windows":
            _build_windows(component, src_dir, build_dir)
        else:
            _build(component, src_dir, build_dir)
