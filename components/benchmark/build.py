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
Benchmark.
"""

import os

from support import data

from util import binaries, cmake, shell, workspace


def dependencies():
    """
    Gives the names of the components that this component depends
    on.
    """
    return ["cmake"]


def build(component):
    """Builds the dependency."""
    if binaries.exist(component, os.path.join("lib", "libbenchmark.a")):
        return
    with workspace.build_directory(component) as build_dir:
        if binaries.exist(component, os.path.join("lib", "libbenchmark.a")):
            return
        src_dir = workspace.source_dir(component)
        # shell.copytree(src_dir, build_dir)
        cmake.call(
            component,
            src_dir,
            build_dir,
            {"BENCHMARK_ENABLE_GTEST_TESTS": False}
        )
        binaries.compile(component, build_dir)
