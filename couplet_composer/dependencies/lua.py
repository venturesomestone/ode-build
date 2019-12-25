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
This support module contains the functions related to the
building and finding Lua.
"""

import os
import sys

from ..github import tag

from ..support.cmake_generators import get_make_cmake_generator_name

from ..support.environment import get_temporary_directory

from ..support.github_data import GitHubData

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.build_util import build_with_cmake

from ..util.cache import cached

from ..util import http, shell


def _build_with_make(
    toolchain,
    dependencies_root,
    host_system,
    dry_run,
    print_debug
):
    """
    Builds Lua by using the Makefile provided with the source
    code.

    toolchain -- The toolchain object of the run.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    host_system -- The system this script is run on.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    make_call = [toolchain.build_system]
    if host_system == get_darwin_system_name():
        make_call.extend(["macosx"])
    elif host_system == get_linux_system_name():
        make_call.extend(["macosx"])
    shell.call(make_call, dry_run=dry_run, echo=print_debug)
    make_install_call = [
        toolchain.build_system,
        "install",
        "INSTALL_TOP={}".format(dependencies_root)
    ]
    shell.call(make_install_call, dry_run=dry_run, echo=print_debug)


def _create_cxx_header(dependencies_root, dry_run, print_debug):
    """
    Creates the Lua header for C++.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    if not os.path.isdir(os.path.join(dependencies_root, "include")):
        shell.makedirs(
            os.path.join(dependencies_root, "include"),
            dry_run=dry_run,
            echo=print_debug
        )
    cxx_header = os.path.join(dependencies_root, "include", "lua.hpp")
    if os.path.exists(cxx_header):
        shell.rm(cxx_header, dry_run=dry_run, echo=print_debug)
    with open(cxx_header, "w+") as outfile:
        outfile.write("// lua.hpp\n")
        outfile.write("// Lua header files for C++\n")
        outfile.write(
            "// <<extern \"C\">> not supplied automatically because Lua also "
            "compiles as C++\n"
        )
        outfile.write("\n")
        outfile.write("extern \"C\" {\n")
        outfile.write("#include \"lua.h\"\n")
        outfile.write("#include \"lualib.h\"\n")
        outfile.write("#include \"lauxlib.h\"\n")
        outfile.write("}\n")
        outfile.write("")


################################################################
# DEPENDENCY DATA FUNCTIONS
################################################################


@cached
def should_install(
    dependencies_root,
    version,
    target,
    host_system,
    installed_version
):
    """
    Tells whether the build of the dependency should be skipped.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    version -- The full version number of the dependency.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    installed_version -- The version of the dependecy that is
    written to the JSON file containing the currently installed
    versions of the dependencies.
    """
    if not installed_version or version != installed_version:
        return True

    if host_system == get_windows_system_name():
        return not os.path.exists(
            os.path.join(dependencies_root, "lib", "lua.lib")
        )
    else:
        return not os.path.exists(
            os.path.join(dependencies_root, "lib", "liblua.a")
        )


def install_dependency(
    toolchain,
    cmake_generator,
    build_root,
    dependencies_root,
    version,
    target,
    host_system,
    build_variant,
    github_user_agent,
    github_api_token,
    opengl_version,
    dry_run=None,
    print_debug=None
):
    """
    Installs the dependency by downloading and possibly building
    it. Returns the path to the built dependency.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    version -- The full version number of the dependency.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    build_variant -- The build variant used to build the project.

    github_user_agent -- The user agent used when accessing the
    GitHub API.

    github_api_token -- The GitHub API token that is used to
    access the API.

    opengl_version -- The version of OpenGL that is used.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    temp_dir = get_temporary_directory(build_root=build_root)
    dependency_temp_dir = os.path.join(temp_dir, "lua")

    shell.makedirs(temp_dir, dry_run=dry_run, echo=print_debug)
    shell.makedirs(dependency_temp_dir, dry_run=dry_run, echo=print_debug)

    url = "https://www.lua.org/ftp/lua-{version}.tar.gz".format(
        version=version
    )
    dest = os.path.join(dependency_temp_dir, "lua.tar.gz")

    http.stream(
        url=url,
        destination=dest,
        host_system=host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )
    shell.tar(dest, dependency_temp_dir, dry_run=dry_run, echo=print_debug)

    subdir = os.path.join(dependency_temp_dir, "lua-{}".format(version))

    with shell.pushd(subdir, dry_run=dry_run, echo=print_debug):
        if cmake_generator == get_make_cmake_generator_name() \
                and host_system != get_windows_system_name():
            _build_with_make(
                toolchain=toolchain,
                dependencies_root=dependencies_root,
                host_system=host_system,
                dry_run=dry_run,
                print_debug=print_debug
            )
        else:
            shell.copy(
                os.path.join(
                    os.path.dirname(__file__),
                    "lua",
                    "CMakeLists.txt"
                ),
                os.path.join(subdir, "CMakeLists.txt"),
                dry_run=dry_run,
                echo=print_debug
            )
            build_with_cmake(
                toolchain=toolchain,
                cmake_generator=cmake_generator,
                source_directory=subdir,
                temporary_root=temp_dir,
                dependencies_root=dependencies_root,
                target=target,
                host_system=host_system,
                build_variant=build_variant,
                do_install=host_system != get_windows_system_name(),
                dry_run=dry_run,
                print_debug=print_debug
            )
            _create_cxx_header(
                dependencies_root=dependencies_root,
                dry_run=dry_run,
                print_debug=print_debug
            )
            if host_system == get_windows_system_name():
                build_dir = os.path.join(temp_dir, "build")
                if not os.path.isdir(os.path.join(dependencies_root, "lib")):
                    shell.makedirs(
                        os.path.join(dependencies_root, "lib"),
                        dry_run=dry_run,
                        echo=print_debug
                    )
                lib_file = os.path.join(dependencies_root, "lib", "lua.lib")
                if os.path.exists(lib_file):
                    shell.rm(lib_file, dry_run=dry_run, echo=print_debug)
                shell.copy(
                    os.path.join(build_dir, "Debug", "lua.lib"),
                    lib_file,
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.rm(
                    os.path.join(dependencies_root, "include", "lua.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.rm(
                    os.path.join(dependencies_root, "include", "lualib.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.rm(
                    os.path.join(dependencies_root, "include", "lauxlib.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.rm(
                    os.path.join(dependencies_root, "include", "luaconf.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.copy(
                    os.path.join(dependency_temp_dir, "src", "lua.h"),
                    os.path.join(dependencies_root, "include", "lua.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.copy(
                    os.path.join(dependency_temp_dir, "src", "lualib.h"),
                    os.path.join(dependencies_root, "include", "lualib.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.copy(
                    os.path.join(dependency_temp_dir, "src", "lauxlib.h"),
                    os.path.join(dependencies_root, "include", "lauxlib.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )
                shell.copy(
                    os.path.join(dependency_temp_dir, "src", "luaconf.h"),
                    os.path.join(dependencies_root, "include", "luaconf.h"),
                    dry_run=dry_run,
                    echo=print_debug
                )

    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)
