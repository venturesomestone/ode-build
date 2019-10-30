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
This support module contains constants that are needed in the
build.
"""

import os


def get_project_name():
    """Gives the full name of the project."""
    return "Couplet Composer"


def get_ode_repository_name():
    """Gives the name of the Ode repository directory."""
    return "unsung-anthem"


# The name of the package.
PACKAGE_NAME = "couplet_composer"

# The path to the file containing the default values, relative to
# the Obliging Ode repository.
DEFAULTS_FILE_PATH = os.path.join("util", "composer", "defaults.json")


def get_preset_file_path():
    """
    Gives the path to the default build preset file relative to
    the Ode repository.
    """
    return os.path.join("util", "composer-presets.ini")
