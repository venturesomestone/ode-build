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
This support module has the info necessary for building glad.
"""

import os
import sys

from support import data

from support.defaults import OPENGL_MAJOR_VERSION, OPENGL_MINOR_VERSION

from util import binaries, shell, workspace


def build(component):
    """Builds the dependency."""
    bin_name = os.path.join("src", "glad.c")
    if binaries.exist(component, bin_name):
        return
    with workspace.build_directory(component) as build_dir:
        src_dir = workspace.source_dir(component)
        shell.copytree(src_dir, build_dir)
        with shell.pushd(build_dir):
            shell.call([
                sys.executable,
                "-m",
                "glad",
                "--profile=core",
                "--api=gl={}.{}".format(
                    OPENGL_MAJOR_VERSION,
                    OPENGL_MINOR_VERSION
                ),
                "--generator=c-debug",
                "--spec=gl",
                "--out-path={}".format(
                    data.session.shared_build_dir)
            ])
