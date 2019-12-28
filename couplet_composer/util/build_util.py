# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem project.
#
# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License
#
# ------------------------------------------------------------- #

"""
This support module contains helpers for making build calls for
the dependencies.
"""

import os

from ..support.cmake_generators import get_ninja_cmake_generator_name

from . import shell


def build_with_cmake(
    toolchain,
    cmake_generator,
    source_directory,
    temporary_root,
    dependencies_root,
    target,
    host_system,
    build_variant,
    cmake_options=None,
    do_install=True,
    dry_run=None,
    print_debug=None
):
    """
    Calls CMake and invokes the build script produced by CMake.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated.

    source_directory -- The path to the root directory of the
    project to be built with CMake.

    temporary_root -- The path to the root directory that is used
    for temporary files.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    build_variant -- The build variant used to build the project.

    cmake_options -- Additional options passed to CMake.

    do_install -- Whether or not the install command should be
    called after building the project.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    cmake_call = [
        toolchain.cmake,
        source_directory,
        "-DCMAKE_BUILD_TYPE={}".format(build_variant),
        "-DCMAKE_INSTALL_PREFIX={}".format(dependencies_root)
    ]

    if cmake_generator == get_ninja_cmake_generator_name():
        cmake_call.extend([
            "-DCMAKE_MAKE_PROGRAM={}".format(toolchain.build_system)
        ])

    cmake_call.extend(["-G", cmake_generator])

    if cmake_options:
        if isinstance(cmake_options, dict):
            for k, v in cmake_options.items():
                if isinstance(v, bool):
                    cmake_call.extend(
                        ["-D{}={}".format(k, ("ON" if v else "OFF"))]
                    )
                else:
                    cmake_call.extend(["-D{}={}".format(k, v)])
        else:
            cmake_call += cmake_options

    cmake_env = {"CC": toolchain.cc, "CXX": toolchain.cxx}

    build_directory = os.path.join(temporary_root, "build")

    shell.makedirs(build_directory, dry_run=dry_run, echo=print_debug)

    with shell.pushd(build_directory, dry_run=dry_run, echo=print_debug):
        shell.call(
            cmake_call,
            env=cmake_env,
            dry_run=dry_run,
            echo=print_debug
        )
        shell.call([toolchain.build_system], dry_run=dry_run, echo=print_debug)
        if do_install:
            shell.call(
                [toolchain.build_system, "install"],
                dry_run=dry_run,
                echo=print_debug
            )
