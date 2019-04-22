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
This support module has the info necessary for downloading Lua.
"""

import os

from support import data

from util import diagnostics, http, shell, workspace


SOURCE = True
GITHUB = False


def _move_files(component):
    subdir = "{}-{}".format(component.key, component.version)

    diagnostics.debug("The name of the {} subdirectory is {}".format(
        component.repr, subdir))

    shell.copytree(os.path.join(
        workspace.temporary_dir(component), subdir),
        workspace.source_dir(component))
    # if not platform.system() == "Windows" and not data.build.ci:
    #     shell.rmtree(workspace.temp_dir(product=product))


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_directory(component):
        url = "{}://www.lua.org/ftp/lua-{}.tar.gz".format(
            data.session.connection_protocol, component.version)
        dest = os.path.join(
            workspace.temporary_dir(component),
            "lua-{}.tar.gz".format(component.version))
        http.stream(url, dest)
        shell.tar(dest, workspace.temporary_dir(component))
        _move_files(component)
