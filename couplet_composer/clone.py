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

"""This module downloads the dependecies of the project."""

import json
import os

from absl import logging

from .support.variables import DOWNLOAD_STATUS_FILE

from . import config


def download_dependencies():
    """Downloads the dependecies of the project."""
    logging.info("Downloading the dependencies")
    if os.path.isfile(DOWNLOAD_STATUS_FILE):
        with open(DOWNLOAD_STATUS_FILE) as json_file:
            versions = json.load(json_file)
    else:
        versions = {}

    # The download of some dependencies is skipped if they're not
    # needed.
    def _skip_repositories():
        logging.debug("The toolchain in clone is %s", config.TOOLCHAIN)
        skip_list = []
        if config.TOOLCHAIN.cmake is not None:
            skip_list += ["cmake"]
        if config.TOOLCHAIN.ninja is not None:
            skip_list += ["ninja"]
        return skip_list
