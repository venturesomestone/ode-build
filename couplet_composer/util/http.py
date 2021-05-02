# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains helpers for streaming from internet.
"""

import os

import requests

from . import shell


def stream(
    url: str,
    destination: str,
    headers: dict = None,
    dry_run: bool = None,
    echo: bool = None
) -> None:
    """Streams a file to the local machine by Hypertext Transport
    Protocol.

    Args:
        url (str): The url where the file is streamed from.
        destination (str): The local path where the file is
            streamed.
        headers (dict): The possible headers for the HTTP call.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    if headers:
        response = requests.get(url=url, headers=headers, stream=True)
    else:
        response = requests.get(url=url, stream=True)
    if not os.path.isdir(destination):
        shell.makedirs(
            os.path.dirname(destination),
            dry_run=dry_run,
            echo=echo
        )
    if echo:
        shell.call(
            ["curl", "-L", "-o", destination, "--create-dirs", url],
            dry_run=True,
            echo=True
        )
    if dry_run:
        return
    with open(destination, "wb") as destination_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                destination_file.write(chunk)
