# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""This support module has the default values of the build."""

import json
import os

from util.mapping import Mapping

from .variables import ODE_REPO_NAME, ODE_SOURCE_ROOT


__all__ = [
    # Command line configurable
    "BUILD_VARIANT",
    "CMAKE_GENERATOR",
    "ODE_VERSION",
    "ANTHEM_VERSION",
    "ODE_NAME",
    "ANTHEM_NAME",

    # Constants
    "PROTOCOL",
    "GITHUB_API_V4_ENDPOINT"
]


def _get_defaults():
    with open(os.path.join(
        ODE_SOURCE_ROOT,
        ODE_REPO_NAME,
        "util",
        "composer",
        "defaults.json"
    )) as f:
        return json.load(f)


def _get_dependencies():
    with open(os.path.join(
        ODE_SOURCE_ROOT,
        ODE_REPO_NAME,
        "util",
        "composer",
        "dependencies.json"
    )) as f:
        return json.load(f)


# Options that can be "configured" by command line options

BUILD_VARIANT = _get_defaults()["build_variant"]
CMAKE_GENERATOR = _get_defaults()["cmake_generator"]

CXX_STANDARD = _get_defaults()["cxx_standard"]

ODE_VERSION = _get_defaults()["ode"]["version"]
ANTHEM_VERSION = _get_defaults()["anthem"]["version"]

DARWIN_DEPLOYMENT_VERSION = _get_defaults()["darwin_deployment_version"]

UNIX_INSTALL_PREFIX = "/usr"
DARWIN_INSTALL_PREFIX = "/Applications/Xcode.app/Contents/Developer" \
                        "/Toolchains/XcodeDefault.xctoolchain/usr"

# Options that can only be "configured" by editing this file.
#
# These options are not exposed as command line options on purpose. If you
# need to change any of these, you should do so on trunk or in a branch.

SCRIPT_VERSION = "0.3.0"

OPENGL_MAJOR_VERSION = 3
OPENGL_MINOR_VERSION = 2

ODE_NAME = _get_defaults()["ode"]["name"]
ANTHEM_NAME = _get_defaults()["anthem"]["name"]
SDL_NAME = _get_dependencies()["sdl"]["name"]

PROTOCOL = "https"
GITHUB_API_V4_ENDPOINT = "https://api.github.com/graphql"

COVERAGE_TARGET_MARK = "c"
