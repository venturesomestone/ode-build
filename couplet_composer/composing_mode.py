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

import logging
import os

from .support.cmake_generators import \
    get_ninja_cmake_generator_name, get_visual_studio_16_cmake_generator_name

from .support.environment import \
    get_build_root, get_composing_directory, get_destination_directory, \
    get_latest_install_path_file, get_latest_install_version_file, \
    get_relative_destination_directory, get_sdl_shared_data_file

from .support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from .util.target import parse_target_from_argument_string

from .util import shell


def create_composing_root(
    source_root,
    in_tree_build,
    target,
    cmake_generator,
    build_variant
):
    """
    Checks if the directory for the actual build of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    in_tree_build -- Whether the build files are created in-tree.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.
    """
    composing_root = get_composing_directory(
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=in_tree_build
        ),
        target=target,
        cmake_generator=cmake_generator,
        build_variant=build_variant
    )
    if not os.path.exists(composing_root):
        shell.makedirs(path=composing_root)
    return composing_root


def create_destination_root(
    source_root,
    in_tree_build,
    target,
    cmake_generator,
    build_variant,
    version
):
    """
    Checks if the directory for the built products of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    in_tree_build -- Whether the build files are created in-tree.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    destination_root = get_destination_directory(
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=in_tree_build
        ),
        target=target,
        cmake_generator=cmake_generator,
        build_variant=build_variant,
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
        "-DCMAKE_C_COMPILER={}".format(
            toolchain.compiler["cc"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        ),
        "-DCMAKE_CXX_COMPILER={}".format(
            toolchain.compiler["cxx"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        ),
        "-DCMAKE_INSTALL_PREFIX={}".format(
            destination_root.replace("\\", "/")
            if host_system == get_windows_system_name() else destination_root
        ),
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
        # TODO Maybe have some more sophisticated way to set this
        # option
        "-DODE_DISABLE_GL_CALLS={}".format(
            "ON" if host_system == get_linux_system_name() and os.getenv(
                "GITHUB_ACTIONS",
                None
            ) else "OFF"
        ),
        "-DODE_CXX_VERSION={}".format(arguments.std),
        "-DODE_DEPENDENCY_PREFIX={}".format(
            dependencies_root.replace("\\", "/")
            if host_system == get_windows_system_name() else dependencies_root
        ),
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

    if isinstance(toolchain.compiler, dict):
        cmake_env = {
            "CC": toolchain.compiler["cc"],
            "CXX": toolchain.compiler["cxx"]
        }
    else:
        cmake_env = {"CC": toolchain.compiler, "CXX": toolchain.compiler}

    with shell.pushd(composing_root):
        shell.call(
            cmake_call,
            env=cmake_env,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        if arguments.cmake_generator \
                == get_visual_studio_16_cmake_generator_name():
            logging.debug(
                "The build directory contains the following files and "
                "directories:\n%s",
                "\n".join([f for f in os.listdir(composing_root)])
            )
            shell.call(
                [
                    toolchain.build_system,
                    "anthem.sln",
                    "/property:Configuration={}".format(
                        arguments.build_variant
                    )
                ],
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        else:
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

    build_target = parse_target_from_argument_string(arguments.host_target)

    if host_system != get_windows_system_name():
        logging.debug(
            "Found the following SDL libraries:\n\n{}".format(
                "\n".join(
                    [f for f in os.listdir(os.path.join(
                        dependencies_root,
                        "lib"
                    )) if "libSDL" in f]
                )
            )
        )

    if host_system == get_darwin_system_name():
        sdl_dynamic_lib_name = "libSDL2-2.0.0.dylib"
        sdl_dynamic_lib = os.path.join(
            destination_root,
            "bin",
            sdl_dynamic_lib_name
        )
        if os.path.exists(sdl_dynamic_lib):
            shell.rm(
                sdl_dynamic_lib,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        shell.copy(
            os.path.join(dependencies_root, "lib", sdl_dynamic_lib_name),
            os.path.join(destination_root, "bin"),
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
    elif host_system == get_linux_system_name():
        def _copy_linux_sdl(name):
            dynamic_lib = os.path.join(destination_root, "bin", name)
            if os.path.exists(dynamic_lib):
                shell.rm(
                    dynamic_lib,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            shell.copy(
                os.path.join(dependencies_root, "lib", name),
                os.path.join(destination_root, "bin"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

        shared_version_file = get_sdl_shared_data_file(
            build_root=build_root,
            target=build_target,
            build_variant=arguments.build_variant
        )
        if os.path.exists(shared_version_file):
            with open(shared_version_file) as f:
                shared_version = f.read()
        else:
            shared_version = "0.0.0"

        version_data = shared_version.split(".")

        _copy_linux_sdl("libSDL2-2.0.so.{}".format(shared_version))

        def _link_linux_sdl(name, src):
            new_link = os.path.join(destination_root, "bin", name)
            if os.path.exists(new_link):
                shell.rm(
                    new_link,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            original = os.path.join(destination_root, "bin", src)
            shell.link(
                original,
                new_link,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

        _link_linux_sdl(
            name="libSDL2-2.0.so.{}".format(version_data[0]),
            src="libSDL2-2.0.so.{}".format(shared_version)
        )
        _link_linux_sdl(
            name="libSDL2-2.0.so",
            src="libSDL2-2.0.so.{}".format(version_data[0])
        )
        _link_linux_sdl(name="libSDL2.so", src="libSDL2-2.0.so")

    latest_path_file = get_latest_install_path_file(build_root=build_root)

    if os.path.exists(latest_path_file):
        shell.rm(latest_path_file)

    with open(latest_path_file, "w") as f:
        f.write(str(get_relative_destination_directory(
            target=build_target,
            cmake_generator=arguments.cmake_generator,
            build_variant=arguments.build_variant,
            version=arguments.anthem_version)
        ))

    latest_version_file = get_latest_install_version_file(
        build_root=build_root
    )

    if os.path.exists(latest_version_file):
        shell.rm(latest_version_file)

    with open(latest_version_file, "w") as f:
        f.write(arguments.anthem_version)
