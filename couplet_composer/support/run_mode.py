# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains a helper enumeration that represents
the selected run mode of the build script.
"""

from enum import Enum, unique


@unique
class RunMode(Enum):
    """An enumeration that represents the possible run modes of
    the build script.
    """
    preset = "preset"
    configure = "configure"
    compose = "compose"
