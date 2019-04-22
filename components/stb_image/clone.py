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
This support module has the info necessary for downloading
stb_image.
"""

import os
import platform

from github import tag, v4_util

from support import data

from util import diagnostics, shell, workspace

from util.mapping import Mapping


SOURCE = True
GITHUB = True
GITHUB_DATA = Mapping(
    owner="nothings",
    name="stb",
    commit="2c2908f50515dcd939f24be261c3ccbcd277bb49"
)


def _checkout_commit(component):
    with shell.pushd(
        os.path.join(workspace.temporary_dir(component), GITHUB_DATA.name)
    ):
        shell.call([
            data.session.toolchain.git,
            "checkout",
            "-b",
            "{}_ode_branch".format(component.version),
            GITHUB_DATA.commit
        ])


def _clone_v4(component):
    response_json_data = v4_util.call_query(tag.REPOSITORY_QUERY_GRAPHQL, {
        "{REPOSITORY_OWNER}": GITHUB_DATA.owner,
        "{REPOSITORY_NAME}": GITHUB_DATA.name
    })

    repository_url = response_json_data["data"]["repository"]["url"]

    with shell.pushd(workspace.temporary_dir(component)):
        shell.call([
            data.session.toolchain.git,
            "clone",
            "{}.git".format(repository_url)
        ])
    _checkout_commit(component)


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_directory(component):
        diagnostics.trace_head("Going to download a release of {}".format(
            component.repr
        ))
        if data.session.github_token:
            _clone_v4(component)
        else:
            # TODO
            diagnostics.fatal("TODO")
        shell.copy(
            os.path.join(
                workspace.temporary_dir(component),
                GITHUB_DATA.name,
                "stb_image.h"
            ),
            os.path.join(workspace.source_dir(component), "stb_image.h")
        )


def version_data():
    """
    Gives the custom version data that the program writes into
    the JSON file where the local dependency versions are stored.
    """
    return {"commit": GITHUB_DATA.commit}
