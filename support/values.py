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

"""
This support module has build values that are set at the
beginning of the run.
"""

import os

from util.mapping import Mapping

from .variables import ODE_BUILD_ROOT


__all__ = [
    "BUILD_VARIANTS",
    "ASSERTIONS",
    "BUILD_SUBDIR",
    "BUILD_DIR",
    "DOWNLOAD_DIR",
    "DOWNLOAD_STATUS_FILE"
]


# The dictionary of build variants has the build variant for each
# project propagated from the command line flags
BUILD_VARIANTS = Mapping()


# The dictionary of assertions has the assertion status for each
# project propagated from the command line flags
ASSERTIONS = Mapping()


# The build subdirectory is the directory in the build directory
# where the build files are created
BUILD_SUBDIR = None

# The build directory in the build root is the directory that the
# build files are created in.
BUILD_DIR = os.path.join(ODE_BUILD_ROOT, "build")

# The download directory in the build root is the directory that
# the dependencies needed to build the project are downloaded to.
DOWNLOAD_DIR = os.path.join(ODE_BUILD_ROOT, "shared")

# The download status file is a JSON file containing the versions
# of the dependencies in order to determine whether to download
# new versions of them.
DOWNLOAD_STATUS_FILE = os.path.join(DOWNLOAD_DIR, "status")
