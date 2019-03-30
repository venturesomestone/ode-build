#===--------------------------- github_master.py --------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved

"""
The support module containing the utilities for downloading a repository from
GitHub.
"""


import os
import platform

from build_utils import diagnostics, shell, workspace

from script_support import data

from . import github_v4_util


URL_QUERY_GRAPHQL = "github_url.graphql"


def checkout_tag_windows(product):
    """Checkout the master branch."""
    with shell.pushd(workspace.source_dir(product=product)):
        shell.call([data.build.toolchain.git, "checkout", "master"])


def checkout_tag(product):
    """Checkout the master branch."""
    key = product.key
    with shell.pushd(os.path.join(workspace.temp_dir(product=product), key)):
        shell.call([data.build.toolchain.git, "checkout", "master"])


def download_v4(product):
    """Download a repository from GitHub."""
    github_data = product.github_data
    response_json_data = github_v4_util.call_query(URL_QUERY_GRAPHQL, {
        "{REPOSITORY_OWNER}": github_data.owner,
        "{REPOSITORY_NAME}": github_data.name
    })

    if platform.system() == "Windows":
        source_dir = workspace.source_dir(product=product)
        head, tail = os.path.split(source_dir)
        with shell.pushd(head):
            shell.call([data.build.toolchain.git, "clone", "{}.git".format(
                response_json_data["repository"]["url"]), tail])
    else:
        with shell.pushd(workspace.temp_dir(product=product)):
            shell.call([data.build.toolchain.git, "clone", "{}.git".format(
                response_json_data["repository"]["url"])])

    if platform.system() == "Windows":
        checkout_tag_windows(product)
    else:
        checkout_tag(product)


def download(product):
    """Download a tag from GitHub."""
    if data.build.github_token:
        download_v4(product=product)
    else:
        # TODO
        diagnostics.fatal("TODO")
