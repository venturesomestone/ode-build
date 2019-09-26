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


"""This support module sets essential variables for the build."""

import json
import os

from .values import DEFAULTS_FILE_PATH


# $HOME is got as an environment variable so it is set to the
# value it is expected to have.
HOME = os.environ.get("HOME", "/")


def _get_default_source_root():
    # The script assumes the build is run with source root as the
    # working directory.
    working_directory = os.getcwd()

    # The checkout has to have a CMake Listfile.
    if not os.path.exists(
        os.path.join(working_directory, "unsung-anthem", "CMakeLists.txt")
    ):
        return ""
    return working_directory


# $ODE_SOURCE_ROOT is got from the working directory if the
# environment variable is not set.
ODE_SOURCE_ROOT = os.environ.get(
    "ODE_SOURCE_ROOT",
    _get_default_source_root()
)

# $ODE_BUILD_ROOT is resolved from $ODE_SOURCE_ROOT if the environment
# variable is not set.
ODE_BUILD_ROOT = os.environ.get(
    "ODE_BUILD_ROOT",
    os.path.join(ODE_SOURCE_ROOT, "build")
)

# $ODE_GRAPHQL_ROOT is resolved from $ODE_BUILD_ROOT if the environment
# variable is not set.
ODE_GRAPHQL_ROOT = os.environ.get(
    "ODE_GRAPHQL_ROOT",
    os.path.join(ODE_BUILD_ROOT, "graphql")
)

# $ODE_REPO_NAME is got from the default value if the environment
# variable is not set.
ODE_REPO_NAME = os.environ.get("ODE_REPO_NAME", "unsung-anthem")

# The download directory in the build root is the directory where
# the dependencies needed to build the project are downloaded to.
DOWNLOAD_DIR = os.path.join(ODE_BUILD_ROOT, "shared")

# The download status file is a JSON file containing the versions
# of the dependencies in order to determine whether to download
# new versions of them.
DOWNLOAD_STATUS_FILE = os.path.join(DOWNLOAD_DIR, "status")


# Get the default values for the names of the projects from the
# project repository.
def _get_defaults():
    with open(
        os.path.join(ODE_SOURCE_ROOT, ODE_REPO_NAME, DEFAULTS_FILE_PATH)
    ) as f:
        return json.load(f)


ODE_NAME = os.environ.get("ODE_NAME", _get_defaults()["ode"]["name"])

ANTHEM_NAME = os.environ.get("ANTHEM_NAME", _get_defaults()["anthem"]["name"])
