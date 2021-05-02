# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains a helper enumeration that represents
the possible actions that can be performed on compressed archives
by the tar shell utility.
"""

from enum import Enum, auto, unique


@unique
class ArchiveAction(Enum):
    """An enumeration that represents the possible actions that
    can be performed on compressed archives by the tar shell
    utility.
    """
    extract = auto()
    unzip = auto()
