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
def get_build_root(source_root):
    """
    Gives the path to the root directory that this script uses
    for all created files and directories.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return os.path.join(source_root, "build")


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
