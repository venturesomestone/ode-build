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


def is_path_source_root(path):
    """
    Checks if the given path is valid source root for the script.

    path        The path that is to be checked.
    """
    # The checkout has to have a CMake Listfile.
    return os.path.exists(
        os.path.join(path, "unsung-anthem", "CMakeLists.txt")
    )
