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
This support module has the info necessary for downloading Simple
DirectMedia Layer.
"""

import os
import platform

from support import data

from util import diagnostics, http, shell, workspace


SOURCE = True
GITHUB = False


def _move_files(component):
    subdir = "SDL2-{}".format(component.version)

    diagnostics.debug(
        "The name of the {} subdirectory is {}".format(component.repr, subdir)
    )

    shell.copytree(
        os.path.join(workspace.temporary_dir(component), subdir),
        workspace.source_dir(component)
    )


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_directory(component):
        if platform.system() == "Windows":
            url = "{}://www.libsdl.org/release/SDL2-devel-{}-VC.zip".format(
                data.session.connection_protocol,
                component.version
            )
        else:
            url = "{}://www.libsdl.org/release/SDL2-{}.tar.gz".format(
                data.session.connection_protocol,
                component.version
            )
        dest = os.path.join(
            workspace.temporary_dir(component),
            "sdl.{}".format(
                "zip" if platform.system() == "Windows" else "tar.gz"
            )
        )
        http.stream(url, dest)
        shell.tar(dest, workspace.temporary_dir(component))
        shell.rm(dest)
        _move_files(component)
