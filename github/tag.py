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
REPOSITORY_QUERY_GRAPHQL = "github_repository.graphql"


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


def _clone_release_v4(component, github_data):
    """Download a tag from GitHub."""
    response_json_data = v4_util.call_query(TAG_QUERY_GRAPHQL, {
        "{REPOSITORY_OWNER}": github_data.owner,
        "{REPOSITORY_NAME}": component.key,
        "{TAG_NAME}": v4_util.get_github_version(component, github_data)
    })

    repository_url = response_json_data["data"]["repository"]["url"]

    if platform.system() == "Windows":
        source_dir = workspace.source_dir(component)
        head, tail = os.path.split(source_dir)
        with shell.pushd(head):
            shell.call([
                data.session.toolchain.git,
                "clone",
                "{}.git".format(repository_url),
                tail
            ])
    else:
        with shell.pushd(workspace.temporary_dir(component)):
            shell.call([
                data.session.toolchain.git,
                "clone",
                "{}.git".format(repository_url)
            ])
    tag_ref_name = v4_util.find_release_node(
        component,
        github_data,
        response_json_data
    )["tag"]["name"]

    if platform.system() == "Windows":
        _checkout_tag_windows(component, tag_ref_name)
    else:
        _checkout_tag(component, tag_ref_name)


def _clone_v4(component, github_data):
    """Download a tag from GitHub."""
    response_json_data = v4_util.call_query(REPOSITORY_QUERY_GRAPHQL, {
        "{REPOSITORY_OWNER}": github_data.owner,
        "{REPOSITORY_NAME}": component.key
    })

    repository_url = response_json_data["data"]["repository"]["url"]

    if platform.system() == "Windows":
        source_dir = workspace.source_dir(component)
        head, tail = os.path.split(source_dir)
        with shell.pushd(head):
            shell.call([
                data.session.toolchain.git,
                "clone",
                "{}.git".format(repository_url),
                tail
            ])
    else:
        with shell.pushd(workspace.temporary_dir(component)):
            shell.call([
                data.session.toolchain.git,
                "clone",
                "{}.git".format(repository_url)
            ])

    tag_ref_name = v4_util.get_github_version(component, github_data)

    if platform.system() == "Windows":
        _checkout_tag_windows(component, tag_ref_name)
    else:
        _checkout_tag(component, tag_ref_name)


def clone_release(component, github_data):
    """Download a tag from GitHub."""
    if data.session.github_token:
        _clone_release_v4(component, github_data)
    else:
        # TODO
        diagnostics.fatal("TODO")


def clone(component, github_data):
    """Download a tag from GitHub."""
    diagnostics.trace_head("Going to download a tag of {}".format(
        component.repr
    ))
    if data.session.github_token:
        _clone_v4(component, github_data)
    else:
        # TODO
        diagnostics.fatal("TODO")
    if platform.system() != "Windows":
        shell.copytree(
            os.path.join(workspace.temporary_dir(component), component.key),
            workspace.source_dir(component))
