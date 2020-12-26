# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains a helper enumeration that represents
the possible installation statuses of the tools of the build
script.
"""

from enum import Enum, auto, unique


@unique
class InstallStatus(Enum):
    """An enumeration that represents the possible installation
    statuses of the tools of the build script.
    """
    none = auto()
    system = auto()
    local = auto()
