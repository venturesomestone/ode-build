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


def clone_tools():
    # The download of some dependencies is skipped if they're not
    # needed.
    def _skip_repositories():
        logging.debug("The toolchain in clone is %s", config.TOOLCHAIN)
        skip_list = []
        if config.TOOLCHAIN["cmake"] is not None:
            skip_list += ["cmake"]
        if config.TOOLCHAIN["ninja"] is not None:
            skip_list += ["ninja"]
        return skip_list

    skip_repository_list = _skip_repositories()

    logging.debug(
        "The cloning of the following repositories is to be skipped: %s",
        skip_repository_list
    )

    for k, v in config.TOOLS.items():
        logging.debug("Checking if %s needs to be cloned", v["name"])

        if k in skip_repository_list:
            logging.debug(
                "%s is in the list of the repositories to be skipped, "
                "continuing",
                v["name"]
            )
            continue
