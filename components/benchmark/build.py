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


def build(component):
    """Builds the dependency."""
    if binaries.exist(component, os.path.join("lib", "libbenchmark.a")):
        return
    with workspace.build_directory(component) as build_dir:
        if binaries.exist(component, os.path.join("lib", "libbenchmark.a")):
            return
        src_dir = workspace.source_dir(component)
        shell.copytree(src_dir, build_dir)
        cmake.call(
            component,
            build_dir,
            {"BENCHMARK_ENABLE_GTEST_TESTS": False}
        )
    # bin_path = os.path.join(data.session.local_root, "lib", "libbenchmark.a")
    # build_dir = workspace.build_dir(component)
    # if common.build.binary_exists(product=product, path=bin_path):
    #     return
    # shell.makedirs(build_dir)
    # common.build.build_call(product=product, cmake_args={
    #     "BENCHMARK_ENABLE_GTEST_TESTS": False
    # })
