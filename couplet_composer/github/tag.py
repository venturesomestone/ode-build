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

"""
This support module contains functions for downloading tags from
GitHub.
"""

import os

from ..support.platform_names import get_windows_system_name

from ..util import http, shell

from ._api_v4 import find_release_node, make_api_call


def _checkout_tag(
    path,
    git,
    github_data,
    tag_name,
    dry_run=None,
    print_debug=None
):
    with shell.pushd(os.path.join(path, github_data.name)):
        shell.call(
            [
                git,
                "checkout",
                "tags/{}".format(tag_name),
                "-b",
                "{}_composer_branch".format(tag_name)
            ],
            dry_run=dry_run,
            echo=print_debug
        )


def _clone_by_api_v4(
    path,
    git,
    github_data,
    user_agent,
    api_token,
    host_system,
    dry_run=None,
    print_debug=None
):
    """
    Downloads a tag from GitHub using the version 4 of the
    GitHub API.

    path -- Path to the directory where the downloaded files are
    put.

    git -- Path to the Git executable from the toolchain.

    github_data -- The object containing the data required to
    download the tag from GitHub.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.

    host_system -- The system this script is run on.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    graph_ql_call = None
    with open(os.path.join(
        os.path.dirname(__file__),
        "graphql",
        "github_tag.graphql"
    )) as f:
        graph_ql_call = str(f.read()).replace(
            "{OWNER}",
            github_data.owner
        ).replace(
            "{REPOSITORY_NAME}",
            github_data.name
        ).replace(
            "{TAG_NAME}",
            github_data.tag_name
        )
    api_response = make_api_call(
        query=graph_ql_call,
        user_agent=user_agent,
        api_token=api_token
    )
    repository_url = api_response["data"]["repository"]["url"]

    with shell.pushd(path):
        shell.call(
            [git, "clone", "{}.git".format(repository_url)],
            dry_run=dry_run,
            echo=print_debug
        )

    tag_name = find_release_node(api_response=api_response)["tag"]["name"]

    _checkout_tag(
        path=path,
        git=git,
        github_data=github_data,
        tag_name=tag_name,
        dry_run=dry_run,
        print_debug=print_debug
    )

    return os.path.join(path, github_data)


def download(
    path,
    git,
    github_data,
    user_agent,
    api_token,
    host_system,
    dry_run=None,
    print_debug=None
):
    """
    Downloads a tag from GitHub according to release data and
    returns path to the downloaded tag.

    path -- Path to the directory where the downloaded files are
    put.

    git -- Path to the Git executable from the toolchain.

    github_data -- The object containing the data required to
    download the tag from GitHub.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.

    host_system -- The system this script is run on.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    return _clone_by_api_v4(
        path=path,
        git=git,
        github_data=github_data,
        user_agent=user_agent,
        api_token=api_token,
        host_system=host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )
