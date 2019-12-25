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
This support module contains constants for determining which of
the project libraries to build.
"""


def get_ode_static_name():
    """
    Gives the constant that informs to build the static library
    of Obliging Ode.
    """
    return "ode-static"


def get_ode_shared_name():
    """
    Gives the constant that informs to build the static library
    of Obliging Ode.
    """
    return "ode-shared"


def get_anthem_static_name():
    """
    Gives the constant that informs to build the static library
    of Unsung Anthem.
    """
    return "anthem-static"


def get_anthem_shared_name():
    """
    Gives the constant that informs to build the static library
    of Unsung Anthem.
    """
    return "anthem-shared"


def get_all_project_library_names():
    """
    Gives a list containing all of the constants that inform to
    build specific libraries of Obliging Ode and Unsung Anthem.
    """
    return [
        get_ode_static_name(),
        get_ode_shared_name(),
        get_anthem_static_name(),
        get_anthem_shared_name()
    ]
