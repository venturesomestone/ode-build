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

"""
This support module has functions for downloading content from
GitHub.
"""

import os
import platform

from support import data

from util import diagnostics, http, shell, workspace

from . import tag, v4_util


ASSET_QUERY_GRAPHQL = "github_asset.graphql"


def _download_v4(component, github_data, asset):
    release_asset_node = v4_util.find_release_node(
        component,
        github_data,
        v4_util.call_query(ASSET_QUERY_GRAPHQL, {
            "{REPOSITORY_OWNER}": github_data.owner,
            "{REPOSITORY_NAME}": component.key,
            "{TAG_NAME}": v4_util.get_github_version(component, github_data),
            "{ASSET_NAME}": asset
        })
    )["releaseAssets"]["edges"][0]["node"]
    diagnostics.trace(
        "The release asset node has the name {} and the URL {}".format(
            release_asset_node["name"],
            release_asset_node["url"]
        )
    )
    dest = os.path.join(workspace.temporary_dir(component), asset)
    http.stream(url=release_asset_node["url"], destination=dest, headers={
        "User-Agent": "anttikivi",
        "Accept": "application/octet-stream"
    })


def download(component, github_data, asset):
    """Download an asset from GitHub."""
    if data.session.github_token:
        _download_v4(component, github_data, asset)
    else:
        # TODO
        diagnostics.fatal("TODO")


def basic_tag(component, github_data):
    """Downloads a basic release tag from GitHub."""
    diagnostics.trace_head("Going to download a release of {}".format(
        component.repr
    ))
    tag.clone_release(component, github_data)
    if platform.system() != "Windows":
        source_dir = workspace.source_dir(component)
        version_dir = os.path.dirname(source_dir)
        shell.rmtree(source_dir)
        shell.rmtree(version_dir)
        shell.copytree(
            os.path.join(workspace.temporary_dir(component), component.key),
            workspace.source_dir(component))


def basic_asset(component, github_data, asset):
    """Downloads a specific asset from GitHub."""
    diagnostics.trace_head("Going to download a release of {}".format(
        component.repr
    ))
    download(component, github_data, asset)
