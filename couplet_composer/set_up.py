# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem project.
#
# Copyright 2019 Antti Kivi
# Licensed under the EUPL, version 1.2
#
# ------------------------------------------------------------- #

"""
This module contains the functions for common set-up procedures.
"""

import json
import os

from .support.toolchain import host_toolchain, target_toolchain_file

from . import config


def set_up():
    """Sets up the runtime values for the composer."""

    # Get the saved toolchain
    toolchain_data = None
    toolchain_file = target_toolchain_file(FLAGS["host-toolchain"].value)

    if os.path.exists(toolchain_file):
        with open(toolchain_file) as json_file:
            toolchain_data = json.load(json_file)

    config.TOOLCHAIN = host_toolchain(
        FLAGS["host-target"].value,
        toolchain_data
    )
