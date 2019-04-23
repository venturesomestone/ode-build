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

"""This support module has CMake utilities."""

from support import data

from . import shell, workspace


def call(component, source_directory, build_directory, cmake_args=None):
    """Builds the given component by using CMake."""
    args = data.session.args
    toolchain = data.session.toolchain
    use_ninja = \
        args.cmake_generator == "Ninja" or args.cmake_generator == "Xcode"

    cmake_call = [
        toolchain.cmake,
        source_directory,
        "-DCMAKE_INSTALL_PREFIX={}".format(data.session.shared_build_dir)
    ]

    # TODO
    # if build_type:
    #     cmake_call += ["-DCMAKE_BUILD_TYPE={}".format(build_type)]

    if use_ninja:
        cmake_call += ["-DCMAKE_MAKE_PROGRAM={}".format(toolchain.ninja)]
        cmake_call += ["-G", "Ninja"]
    else:
        cmake_call += ["-G", args.cmake_generator]

    if cmake_args:
        if isinstance(cmake_args, dict):
            for k, v in cmake_args.items():
                if isinstance(v, bool):
                    cmake_call += ["-D{}={}".format(k, ("ON" if v else "OFF"))]
                else:
                    cmake_call += ["-D{}={}".format(k, v)]
        else:
            cmake_call += cmake_args

    cmake_env = {"CC": toolchain.cc, "CXX": toolchain.cxx}

    with shell.pushd(build_directory):
        shell.call(cmake_call, env=cmake_env)
