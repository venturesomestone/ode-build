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

"""This support module contains path constants."""

import os


def get_preset_file_path():
    """
    Gives the path to the default build preset file relative to
    the Ode repository.
    """
    return os.path.join("util", "composer-presets.ini")


def get_project_values_file_path():
    """
    Gives the path to the file that contains constants of the
    project this script acts on relative to the Ode repository.
    """
    return os.path.join("util", "composer", "values.json")
