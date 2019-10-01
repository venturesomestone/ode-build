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

"""
This module contains the functions for common set-up procedures.
"""

import json
import logging
import os

from .support.toolchain import host_toolchain, target_toolchain_file

from .support.variables import COMPOSER_ROOT

from . import config


def _set_up_tool_dependencies(json_data):
    return dict(json_data)


def set_up():
    """Sets up the runtime values for the composer."""

    # Get the saved toolchain
    toolchain_data = None
    toolchain_file = target_toolchain_file(config.ARGS.host_target)

    if os.path.exists(toolchain_file):
        logging.debug("Loading the toolchain from a file: %s", toolchain_file)
        with open(toolchain_file) as json_file:
            toolchain_data = json.load(json_file)

    config.TOOLCHAIN = host_toolchain(toolchain_data)

    # Set up the tool dependency data
    tools_data = None
    tools_file = os.path.join(COMPOSER_ROOT, "tools.json")

    logging.debug(
        "Loading the tool dependency data from a file: %s",
        tools_file
    )

    with open(tools_file) as f:
        tools_data = json.load(f)
    config.TOOLS = _set_up_tool_dependencies(tools_data)

    logging.debug("The tool dependency data is: %s", config.TOOLS)
