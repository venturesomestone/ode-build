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

import json
import logging
import os

from .dependencies import googletest

from .support.cmake_generators import \
    get_ninja_cmake_generator_name, get_visual_studio_16_cmake_generator_name

from .support.environment import \
    get_artefact_directory, get_build_root, get_composing_directory, \
    get_destination_directory, get_project_root, get_running_directory, \
    get_temporary_directory

from .support.file_paths import get_project_dependencies_file_path

from .support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

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
    source_root,
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

    source_root -- Path to the directory that is the root of the
    script run.

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
        "-DCMAKE_INSTALL_PREFIX={}".format(
            destination_root.replace("\\", "/")
            if host_system == get_windows_system_name() else destination_root
        ),
        "-DODE_BUILD_TEST={}".format("ON" if arguments.build_test else "OFF"),
        "-DODE_TEST_BENCHMARKING={}".format(
            "ON" if arguments.build_benchmark else "OFF"
        ),
        "-DODE_BUILD_DOCS={}".format("ON" if arguments.build_docs else "OFF"),
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
        "-DODE_TEST_USE_NULL_SINK={}".format(
            "ON" if not arguments.test_logging else "OFF"
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

    if host_system != get_windows_system_name():
        cmake_call.extend(["-DCMAKE_C_COMPILER={}".format(
            toolchain.compiler["cc"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        )])
        cmake_call.extend(["-DCMAKE_CXX_COMPILER={}".format(
            toolchain.compiler["cxx"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        )])

    if arguments.cmake_generator == get_ninja_cmake_generator_name():
        cmake_call.extend(
            ["-DCMAKE_MAKE_PROGRAM={}".format(toolchain.build_system)]
        )

    if host_system == get_darwin_system_name():
        cmake_call.extend(["-DODE_RPATH=@loader_path"])
    elif host_system == get_linux_system_name():
        cmake_call.extend(["-DODE_RPATH=$ORIGIN"])

    if host_system == get_windows_system_name():
        if os.path.exists(os.path.join(dependencies_root, "lib", "SDL2d.lib")):
            cmake_call.extend(["-DODE_USE_SDL_DEBUG_SUFFIX=ON"])
        else:
            cmake_call.extend(["-DODE_USE_SDL_DEBUG_SUFFIX=OFF"])

    if googletest.should_add_sources_to_project(host_system=host_system):
        cmake_call.extend(["-DODE_ADD_GOOGLE_TEST_SOURCE=ON"])
        cmake_call.extend(["-DODE_GOOGLE_TEST_DIRECTORY={}".format(
            googletest.get_dependency_source_directory(
                dependencies_root=dependencies_root
            )
        )])
    else:
        cmake_call.extend(["-DODE_ADD_GOOGLE_TEST_SOURCE=OFF"])

    # if host_system == get_windows_system_name():
    #     cmake_call.extend(["-DODE_MSVC_RUNTIME_LIBRARY=MultiThreadedDebug"])

    if host_system != get_windows_system_name():
        if isinstance(toolchain.compiler, dict):
            cmake_env = {
                "CC": toolchain.compiler["cc"],
                "CXX": toolchain.compiler["cxx"]
            }
        else:
            cmake_env = {"CC": toolchain.compiler, "CXX": toolchain.compiler}
    else:
        cmake_env = None

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
            anthem_executable_name = "{}.exe".format(
                arguments.anthem_binaries_name
            )
            anthem_executable = os.path.join(
                destination_root,
                "bin",
                anthem_executable_name
            )
            if os.path.exists(anthem_executable):
                shell.rm(
                    anthem_executable,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            test_executable_name = "test-{}.exe".format(
                arguments.anthem_binaries_name
            )
            test_executable = os.path.join(
                destination_root,
                "bin",
                test_executable_name
            )
            if os.path.exists(test_executable):
                shell.rm(
                    test_executable,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            shell.makedirs(
                os.path.join(destination_root, "bin"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.copy(
                os.path.join(
                    composing_root,
                    arguments.build_variant,
                    anthem_executable_name
                ),
                anthem_executable,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.copy(
                os.path.join(
                    composing_root,
                    arguments.build_variant,
                    test_executable_name
                ),
                test_executable,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

            script_dest_dir = os.path.join(destination_root, "lib")

            if os.path.exists(script_dest_dir):
                shell.rmtree(
                    script_dest_dir,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )

            shell.makedirs(
                script_dest_dir,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

            shell.copytree(
                os.path.join(project_root, "script", "anthem"),
                os.path.join(script_dest_dir, "anthem"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.copytree(
                os.path.join(project_root, "script", "ode"),
                os.path.join(script_dest_dir, "ode"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.copytree(
                os.path.join(project_root, "script", "test", "anthem"),
                os.path.join(script_dest_dir, "anthem"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.copytree(
                os.path.join(project_root, "script", "test", "ode"),
                os.path.join(script_dest_dir, "ode"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

            lua_scripts = []

            for dirpath, dirnames, filenames in os.walk(script_dest_dir):
                for filename in filenames:
                    if filename == "CMakeLists.txt":
                        shell.rm(
                            os.path.join(dirpath, filename),
                            dry_run=arguments.dry_run,
                            echo=arguments.print_debug
                        )
                    else:
                        lua_scripts.append(os.path.join(dirpath, filename))

            logging.debug("The Lua scripts are:\n\n%s", "\n".join(lua_scripts))
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

        dependency_version_file = os.path.join(
            get_project_root(source_root=source_root),
            get_project_dependencies_file_path()
        )
        with open(dependency_version_file) as f:
            sdl_version = json.load(f)["sdl"]["version"]

        sdl_major, sdl_minor, sdl_patch = sdl_version.split(".")

        _copy_linux_sdl("libSDL2-2.0.so.{}.{}.0".format(sdl_minor, sdl_patch))

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
            name="libSDL2-2.0.so.{}".format(sdl_major),
            src="libSDL2-2.0.so.{}.{}.0".format(sdl_minor, sdl_patch)
        )
        _link_linux_sdl(
            name="libSDL2-2.0.so",
            src="libSDL2-2.0.so.{}".format(sdl_major)
        )
        _link_linux_sdl(name="libSDL2.so", src="libSDL2-2.0.so")
    elif host_system == get_windows_system_name():
        sdl_dynamic_lib_name = "SDL2.dll"
        sdl_dynamic_lib_d_name = "SDL2d.dll"
        sdl_dynamic_lib = os.path.join(
            destination_root,
            "bin",
            sdl_dynamic_lib_name
        )
        sdl_dynamic_lib_d = os.path.join(
            destination_root,
            "bin",
            sdl_dynamic_lib_d_name
        )
        if os.path.exists(sdl_dynamic_lib):
            shell.rm(
                sdl_dynamic_lib,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        if os.path.exists(sdl_dynamic_lib_d):
            shell.rm(
                sdl_dynamic_lib_d,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        if os.path.exists(
            os.path.join(dependencies_root, "lib", sdl_dynamic_lib_name)
        ):
            shell.copy(
                os.path.join(dependencies_root, "lib", sdl_dynamic_lib_name),
                os.path.join(destination_root, "bin"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        elif os.path.exists(
            os.path.join(dependencies_root, "lib", sdl_dynamic_lib_d_name)
        ):
            shell.copy(
                os.path.join(dependencies_root, "lib", sdl_dynamic_lib_d_name),
                os.path.join(destination_root, "bin"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        else:
            logging.debug("No dynamic SDL library was found for Windows")


def install_running_copies(arguments, build_root, destination_root):
    """
    Installs the built products to the running directories.

    arguments -- The parsed command line arguments of the run.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    destination_root -- The directory where the built product is
    placed in.
    """
    running_path = get_running_directory(build_root=build_root)

    if os.path.exists(running_path):
        shell.rmtree(
            running_path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.makedirs(
        running_path,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(destination_root, "bin"),
        running_path,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.makedirs(
        os.path.join(running_path, "lib"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(destination_root, "lib"),
        os.path.join(running_path, "lib"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )


def create_artefacts(arguments, host_system, build_root):
    """
    Creates the artefacts of the built products.

    arguments -- The parsed command line arguments of the run.

    host_system -- The system this script is run on.

    build_root -- The path to the root directory that is used for
    all created files and directories.
    """
    artefact_name = "{}-{}-{}.{}".format(
        arguments.anthem_artefacts_name,
        arguments.anthem_version,
        arguments.host_target,
        "zip" if host_system == get_windows_system_name() else "tar.gz"
    )
    artefact_dir = get_artefact_directory(build_root=build_root)
    artefact_path = os.path.join(artefact_dir, artefact_name)

    if os.path.exists(artefact_path):
        shell.rm(
            artefact_path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.makedirs(
        artefact_dir,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    tmp_dir = get_temporary_directory(build_root=build_root)
    tmp_subdir = "{}-{}-{}".format(
        arguments.anthem_artefacts_name,
        arguments.anthem_version,
        arguments.host_target
    )

    if os.path.exists(tmp_dir):
        shell.rmtree(
            tmp_dir,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.makedirs(
        tmp_dir,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.makedirs(
        os.path.join(tmp_dir, tmp_subdir),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    running_path = get_running_directory(build_root=build_root)

    shell.copytree(
        running_path,
        os.path.join(tmp_dir, tmp_subdir),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    if host_system == get_windows_system_name():
        shell.create_zip(
            os.path.join(tmp_dir, tmp_subdir),
            artefact_path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
    else:
        shell.create_tar(
            os.path.join(tmp_dir, tmp_subdir),
            artefact_path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.rmtree(
        tmp_dir,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
