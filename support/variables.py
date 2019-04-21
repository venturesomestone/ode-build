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
    # In stack development mode:
    # $ODE_SOURCE_ROOT/build/script/support/variables.py
    return os.path.dirname(os.path.dirname(__file__))


def _get_default_source_root():
    script_path = _script_path()

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
    return os.path.dirname(os.path.dirname(script_path))


# $ODE_SCRIPT_ROOT is got from the path of this file if the
# environment variable is not set.
ODE_SCRIPT_ROOT = os.environ.get("ODE_SCRIPT_ROOT", _script_path())


# $ODE_SOURCE_ROOT is got from the path of this file if the
# environment variable is not set.
ODE_SOURCE_ROOT = os.environ.get(
    "ODE_SOURCE_ROOT", _get_default_source_root())

# $ODE_BUILD_ROOT is resolved from $ODE_SOURCE_ROOT if the environment
# variable is not set.
ODE_BUILD_ROOT = os.environ.get("ODE_BUILD_ROOT", os.path.join(
    ODE_SOURCE_ROOT, "build"))

# $ODE_GRAPHQL_ROOT is resolved from $ODE_BUILD_ROOT if the environment
# variable is not set.
ODE_GRAPHQL_ROOT = os.environ.get("ODE_GRAPHQL_ROOT", os.path.join(
    ODE_BUILD_ROOT, "graphql"))

# $ODE_REPO_NAME is got from the default value if the environment
# variable is not set.
ODE_REPO_NAME = os.environ.get("ODE_REPO_NAME", "unsung-anthem")
