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

"""This support module has the file stream functions."""

import platform
import sys

import requests

from absl import logging

from support.values import CI

from . import shell


def stream(url, destination, headers=None):
    """
    Stream a file to the local machine.

    url -- the url that the file is streamed from.
    destination -- the local file where the file is streamed.
    headers -- the possible headers for the call.
    """
    logging.debug("Streaming an asset from %s", url)
    if CI or sys.version_info.major < 3:
        if platform.system() == "Windows":
            if headers:
                response = requests.get(url=url, headers=headers, stream=True)
            else:
                response = requests.get(url=url, stream=True)
            with open(destination, "wb") as destination_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        destination_file.write(chunk)
        else:
            shell.curl(url, destination)
        return
    if headers:
        response = requests.get(url=url, headers=headers, stream=True)
    else:
        response = requests.get(url=url, stream=True)
    with open(destination, "wb") as destination_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                destination_file.write(chunk)
    logging.debug("Finished streaming an asset to %s", destination)
