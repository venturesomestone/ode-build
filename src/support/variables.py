# ------------------------------------------------------------- #
#                 Obliging Ode & Unsung Anthem
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""This support module sets essential variables for the build."""

import os


# $HOME is got as an environment variable so it is set to the
# value it is expected to have.
HOME = os.environ.get("HOME", "/")


def _script_path():
    # Get the parent directory of this file for checking if this
    # file is in an Unsung Anthem checkout.
    #
    # $ANTHEM_SOURCE_ROOT/build/script/support/variables.py
    script_path = os.path.dirname(os.path.dirname(__file__))

    # Split the path as the first part of the 'script_path' is
    # likely the 'script' folder.
    build_path, parent_dirname = os.path.split(script_path)
    if parent_dirname != "script":
        return ""
    root_path = os.path.dirname(build_path)
    # The checkout has to have a CMake Listfile.
    if not os.path.exists(os.path.join(
            root_path, "unsung-anthem", "CMakeLists.txt")):
        return ""
    return script_path


def _get_default_source_root():
    return os.path.dirname(os.path.dirname(_script_path()))


# $ANTHEM_SOURCE_ROOT is got from the path of this file if the
# environment variable is not set.
ANTHEM_SOURCE_ROOT = os.environ.get(
    "ANTHEM_SOURCE_ROOT", _get_default_source_root())

# $ANTHEM_REPO_NAME is got from the default value if the
# environment variable is not set.
ANTHEM_REPO_NAME = os.environ.get("ANTHEM_REPO_NAME", "unsung-anthem")
