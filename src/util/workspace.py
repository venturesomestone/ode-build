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
This utility module works out the directories to be used in the
project workspace.
"""

import os


def compute_build_subdir(args):
    """
    Creates the directory name for the full build subdirectory.
    """
    version_subdir = args.anthem_version
    cmake_label = args.cmake_generator.replace(" ", "_")
    build_subdir = cmake_label
    # NOTE: It is not possible to set assertions to SDL at least
    # for now.
    sdl_build_dir_label = args.sdl_build_variant
    anthem_build_dir_label = args.anthem_build_variant
    if args.assertions:
        anthem_build_dir_label += "Assert"
    if args.sdl_build_variant == args.anthem_build_variant:
        build_subdir += anthem_build_dir_label
    else:
        build_subdir += anthem_build_dir_label
        build_subdir += "+sdl-{}".format(sdl_build_dir_label)
    return os.path.join(version_subdir, build_subdir)
