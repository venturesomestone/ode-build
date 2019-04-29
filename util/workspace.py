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
This utility module works out the directories to be used in the
project workspace.
"""

from couplet_composer.flags import FLAGS

from support.values import ASSERTIONS, BUILD_VARIANTS


def build_subdir_name():
    """
    Creates the name for the build subdirectory.
    """
    build_subdir = FLAGS["cmake-generator"].value.replace(" ", "_")

    # NOTE: It is not possible to set assertions to SDL at least
    # for now.
    # sdl_build_dir_label = args.sdl_build_variant
    ode_build_dir_label = BUILD_VARIANTS.ode
    if ASSERTIONS.ode:
        ode_build_dir_label += "Assert"

    anthem_build_dir_label = BUILD_VARIANTS.anthem
    if ASSERTIONS.anthem:
        anthem_build_dir_label += "Assert"

    # TODO It's currently impossible to use assertions in SDL
    sdl_build_dir_label = BUILD_VARIANTS.sdl

    if ode_build_dir_label == anthem_build_dir_label \
            and ode_build_dir_label == sdl_build_dir_label:
        build_subdir += "-" + ode_build_dir_label

    elif ode_build_dir_label != anthem_build_dir_label \
            and ode_build_dir_label == sdl_build_dir_label:
        build_subdir += "-" + ode_build_dir_label
        build_subdir += "+anthem-" + anthem_build_dir_label

    elif ode_build_dir_label == anthem_build_dir_label \
            and ode_build_dir_label != sdl_build_dir_label:
        build_subdir += "-" + ode_build_dir_label
        build_subdir += "+sdl-" + sdl_build_dir_label

    elif sdl_build_dir_label == anthem_build_dir_label \
            and ode_build_dir_label != sdl_build_dir_label:
        build_subdir += "-" + anthem_build_dir_label
        build_subdir += "+ode-" + ode_build_dir_label

    else:
        build_subdir += "+ode-" + ode_build_dir_label
        build_subdir += "+anthem-" + anthem_build_dir_label
        build_subdir += "+sdl-" + sdl_build_dir_label

    return build_subdir
