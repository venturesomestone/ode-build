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
This support module has the info necessary for building Google
Test.
"""

import os
import platform

from support import data

from util import binaries, cmake, shell, workspace


def dependencies():
    """
    Gives the names of the components that this component depends
    on.
    """
    return ["cmake"]


def _copy_windows(component, src_dir):
    build_dir = workspace.build_dir(component)
    if not os.path.isdir(
        os.path.join(data.session.shared_build_dir, "lib")
    ):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "lib"))
    lib_file = os.path.join(data.session.shared_build_dir, "lib", "gtest.lib")
    if os.path.exists(lib_file):
        shell.rm(lib_file)
    shell.copy(os.path.join(build_dir, "Debug", "gtest.lib"), lib_file)
    if not os.path.isdir(
        os.path.join(data.session.shared_build_dir, "include")
    ):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "include"))
    include_dir = os.path.join(
        data.session.shared_build_dir,
        "include",
        "gtest"
    )
    if os.path.isdir(include_dir):
        shell.rmtree(include_dir)
    shell.copytree(os.path.join(src_dir, "include", "gtest"), include_dir)


def _copy(component, src_dir):
    build_dir = workspace.build_dir(component)
    if not os.path.isdir(os.path.join(data.session.shared_build_dir, "lib")):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "lib"))
    lib_file = os.path.join(data.session.shared_build_dir, "lib", "libgtest.a")
    if os.path.exists(lib_file):
        shell.rm(lib_file)
    shell.copy(os.path.join(build_dir, "libgtest.a"), lib_file)
    lib_file = os.path.join(
        data.session.shared_build_dir,
        "lib",
        "libgtest_main.a"
    )
    if os.path.exists(lib_file):
        shell.rm(lib_file)
    shell.copy(os.path.join(build_dir, "libgtest_main.a"), lib_file)
    if not os.path.isdir(
        os.path.join(data.session.shared_build_dir, "include")
    ):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "include"))
    include_dir = os.path.join(
        data.session.shared_build_dir,
        "include",
        "gtest"
    )
    if os.path.isdir(include_dir):
        shell.rmtree(include_dir)
    shell.copytree(os.path.join(src_dir, "include", "gtest"), include_dir)


def build(component):
    """Builds the dependency."""
    if platform.system() == "Windows":
        bin_name = os.path.join("lib", "gtest.lib")
    else:
        bin_name = os.path.join("lib", "libgtest.a")
    if binaries.exist(component, bin_name):
        return
    with workspace.build_directory(component) as build_dir:
        src_dir = os.path.join(workspace.source_dir(component), "googletest")
        if platform.system() == "Windows":
            cmake.call(
                component,
                src_dir,
                build_dir,
                {
                    "CMAKE_CXX_FLAGS":
                        "/D_SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING"
                }
            )
        else:
            cmake.call(component, src_dir, build_dir)
        binaries.compile(
            component,
            build_dir,
            solution_name="gtest",
            install=False
        )
        if platform.system() == "Windows":
            _copy_windows(component, src_dir)
        else:
            _copy(component, src_dir)
