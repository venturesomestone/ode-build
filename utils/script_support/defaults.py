#===----------------------------- defaults.py ----------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved

"""Default option value definitions."""


from build_utils.mapping import Mapping

from build_utils.reflection import product_config_value


__all__ = [
    # Command line configurable
    "BUILD_VARIANT", "CMAKE_GENERATOR", "CXX_STANDARD", "ANTHEM_VERSION",
    "ODE_VERSION", "DARWIN_DEPLOYMENT_VERSION", "UNIX_INSTALL_PREFIX",
    "DARWIN_INSTALL_PREFIX",

    # Constants
    "PRODUCT_CONFIG", "PROTOCOL", "GITHUB_API_V4_ENDPOINT"
]


# Options that can be "configured" by command line options

BUILD_VARIANT = "Debug"
CMAKE_GENERATOR = "Ninja"

CXX_STANDARD = "c++17"

ANTHEM_VERSION = product_config_value("ANTHEM_VERSION")
ODE_VERSION = product_config_value("ODE_VERSION")

DARWIN_DEPLOYMENT_VERSION = "10.9"

UNIX_INSTALL_PREFIX = "/usr"
DARWIN_INSTALL_PREFIX = "/Applications/Xcode.app/Contents/Developer" \
                        "/Toolchains/XcodeDefault.xctoolchain/usr"

# Options that can only be "configured" by editing this file.
#
# These options are not exposed as command line options on purpose. If you
# need to change any of these, you should do so on trunk or in a branch.

SCRIPT_VERSION = "0.3.0"

PROTOCOL = "https"
GITHUB_API_V4_ENDPOINT = "https://api.github.com/graphql"


COVERAGE_TARGET_MARK = "c"


PRODUCT_CONFIG = product_config_value("PRODUCT_CONFIG")
