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

"""The version data of Couplet Composer."""


def get_release_version():
    """
    Gives the current release version data of Couplet Composer
    and, thus, returns three values: the major version number,
    the minor version number, and the patch version number.
    """
    return 0, 4, 1


def get_version():
    """
    Gives a string that represents the current version of Couplet
    Composer.
    """
    return ".".join([str(n) for n in get_release_version()])


__version__ = get_version()
