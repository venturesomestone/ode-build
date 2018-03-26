#===------------------------------- build.py -----------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (c) 2018 Venturesome Stone
# Licensed under GNU Affero General Public License v3.0

"""The support module containing the utilities for Google Benchmark build."""


import os
import platform

from build_utils import shell, workspace

from products import common

from script_support import data


def do_build():
    """Build Google Benchmark."""
    product = data.build.products.benchmark
    common.build.check_source(product)
    bin_path = os.path.join(data.build.local_root, "lib", "libbenchmark.a")
    build_dir = workspace.build_dir(product)
    if common.build.binary_exists(product=product, path=bin_path):
        return
    shell.makedirs(build_dir)
    if data.build.args.stdlib == "libc++":
        common.build.build_call(product=product, cmake_args={
            "BENCHMARK_ENABLE_GTEST_TESTS": False,
            "BENCHMARK_USE_LIBCXX": True
        })
    elif data.build.args.build_llvm:
        std_path = os.path.join(data.build.local_root, "include", "c++", "v1")
        lib_path = os.path.join(data.build.local_root, "lib")
        common.build.build_call(product=product, cmake_args={
            "BENCHMARK_ENABLE_GTEST_TESTS": False,
            "BENCHMARK_USE_LIBCXX": True,
            "CMAKE_CXX_FLAGS": "-I{} -L{}".format(std_path, lib_path)
        })
    else:
        common.build.build_call(product=product, cmake_args={
            "BENCHMARK_ENABLE_GTEST_TESTS": False
        })


def should_build():
    """Check whether this product should be built."""
    return True
