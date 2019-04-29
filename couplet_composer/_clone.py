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

"""This module downloads the dependecies of the project."""

import json
import os

from absl import logging

from support.values import DOWNLOAD_STATUS_FILE


def download_dependencies():
    """Downloads the dependecies of the project."""
    logging.info("Downloading the dependencies")

    if os.path.isfile(DOWNLOAD_STATUS_FILE):
        with open(DOWNLOAD_STATUS_FILE) as json_file:
            versions = json.load(json_file)
    else:
        versions = {}
