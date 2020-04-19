# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
The version data of Couplet Composer. The version number is given
according to Semantic Versioning.
"""


def get_release_version():
    """
    Gives the current release version data of Couplet Composer
    and, thus, returns three values: the major version number,
    the minor version number, and the patch version number.
    """
    return 0, 12, 0


def get_version():
    """
    Gives a string that represents the current version of Couplet
    Composer.
    """
    return ".".join([str(n) for n in get_release_version()]) + "-dev.1"


__version__ = get_version()
