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
import platform

from support import data

from util import binaries, cmake, diagnostics, shell, workspace


def skip_build(component, has_correct_version):
    """Whether the build is skippped."""
    if platform.system() == "Windows":
        diagnostics.debug("{} won't be built on Windows".format(
            data.session.dependencies["benchmark"].repr
        ))
        return True
    return binaries.exist(component, os.path.join("lib", "libbenchmark.a")) \
        and has_correct_version


def dependencies():
    """
    Gives the names of the components that this component depends
    on.
    """
    return ["cmake"]


def build(component):
    """Builds the dependency."""
    with workspace.build_directory(component) as build_dir:
        src_dir = workspace.source_dir(component)
        cmake.call(
            component,
            src_dir,
            build_dir,
            {"BENCHMARK_ENABLE_GTEST_TESTS": False}
        )
        binaries.compile(component, build_dir)
