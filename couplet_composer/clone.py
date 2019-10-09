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

"""This module downloads the dependecies of the project."""

import json
import logging
import os

from .clone.tools import clone_tools

from .support.variables import DOWNLOAD_STATUS_FILE

from . import config


def clone_dependencies():
    """Downloads the dependecies of the project."""
    logging.debug("Cloning the dependencies")
    if os.path.isfile(DOWNLOAD_STATUS_FILE):
        with open(DOWNLOAD_STATUS_FILE) as json_file:
            versions = json.load(json_file)
    else:
        versions = {}

    logging.info("Cloning the tools needed to build the project")
    clone_tools()
