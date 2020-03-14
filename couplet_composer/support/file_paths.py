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
    return os.path.join("util", "values.json")


def get_project_dependencies_file_path():
    """
    Gives the path to the file that contains constants of the
    dependencies of the project this script acts on relative to
    the Ode repository.
    """
    return os.path.join("util", "dependencies.json")


def get_github_api_file_path():
    """
    Gives the relative default path to the file where the
    information required to access the version 4 of the GitHub
    API can be found.
    """
    return os.path.join("util", ".github_api")
