# ------------------------------------------------------------- #
#                 Obliging Ode & Unsung Anthem
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""This support module has the file stream functions."""


import platform
import sys

import requests

from support import data

from . import diagnostics, shell


def stream(url, destination, headers=None):
    """
    Stream a file to the local machine.

    url -- the url that the file is streamed from.
    destination -- the local file where the file is streamed.
    headers -- the possible headers for the HTTP call.
    """
    diagnostics.debug("Streaming an asset from {}".format(url))
    if data.session.ci or sys.version_info.major < 3:
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
    diagnostics.debug_ok("Finished streaming an asset to {}".format(
        destination))
