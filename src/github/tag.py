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
This support module has functions for downloading a tag from
GitHub.
"""

import os
import platform

from support import data

from util import diagnostics, shell, workspace

from . import v4_util


TAG_QUERY_GRAPHQL = "github_tag.graphql"


def _checkout_tag_windows(component, tag_ref_name):
    with shell.pushd(workspace.source_dir(component)):
        shell.call([
            data.session.toolchain.git, "checkout",
            "tags/{}".format(tag_ref_name), "-b",
            "{}_ode_branch".format(tag_ref_name)
        ])


def _checkout_tag(component, tag_ref_name):
    key = component.key
    with shell.pushd(os.path.join(workspace.temporary_dir(component), key)):
        shell.call([
            data.session.toolchain.git, "checkout",
            "tags/{}".format(tag_ref_name), "-b",
            "{}_ode_branch".format(tag_ref_name)
        ])


def _download_v4(component, github_data):
    """Download a tag from GitHub."""
    response_json_data = v4_util.call_query(TAG_QUERY_GRAPHQL, {
        "{REPOSITORY_OWNER}": github_data.owner,
        "{REPOSITORY_NAME}": component.key
    })

    if platform.system() == "Windows":
        source_dir = workspace.source_dir(component)
        head, tail = os.path.split(source_dir)
        with shell.pushd(head):
            shell.call([data.session.toolchain.git, "clone", "{}.git".format(
                response_json_data["repository"]["url"]), tail])
    else:
        with shell.pushd(workspace.temporary_dir(component)):
            shell.call([data.session.toolchain.git, "clone", "{}.git".format(
                response_json_data["repository"]["url"])])
    release_node = v4_util.find_release_node(
        component, github_data, response_json_data)

    if not release_node:
        release_node = v4_util.find_release_node_by_tag(
            component, github_data, response_json_data)

    tag_ref_name = v4_util.get_github_version(component, github_data) \
        if not release_node else release_node["tag"]["name"]

    if platform.system() == "Windows":
        _checkout_tag_windows(component, tag_ref_name)
    else:
        _checkout_tag(component, tag_ref_name)


def download(component, github_data):
    """Download a tag from GitHub."""
    if data.session.github_token:
        _download_v4(component, github_data)
    else:
        # TODO
        diagnostics.fatal("TODO")
