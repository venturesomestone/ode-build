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


def _build():
    product = data.build.products.benchmark
    bin_path = os.path.join(data.build.local_root, "lib", "libbenchmark.a")
    build_dir = workspace.build_dir(product)
    if common.build.binary_exists(product=product, path=bin_path):
        return
    shell.makedirs(build_dir)
    common.build.build_call(product=product, cmake_args={
        "BENCHMARK_ENABLE_GTEST_TESTS": False
    })
    # if data.build.args.stdlib == "libc++":
    #     common.build.build_call(product=product, cmake_args={
    #         "BENCHMARK_ENABLE_GTEST_TESTS": False,
    #         "BENCHMARK_USE_LIBCXX": True
    #     })
    # elif data.build.args.build_llvm:
    #     cmakelist = os.path.join(workspace.source_dir(product), "CMakeLists.txt")
    #     cmakelist2 = os.path.join(workspace.source_dir(product), "CMakeLists2.txt")
    #     shell.move(cmakelist, cmakelist2)
    #     with open(cmakelist2, "rt") as fin:
    #         with open(cmakelist, "wt") as fout:
    #             for line in fin:
    #                 fout.write(line.replace("c++11", "{}".format(data.build.std)))
    #     shell.rm(cmakelist2)
    #     std_path = os.path.join(data.build.local_root, "include", "c++", "v1")
    #     lib_path = os.path.join(data.build.local_root, "lib")
    #     common.build.build_call(product=product, cmake_args={
    #         "BENCHMARK_ENABLE_GTEST_TESTS": False,
    #         "BENCHMARK_USE_LIBCXX": True,
    #         "CMAKE_CXX_FLAGS": "-I{} -L{}".format(std_path, lib_path)
    #     })
    # else:
    #     common.build.build_call(product=product, cmake_args={
    #         "BENCHMARK_ENABLE_GTEST_TESTS": False
    #     })


def _copy_source():
    product = data.build.products.benchmark
    if os.path.isdir(os.path.join(data.build.local_root, "src", "benchmark")):
        shell.rmtree(os.path.join(data.build.local_root, "src", "benchmark"))
    shell.makedirs(os.path.join(data.build.local_root, "src", "benchmark"))
    shell.copytree(
        os.path.join(workspace.source_dir(product), "src"),
        os.path.join(data.build.local_root, "src", "benchmark"))
    if os.path.isdir(workspace.include_file("benchmark")):
        shell.rmtree(workspace.include_file("benchmark"))
    shell.copytree(
        os.path.join(workspace.source_dir(product), "include", "benchmark"),
        workspace.include_file("benchmark"))


def do_build():
    """Build Google Benchmark."""
    product = data.build.products.benchmark
    common.build.check_source(product)
    if data.build.args.build_llvm:
        _copy_source()
    else:
        _build()


def should_build():
    """Check whether this product should be built."""
    return True
