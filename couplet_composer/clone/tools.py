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

"""This module clones the tool dependecies of the composer."""

import logging

from .. import config


def _resolve_repositories_for_skipping():
    logging.debug("The toolchain in clone is %s", config.TOOLCHAIN)
    skip_list = []
    if config.TOOLCHAIN["cmake"] is not None:
        skip_list += ["cmake"]
    if config.TOOLCHAIN["ninja"] is not None:
        skip_list += ["ninja"]
    return skip_list


def clone_tools():
    # The downloads of some dependencies are skipped if they're
    # not needed.
    skip_repository_list = _resolve_repositories_for_skipping()

    logging.debug(
        "The cloning of the following repositories is to be skipped: %s",
        skip_repository_list
    )

    for tool_key, tool_data in config.TOOLS.items():
        tool_name = tool_data["name"]

        logging.debug("Checking if %s needs to be cloned", tool_name)

        if tool_key in skip_repository_list:
            logging.debug(
                "%s is in the list of the repositories to be skipped, "
                "continuing",
                tool_name
            )
            continue
