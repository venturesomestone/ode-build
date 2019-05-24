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

"""
This support module has functions for downloading content from
GitHub based on a release in the repository data.
"""

import os
import platform

from absl import logging

from support.values import GITHUB_ASSET_QUERY_FILE, GITHUB_OAUTH_TOKEN

from util import http, shell, workspace

from . import tag

from ._util import create_github_version

from ._v4_util import call_query, find_release_node


def _download_v4(component, github_data, asset):
    release_asset_node = find_release_node(
        component,
        github_data,
        call_query(GITHUB_ASSET_QUERY_FILE, {
            "{REPOSITORY_OWNER}": github_data.owner,
            "{REPOSITORY_NAME}": component.key,
            "{TAG_NAME}": create_github_version(component, github_data),
            "{ASSET_NAME}": asset
        })
    )["releaseAssets"]["edges"][0]["node"]
    logging.debug(
        "The release asset node has the name '%s' and the URL '%s'",
        release_asset_node["name"],
        release_asset_node["url"]
    )
    dest = os.path.join(workspace.temporary_dir(component), asset)
    http.stream(
        release_asset_node["url"],
        dest,
        {"User-Agent": "anttikivi", "Accept": "application/octet-stream"}
    )


def _download(component, github_data, asset):
    """Downloads an asset from GitHub."""
    if GITHUB_OAUTH_TOKEN:
        _download_v4(component, github_data, asset)
    else:
        # TODO
        logging.fatal("TODO")


def basic_tag(component, github_data):
    """Downloads a basic release tag from GitHub."""
    logging.debug("Going to download a release of %s", component.repr)
    tag.clone_release(component, github_data)
    if platform.system() != "Windows":
        source_dir = workspace.source_dir(component)
        version_dir = os.path.dirname(source_dir)
        shell.rmtree(source_dir)
        shell.rmtree(version_dir)
        shell.copytree(
            os.path.join(workspace.temporary_dir(component), component.key),
            workspace.source_dir(component)
        )


def basic_asset(component, github_data, asset):
    """Downloads a specific asset from GitHub."""
    logging.debug("Going to download a release of %s", component.repr)
    _download(component, github_data, asset)
