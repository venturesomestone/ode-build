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

from .support.platform_names import \
    get_darwin_system_name, get_linux_system_name

from .support.project_libraries import \
    get_anthem_shared_name, get_anthem_static_name, get_ode_shared_name, \
    get_ode_static_name

from .util import shell


def create_composing_root(
    source_root,
    target,
    cmake_generator,
    build_variant,
    assertions
):
    """
    Checks if the directory for the actual build of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.

    assertions -- Whether the assertions are enabled in the
    project.
    """
    composing_root = get_composing_directory(
        build_root=get_build_root(source_root=source_root),
        target=target,
        cmake_generator=cmake_generator,
        build_variant=build_variant,
        assertions=assertions
    )
    if not os.path.exists(composing_root):
        shell.makedirs(path=composing_root)
    return composing_root


def create_destination_root(
    source_root,
    target,
    cmake_generator,
    build_variant,
    assertions,
    version
):
    """
    Checks if the directory for the built products of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.

    assertions -- Whether the assertions are enabled in the
    project.

    version -- The version number of the project.
    """
    destination_root = get_destination_directory(
        build_root=get_build_root(source_root=source_root),
        target=target,
        cmake_generator=cmake_generator,
        build_variant=build_variant,
        assertions=assertions,
        version=version
    )
    if not os.path.exists(destination_root):
        shell.makedirs(path=destination_root)
    return destination_root


def compose_project(
    toolchain,
    arguments,
    host_system,
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

    host_system -- The system this script is run on.

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
        "-DCMAKE_BUILD_TYPE={}".format(arguments.build_variant),
        "-DCMAKE_C_COMPILER={}".format(toolchain.cc),
        "-DCMAKE_CXX_COMPILER={}".format(toolchain.cxx),
        "-DCMAKE_INSTALL_PREFIX={}".format(destination_root),
        "-DODE_BUILD_TEST={}".format("ON" if arguments.build_test else "OFF"),
        "-DODE_TEST_BENCHMARKING={}".format(
            "ON" if arguments.build_benchmark else "OFF"
        ),
        "-DODE_BUILD_STATIC={}".format(
            "ON" if arguments.build_ode_static_lib else "OFF"
        ),
        "-DODE_BUILD_SHARED={}".format(
            "ON" if arguments.build_ode_shared_lib else "OFF"
        ),
        "-DANTHEM_BUILD_STATIC={}".format(
            "ON" if arguments.build_anthem_static_lib else "OFF"
        ),
        "-DANTHEM_BUILD_SHARED={}".format(
            "ON" if arguments.build_anthem_shared_lib else "OFF"
        ),
        "-DODE_DEVELOPER={}".format(
            "ON" if arguments.developer_build else "OFF"
        ),
        "-DODE_CXX_VERSION={}".format(arguments.std),
        "-DODE_DEPENDENCY_PREFIX={}".format(dependencies_root),
        "-DODE_VERSION={}".format(arguments.ode_version),
        "-DANTHEM_VERSION={}".format(arguments.anthem_version),
        "-DODE_OPENGL_VERSION_MAJOR={}".format(
            arguments.opengl_version.split(".")[0]
        ),
        "-DODE_OPENGL_VERSION_MINOR={}".format(
            arguments.opengl_version.split(".")[1]
        ),
        "-DODE_LOGGER_NAME={}".format(arguments.ode_logger_name),
        "-DODE_WINDOW_NAME={}".format(arguments.ode_window_name),
        "-DANTHEM_LOGGER_NAME={}".format(arguments.anthem_logger_name),
        "-DANTHEM_WINDOW_NAME={}".format(arguments.anthem_window_name),
        "-DODE_NAME={}".format(arguments.ode_binaries_name),
        "-DANTHEM_NAME={}".format(arguments.anthem_binaries_name)
    ]

    if arguments.cmake_generator == get_ninja_cmake_generator_name():
        cmake_call.extend(
            ["-DCMAKE_MAKE_PROGRAM={}".format(toolchain.build_system)]
        )

    if host_system == get_darwin_system_name():
        cmake_call.extend(["-DODE_RPATH=@loader_path"])
    elif host_system == get_linux_system_name():
        cmake_call.extend(["-DODE_RPATH=$ORIGIN"])

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
