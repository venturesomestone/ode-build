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

"""
This support module reads the values from the project Couplet
Composer acts on.
"""

import json
import os

from ..util.cache import cached

from .file_paths import get_project_values_file_path

from .project_names import get_ode_repository_name


@cached
def _get_project_values_file(source_root):
    """
    Gives the path to the file that contains the project values.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return os.path.join(
        source_root,
        get_ode_repository_name(),
        get_project_values_file_path()
    )


@cached
def _get_project_values(source_root):
    """
    Gives the project values.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    with open(_get_project_values_file(source_root=source_root)) as f:
        return json.load(f)


@cached
def get_ode_name(source_root):
    """
    Gives the name of Obliging Ode.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return _get_project_values(source_root=source_root)["ode"]["name"]


@cached
def get_anthem_name(source_root):
    """
    Gives the name of Unsung Anthem.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return _get_project_values(source_root=source_root)["anthem"]["name"]


@cached
def get_ode_version(source_root):
    """
    Gives the default version of Obliging Ode.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return _get_project_values(source_root=source_root)["ode"]["version"]


@cached
def get_anthem_version(source_root):
    """
    Gives the default version of Unsung Anthem.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return _get_project_values(source_root=source_root)["anthem"]["version"]


@cached
def get_opengl_version(source_root):
    """
    Gives the default version of OpenGL.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return _get_project_values(source_root=source_root)["opengl"]["version"]
