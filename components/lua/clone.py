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
This support module has the info necessary for downloading Lua.
"""

import os

from absl import logging

from support.values import CONNECTION_PROTOCOL

from util import http, shell, workspace


SOURCE = True


def _move_files(component):
    subdir = "{}-{}".format(component.key, component.version)
    logging.debug(
        "The name of the subdirectory of %s is %s",
        component.repr,
        subdir
    )
    shell.copytree(
        os.path.join(workspace.temporary_dir(component), subdir),
        workspace.source_dir(component)
    )
    # if not platform.system() == "Windows" and not data.build.ci:
    #     shell.rmtree(workspace.temp_dir(product=product))


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_dir_context(component):
        url = "{}://www.lua.org/ftp/lua-{}.tar.gz".format(
            CONNECTION_PROTOCOL,
            component.version
        )
        dest = os.path.join(
            workspace.temporary_dir(component),
            "lua-{}.tar.gz".format(component.version)
        )
        http.stream(url, dest)
        shell.tar(dest, workspace.temporary_dir(component))
        _move_files(component)
