# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains a helper enumeration that represents
the possible operating systems for the build.
"""

from enum import Enum, unique


@unique
class System(Enum):
    """An enumeration that represents the possible operating
    systems for the build.
    """
    linux = "linux"
    windows = "windows"
    darwin = "darwin"
