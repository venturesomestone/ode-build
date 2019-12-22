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
This support module contains the functions for running the
composing mode of the script.
"""

import os

from .support.cmake_generators import get_ninja_cmake_generator_name

from .support.environment import \
    get_build_root, get_composing_directory, get_destination_directory

from .util import shell


def create_composing_root(source_root, target):
    """
    Checks if the directory for the actual build of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    target -- The target system of the build represented by a
    Target.
    """
    composing_root = get_composing_directory(
        build_root=get_build_root(source_root=source_root),
        target=target
    )
    if not os.path.exists(composing_root):
        shell.makedirs(path=composing_root)
    return composing_root


def create_destination_root(source_root, target):
    """
    Checks if the directory for the built products of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    target -- The target system of the build represented by a
    Target.
    """
    destination_root = get_destination_directory(
        build_root=get_build_root(source_root=source_root),
        target=target
    )
    if not os.path.exists(destination_root):
        shell.makedirs(path=destination_root)
    return destination_root


def compose_project(
    toolchain,
    arguments,
    project_root,
    build_root,
    composing_root,
    destination_root,
    dependencies_root
):
    """
    Builds the project this script acts on.

    toolchain -- The toolchain object of the run.

    arguments -- The parsed command line arguments of the run.

    project_root -- The root directory of the project this script
    acts on.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    composing_root -- The directory for the actual build of the
    project.

    destination_root -- The directory where the built product is
    placed in.

    dependencies_root -- The directory for the dependencies.
    """
    cmake_call = [
        toolchain.cmake,
        project_root,
        "-G",
        arguments.cmake_generator,
        "-DCMAKE_C_COMPILER={}".format(toolchain.cc),
        "-DCMAKE_CXX_COMPILER={}".format(toolchain.cxx),
        "-DCMAKE_INSTALL_PREFIX={}".format(destination_root),
        "-DODE_BUILD_TEST={}".format("ON" if arguments.build_test else "OFF"),
        # TODO
        "-DODE_CXX_VERSION={}".format("c++17"),
        "-DODE_DEPENDENCY_PREFIX={}".format(dependencies_root),
        "-DODE_VERSION={}".format(arguments.ode_version),
        "-DANTHEM_VERSION={}".format(arguments.anthem_version),
        "-DODE_OPENGL_VERSION_MAJOR={}".format(
            arguments.opengl_version.split(".")[0]
        ),
        "-DODE_OPENGL_VERSION_MINOR={}".format(
            arguments.opengl_version.split(".")[1]
        ),
        "-DODE_LOGGER_NAME={}".format("TODO"),
        "-DODE_WINDOW_NAME={}".format("TODO"),
        "-DANTHEM_LOGGER_NAME={}".format("TODO"),
        "-DANTHEM_WINDOW_NAME={}".format("TODO")
    ]

    if arguments.cmake_generator == get_ninja_cmake_generator_name():
        cmake_call.extend(
            ["-DCMAKE_MAKE_PROGRAM={}".format(toolchain.build_system)]
        )

    cmake_env = {"CC": toolchain.cc, "CXX": toolchain.cxx}

    with shell.pushd(composing_root):
        shell.call(
            cmake_call,
            env=cmake_env,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        shell.call(
            [toolchain.build_system],
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        shell.call(
            [toolchain.build_system, "install"],
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
