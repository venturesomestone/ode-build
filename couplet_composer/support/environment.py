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
def get_build_root(source_root, in_tree_build):
    """
    Gives the path to the root directory that this script uses
    for all created files and directories.

    source_root -- Path to the directory that is the root of the
    script run.

    in_tree_build -- Whether the build files are created in-tree.
    """
    return os.path.join(source_root, "build") if not in_tree_build \
        else os.path.join(source_root, "unsung-anthem", "build")


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
            cmake_generator.replace(" ", "_")
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
def get_relative_artifact_directory(target, build_variant, version):
    """
    Gives the path to the directory where the built project
    artifacts are placed relative to the build root.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    return os.path.join(
        "artifacts",
        version,
        "{}-{}-{}".format(target.system, target.machine, build_variant)
    )


@cached
def get_artifact_directory(build_root, target, build_variant, version):
    """
    Gives the path to the directory where the built project
    artifacts are placed.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    return os.path.join(
        build_root,
        get_relative_artifact_directory(
            target=target,
            build_variant=build_variant,
            version=version
        )
    )


@cached
def get_relative_running_directory(target, build_variant, version):
    """
    Gives the path to the directory where the built project is
    placed relative to the build root for running it.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    return os.path.join(
        "run",
        version,
        "{}-{}-{}".format(target.system, target.machine, build_variant)
    )


@cached
def get_running_directory(build_root, target, build_variant, version):
    """
    Gives the path to the directory where the built project is
    placed for running it.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    return os.path.join(
        build_root,
        get_relative_running_directory(
            target=target,
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
        "local",
        "bin",
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
        "local",
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
        "local",
        "versions-{}-{}-{}".format(
            target.system,
            target.machine,
            build_variant
        )
    )


@cached
def get_data_directory(build_root, target, build_variant):
    """
    Gives the path to the directory in the build directory that
    contains helpful data files for the build process.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.
    """
    return os.path.join(
        build_root,
        "local",
        "data",
        "{}-{}-{}".format(target.system, target.machine, build_variant)
    )


@cached
def get_sdl_shared_data_file(build_root, target, build_variant):
    """
    Gives path to the file in the build directory containing
    the version of the installed shared SDL library.

    build_root -- Path to the directory that is the root of the
    script build files.

    target -- The target system of the build represented by a
    Target.

    build_variant -- The build variant used to build the project.
    """
    return os.path.join(
        get_data_directory(
            build_root=build_root,
            target=target,
            build_variant=build_variant
        ),
        "linux-shared-sdl"
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
def get_latest_running_path_file(build_root):
    """
    Gives path to the file in the build directory containing
    relative path to directory for running the most recently
    built products to automatically run tests on them on
    e.g. continuous integration.

    build_root -- Path to the directory that is the root of the
    script build files.
    """
    return os.path.join(build_root, "latest-install-for-running")


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
