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

"""This support module resolves the build environment values."""

import os

from ..util.cache import cached


def is_path_source_root(path):
    """
    Checks if the given path is valid source root for the script.

    path -- The path that is to be checked.
    """
    # The checkout has to have a CMake Listfile.
    return os.path.exists(
        os.path.join(path, "unsung-anthem", "CMakeLists.txt")
    )


@cached
def get_project_root(source_root):
    """
    Gives the path to the root directory of the project this
    script acts on.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return os.path.join(source_root, "unsung-anthem")


@cached
def get_build_root(source_root):
    """
    Gives the path to the root directory that this script uses
    for all created files and directories.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return os.path.join(source_root, "build")


@cached
def get_composing_directory(
    build_root,
    target,
    cmake_generator,
    build_variant
):
    """
    Gives the path to the directory in the build directory that
    is used for the build of the project.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.
    """
    return os.path.join(
        build_root,
        "build",
        "{}-{}-{}-{}".format(
            target.system,
            target.machine,
            build_variant,
            cmake_generator
        )
    )


@cached
def get_relative_destination_directory(
    target,
    cmake_generator,
    build_variant,
    version
):
    """
    Gives the path to the directory where the built project is
    placed relative to the build root.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    return os.path.join(
        "dest",
        version,
        "{}-{}-{}-{}".format(
            target.system,
            target.machine,
            build_variant,
            cmake_generator.replace(" ", "_")
        )
    )


@cached
def get_destination_directory(
    build_root,
    target,
    cmake_generator,
    build_variant,
    version
):
    """
    Gives the path to the directory where the built project is
    placed.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    return os.path.join(
        build_root,
        get_relative_destination_directory(
            target=target,
            cmake_generator=cmake_generator,
            build_variant=build_variant,
            version=version
        )
    )


@cached
def get_tools_directory(build_root, target):
    """
    Gives the path to the directory in the build directory that
    this script uses for all local tools.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.
    """
    return os.path.join(
        build_root,
        "tools",
        "{}-{}".format(target.system, target.machine)
    )


@cached
def get_dependencies_directory(build_root, target, build_variant):
    """
    Gives the path to the directory in the build directory that
    this script uses for all local tools.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.
    """
    return os.path.join(
        build_root,
        "lib",
        "{}-{}-{}".format(target.system, target.machine, build_variant)
    )


@cached
def get_dependency_version_data_file(build_root, target, build_variant):
    """
    Gives path to the file in the build directory containing the
    currently installed versions of the dependencies.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.
    """
    return os.path.join(
        build_root,
        "versions-{}-{}-{}".format(
            target.system,
            target.machine,
            build_variant
        )
    )


@cached
def get_latest_install_path_file(build_root):
    """
    Gives path to the file in the build directory containing
    relative path to the most recently built products to
    automatically run tests on them on e.g. continuous
    integration.

    build_root -- Path to the directory that is the root of the
    script build files.
    """
    return os.path.join(build_root, "latest-install")


@cached
def get_latest_install_version_file(build_root):
    """
    Gives path to the file in the build directory containing
    the version of the most recently built products to
    automatically run tests on them on e.g. continuous
    integration.

    build_root -- Path to the directory that is the root of the
    script build files.
    """
    return os.path.join(build_root, "latest-install-version")


@cached
def get_temporary_directory(build_root):
    """
    Gives the path to the temporary directory in the build
    directory that this script uses for all files that are not
    permanent, for example when installing dependencies.

    build_root -- Path to the directory that is the root of the
    script build files.
    """
    return os.path.join(build_root, "tmp")
