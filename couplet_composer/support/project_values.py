# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

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
    try:
        with open(_get_project_values_file(source_root=source_root)) as f:
            return json.load(f)
    except Exception:
        return None


@cached
def get_ode_name(source_root):
    """
    Gives the name of Obliging Ode.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    project_values = _get_project_values(source_root=source_root)
    if project_values:
        return project_values["ode"]["name"]
    else:
        return "ode-name-file-not-found"


@cached
def get_anthem_name(source_root):
    """
    Gives the name of Unsung Anthem.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    project_values = _get_project_values(source_root=source_root)
    if project_values:
        return project_values["anthem"]["name"]
    else:
        return "anthem-name-file-not-found"


@cached
def get_ode_version(source_root):
    """
    Gives the default version of Obliging Ode.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    project_values = _get_project_values(source_root=source_root)
    if project_values:
        return project_values["ode"]["version"]
    else:
        return "ode-version-file-not-found"


@cached
def get_anthem_version(source_root):
    """
    Gives the default version of Unsung Anthem.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    project_values = _get_project_values(source_root=source_root)
    if project_values:
        return project_values["anthem"]["version"]
    else:
        return "anthem-version-file-not-found"


@cached
def get_opengl_version(source_root):
    """
    Gives the default version of OpenGL.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    project_values = _get_project_values(source_root=source_root)
    if project_values:
        return project_values["opengl"]["version"]
    else:
        return "3.2"


@cached
def get_default_ode_window_name(source_root):
    """
    Gives the default name of the window of Obliging Ode.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return "ode-window"


@cached
def get_default_anthem_window_name(source_root):
    """
    Gives the default name of the window of Unsung Anthem.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return get_anthem_name(source_root=source_root)


@cached
def get_default_ode_logger_name(source_root):
    """
    Gives the default name of the logger of Obliging Ode.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return "ode"


@cached
def get_default_anthem_logger_name(source_root):
    """
    Gives the default name of the logger of Unsung Anthem.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return get_anthem_name(source_root=source_root)


@cached
def get_ode_binaries_base_name(source_root):
    """
    Gives the default base name for the binaries of Obliging Ode.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return "ode"


@cached
def get_anthem_binaries_base_name(source_root):
    """
    Gives the default base name for the binaries of Unsung
    Anthem.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return "anthem"
