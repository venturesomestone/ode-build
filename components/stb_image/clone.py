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
This support module has the info necessary for downloading
stb_image.
"""

import os
import platform

from absl import logging

from github._v4_util import call_query

from support.values import \
    CONNECTION_PROTOCOL, \
    DEPENDENCIES, \
    GITHUB_REPOSITORY_QUERY_FILE, \
    TOOLCHAIN

from util import shell, workspace

from util.mapping import Mapping


SOURCE = True
GITHUB_DATA = Mapping(owner="nothings", name="stb")


def _checkout_commit(component):
    with shell.pushd(
        os.path.join(workspace.temporary_dir(component), GITHUB_DATA.name)
    ):
        shell.call([
            TOOLCHAIN.git,
            "checkout",
            "-b",
            "{}_couplet_branch".format(component.version),
            DEPENDENCIES.stb_image.version_data.commit
        ])


def _clone_v4(component):
    response_json_data = call_query(GITHUB_REPOSITORY_QUERY_FILE, {
        "{REPOSITORY_OWNER}": GITHUB_DATA.owner,
        "{REPOSITORY_NAME}": GITHUB_DATA.name
    })
    repository_url = response_json_data["data"]["repository"]["url"]
    with shell.pushd(workspace.temporary_dir(component)):
        shell.call([TOOLCHAIN.git, "clone", "{}.git".format(repository_url)])
    _checkout_commit(component)


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_dir_context(component):
        logging.debug("Going to download a release of %s", component.repr)
        if CONNECTION_PROTOCOL:
            _clone_v4(component)
        else:
            # TODO
            logging.fatal("TODO")
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
    return {"commit": DEPENDENCIES.stb_image.version_data.commit}
