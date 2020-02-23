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
building and finding Simple DirectMedia Layer.
"""

import os

from ..github import release

from ..support.cmake_generators import \
    get_visual_studio_16_cmake_generator_name

from ..support.environment import \
    get_data_directory, get_sdl_shared_data_file, get_temporary_directory

from ..support.github_data import GitHubData

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.build_util import build_with_cmake

from ..util.cache import cached

from ..util import http, shell


def _copy_visual_c_binaries(
    dependencies_root,
    subdirectory,
    dry_run=None,
    print_debug=None
):
    """
    Copies the pre-built binaries for Visual C on Windows.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    subdirectory -- The temporary directory where the SDL files
    are located.

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
    include_dir = os.path.join(dependencies_root, "include", "SDL2")
    if os.path.isdir(include_dir):
        shell.rmtree(include_dir, dry_run=dry_run, echo=print_debug)
    shell.copytree(
        os.path.join(subdirectory, "include"),
        include_dir,
        dry_run=dry_run,
        echo=print_debug
    )
    if not os.path.isdir(os.path.join(dependencies_root, "lib")):
        shell.makedirs(
            os.path.join(dependencies_root, "lib"),
            dry_run=dry_run,
            echo=print_debug
        )
    for lib_file in os.listdir(os.path.join(
        dependencies_root,
        "lib"
    )):
        if "SDL" in lib_file:
            shell.rm(
                os.path.join(dependencies_root, "lib", lib_file),
                dry_run=dry_run,
                echo=print_debug
            )
    for lib_file in os.listdir(os.path.join(subdirectory, "lib", "x64")):
        shell.copy(
            os.path.join(subdirectory, "lib", "x64", lib_file),
            os.path.join(dependencies_root, "lib", lib_file),
            dry_run=dry_run,
            echo=print_debug
        )


def _build_using_cmake(
    toolchain,
    cmake_generator,
    dependencies_root,
    temporary_directory,
    subdirectory,
    target,
    host_system,
    build_variant,
    dry_run=None,
    print_debug=None
):
    """
    Builds SDL using CMake.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    temporary_directory -- The temporary directory used for
    downloading and building SDL.

    subdirectory -- The temporary directory where the SDL files
    are located.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    build_variant -- The build variant used to build the project.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    build_with_cmake(
        toolchain=toolchain,
        cmake_generator=cmake_generator,
        source_directory=subdirectory,
        temporary_root=temporary_directory,
        dependencies_root=dependencies_root,
        target=target,
        host_system=host_system,
        build_variant=build_variant,
        msbuild_target="ALL_BUILD.vcxproj",
        dry_run=dry_run,
        print_debug=print_debug
    )

    if cmake_generator == get_visual_studio_16_cmake_generator_name():
        if not os.path.isdir(os.path.join(dependencies_root, "lib")):
            shell.makedirs(
                os.path.join(dependencies_root, "lib"),
                dry_run=dry_run,
                echo=print_debug
            )
        lib_file = os.path.join(dependencies_root, "lib", "SDL2.lib")
        main_lib_file = os.path.join(dependencies_root, "lib", "SDL2main.lib")
        if os.path.exists(lib_file):
            shell.rm(lib_file, dry_run=dry_run, echo=print_debug)
        if os.path.exists(main_lib_file):
            shell.rm(main_lib_file, dry_run=dry_run, echo=print_debug)
        shell.copy(
            os.path.join(
                temporary_directory,
                "build",
                build_variant,
                "SDL2.lib"
            ),
            lib_file,
            dry_run=dry_run,
            echo=print_debug
        )
        shell.copy(
            os.path.join(
                temporary_directory,
                "build",
                build_variant,
                "SDL2main.lib"
            ),
            main_lib_file,
            dry_run=dry_run,
            echo=print_debug
        )
        if not os.path.isdir(
            os.path.join(dependencies_root, "include", "SDL2")
        ):
            shell.makedirs(
                os.path.join(dependencies_root, "include", "SDL2"),
                dry_run=dry_run,
                echo=print_debug
            )
        shell.copytree(
            os.path.join(subdirectory, "include"),
            os.path.join(dependencies_root, "include", "SDL2"),
            dry_run=dry_run,
            echo=print_debug
        )


def _build(
    toolchain,
    dependencies_root,
    temporary_directory,
    subdirectory,
    dry_run=None,
    print_debug=None
):
    """
    Builds SDL using the build scripts supplied with it.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    temporary_directory -- The temporary directory used for
    downloading and building SDL.

    subdirectory -- The temporary directory where the SDL files
    are located.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    config_call = [
        os.path.join(subdirectory, "configure"),
        "--prefix={}".format(dependencies_root)
    ]

    build_directory = os.path.join(temporary_directory, "build")

    shell.makedirs(build_directory, dry_run=dry_run, echo=print_debug)

    with shell.pushd(build_directory):
        shell.call(config_call, dry_run=dry_run, echo=print_debug)
        shell.call([toolchain.make], dry_run=dry_run, echo=print_debug)
        shell.call(
            [toolchain.make, "install"],
            dry_run=dry_run,
            echo=print_debug
        )


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
        return not os.path.exists(os.path.join(
            dependencies_root,
            "lib",
            "SDL2.lib"
        ))
    else:
        return not os.path.exists(os.path.join(
            dependencies_root,
            "lib",
            "libSDL2.a"
        )) and not os.path.exists(os.path.join(
            dependencies_root,
            "lib",
            "libSDL2d.a"
        ))


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
    dependency_temp_dir = os.path.join(temp_dir, "sdl")

    shell.makedirs(temp_dir, dry_run=dry_run, echo=print_debug)
    shell.makedirs(dependency_temp_dir, dry_run=dry_run, echo=print_debug)

    url = ("https://www.libsdl.org/release/SDL2-{version}.zip"
           if host_system == get_windows_system_name()
           else "https://www.libsdl.org/release/SDL2-{version}.tar.gz").format(
        version=version
    )
    # url = ("https://www.libsdl.org/release/SDL2-devel-{version}-VC.zip"
    #        if host_system == get_windows_system_name()
    #        else "https://www.libsdl.org/release/SDL2-{version}.tar.gz").format(
    #     version=version
    # )
    dest = os.path.join(
        dependency_temp_dir,
        "sdl.zip" if host_system == get_windows_system_name() else "sdl.tar.gz"
    )

    http.stream(
        url=url,
        destination=dest,
        host_system=host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )
    shell.tar(dest, dependency_temp_dir, dry_run=dry_run, echo=print_debug)

    subdir = os.path.join(dependency_temp_dir, "SDL2-{}".format(version))

    if host_system == get_windows_system_name():
        # _copy_visual_c_binaries(
        #     dependencies_root=dependencies_root,
        #     subdirectory=subdir,
        #     dry_run=dry_run,
        #     print_debug=print_debug
        # )
        _build_using_cmake(
            toolchain=toolchain,
            cmake_generator=cmake_generator,
            dependencies_root=dependencies_root,
            temporary_directory=temp_dir,
            subdirectory=subdir,
            target=target,
            host_system=host_system,
            build_variant=build_variant,
            dry_run=dry_run,
            print_debug=print_debug
        )
    else:
        _build(
            toolchain=toolchain,
            dependencies_root=dependencies_root,
            temporary_directory=temp_dir,
            subdirectory=subdir,
            dry_run=dry_run,
            print_debug=print_debug
        )

    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)

    # Linux requires to use the correct version of the shared SDL
    # library
    if host_system == get_linux_system_name():
        data_file = get_sdl_shared_data_file(
            build_root=build_root,
            target=target,
            build_variant=build_variant
        )
        if os.path.exists(data_file):
            shell.rm(data_file, dry_run=dry_run, echo=print_debug)
        data_dir = get_data_directory(
            build_root=build_root,
            target=target,
            build_variant=build_variant
        )
        shell.makedirs(data_dir, dry_run=dry_run, echo=print_debug)
        (_, minor, patch) = version.split(".")
        with open(data_file, "w") as f:
            f.write("{}.{}.0".format(minor, patch))
