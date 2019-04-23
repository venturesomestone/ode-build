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

from contextlib import contextmanager

from support import data

from support.variables import ODE_SOURCE_ROOT

from . import shell


def source_dir(component):
    """
    Create an absolute path to the source directory of a
    dependency.
    """
    if component.is_source:
        target = "source"
    else:
        target = data.session.host_target
    return os.path.join(
        data.session.shared_dir,
        component.key,
        component.version,
        target
    )


def temporary_dir(component):
    """
    Create an absolute path to the temporary directory of a
    dependency.
    """
    return os.path.join(data.session.shared_dir, component.key, "tmp")


def build_dir(component):
    """
    Gives the build directory for a dependency.
    """
    path = os.path.join(
        data.session.build_dir,
        "{}-{}".format(component.key, data.session.host_target),
        component.version
    )
    shell.makedirs(path)
    return path


@contextmanager
def clone_directory(component):
    """Creates the directories for cloning a dependency."""
    shell.rmtree(source_dir(component))
    shell.rmtree(temporary_dir(component))
    shell.makedirs(source_dir(component))
    shell.makedirs(temporary_dir(component))
    yield
    shell.rmtree(temporary_dir(component))


@contextmanager
def build_directory(component):
    """
    Creates the directories for building a dependency and yields
    the build directory.
    """
    path = build_dir(component)
    shell.rmtree(path)
    shell.makedirs(path)
    yield path


def compute_build_subdir_name(args):
    """
    Creates the directory name for the build subdirectory.
    """
    cmake_label = args.cmake_generator.replace(" ", "_")
    build_subdir = cmake_label
    # NOTE: It is not possible to set assertions to SDL at least
    # for now.
    # sdl_build_dir_label = args.sdl_build_variant
    ode_build_dir_label = args.ode_build_variant
    if args.assertions:
        ode_build_dir_label += "Assert"
    # TODO It's not possible to set SDL build variant
    # if args.sdl_build_variant == args.anthem_build_variant:
    #     build_subdir += anthem_build_dir_label
    # else:
    #     build_subdir += anthem_build_dir_label
    #     build_subdir += "+sdl-{}".format(sdl_build_dir_label)
    build_subdir += ode_build_dir_label
    return build_subdir
