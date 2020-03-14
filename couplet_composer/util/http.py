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

"""This support module is used to download files."""

import sys

import requests

from ..support.platform_names import get_windows_system_name

from . import shell


def stream(
    url,
    destination,
    host_system,
    headers=None,
    dry_run=None,
    print_debug=None
):
    """
    Streams a file to the local machine.

    url -- The url where the file is streamed from.

    destination -- The local file where the file is streamed.

    host_system -- The system this script is run on.

    headers -- The possible headers for the HTTP call.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    # The conditional statement here before renewal was:
    # if data.session.ci or sys.version_info.major < 3:

    if sys.version_info.major < 3:
        if host_system == get_windows_system_name():
            if headers:
                response = requests.get(url=url, headers=headers, stream=True)
            else:
                response = requests.get(url=url, stream=True)
            with open(destination, "wb") as destination_file:
                if print_debug:
                    shell.curl(url, destination, dry_run=True)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        destination_file.write(chunk)
        else:
            shell.curl(url, destination, dry_run=dry_run, echo=print_debug)
        return
    if headers:
        response = requests.get(url=url, headers=headers, stream=True)
    else:
        response = requests.get(url=url, stream=True)
    with open(destination, "wb") as destination_file:
        if print_debug:
            shell.curl(url, destination, dry_run=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                destination_file.write(chunk)
