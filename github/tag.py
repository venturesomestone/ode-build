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
GitHub based on a tag in the repository data.
"""

import os
import platform

from absl import logging

from support.values import \
    GITHUB_OAUTH_TOKEN, \
    GITHUB_REPOSITORY_QUERY_FILE, \
    GITHUB_TAG_QUERY_FILE, \
    TOOLCHAIN

from util import shell, workspace

from ._util import create_github_version

from ._v4_util import call_query, find_release_node


def _checkout_tag_windows(component, tag_ref_name):
    with shell.pushd(workspace.source_dir(component)):
        shell.call([
            TOOLCHAIN.git,
            "checkout",
            "tags/{}".format(tag_ref_name),
            "-b",
            "{}_couplet_branch".format(tag_ref_name)
        ])


def _checkout_tag(component, tag_ref_name):
    key = component.key
    with shell.pushd(os.path.join(workspace.temporary_dir(component), key)):
        shell.call([
            TOOLCHAIN.git,
            "checkout",
            "tags/{}".format(tag_ref_name),
            "-b",
            "{}_couplet_branch".format(tag_ref_name)
        ])


def _clone_release_v4(component, github_data):
    """
    Download a tag based on release info from GitHub by using the
    GraphQL API.
    """
    response_json_data = call_query(GITHUB_TAG_QUERY_FILE, {
        "{REPOSITORY_OWNER}": github_data.owner,
        "{REPOSITORY_NAME}": component.key,
        "{TAG_NAME}": create_github_version(component, github_data)
    })
    repository_url = response_json_data["data"]["repository"]["url"]
    if platform.system() == "Windows":
        src_dir = workspace.source_dir(component)
        head, tail = os.path.split(src_dir)
        with shell.pushd(head):
            shell.call(
                [TOOLCHAIN.git, "clone", "{}.git".format(repository_url), tail]
            )
    else:
        with shell.pushd(workspace.temporary_dir(component)):
            shell.call(
                [TOOLCHAIN.git, "clone", "{}.git".format(repository_url)]
            )
    tag_ref_name = find_release_node(
        component,
        github_data,
        response_json_data
    )["tag"]["name"]
    if platform.system() == "Windows":
        _checkout_tag_windows(component, tag_ref_name)
    else:
        _checkout_tag(component, tag_ref_name)


def _clone_v4(component, github_data):
    """Download a tag from GitHub by using the GraphQL API."""
    response_json_data = call_query(GITHUB_REPOSITORY_QUERY_FILE, {
        "{REPOSITORY_OWNER}": github_data.owner,
        "{REPOSITORY_NAME}": component.key
    })
    repository_url = response_json_data["data"]["repository"]["url"]
    if platform.system() == "Windows":
        src_dir = workspace.source_dir(component)
        head, tail = os.path.split(src_dir)
        with shell.pushd(head):
            shell.call([
                TOOLCHAIN.git,
                "clone",
                "{}.git".format(repository_url),
                tail
            ])
    else:
        with shell.pushd(workspace.temporary_dir(component)):
            shell.call([
                TOOLCHAIN.git,
                "clone",
                "{}.git".format(repository_url)
            ])
    tag_ref_name = create_github_version(component, github_data)
    if platform.system() == "Windows":
        _checkout_tag_windows(component, tag_ref_name)
    else:
        _checkout_tag(component, tag_ref_name)


def clone_release(component, github_data):
    """Download a tag based on release info from GitHub."""
    if GITHUB_OAUTH_TOKEN:
        _clone_release_v4(component, github_data)
    else:
        # TODO
        logging.fatal("TODO")


def clone(component, github_data):
    """Download a tag from GitHub."""
    logging.debug("Going to download a tag of %s", component.repr)
    if GITHUB_OAUTH_TOKEN:
        _clone_v4(component, github_data)
    else:
        # TODO
        logging.fatal("TODO")
    if platform.system() != "Windows":
        shell.copytree(
            os.path.join(workspace.temporary_dir(component), component.key),
            workspace.source_dir(component)
        )
