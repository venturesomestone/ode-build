# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains a helper enumeration that represents
the possible build variants.
"""

from enum import Enum, unique


@unique
class BuildVariant(Enum):
    """An enumeration that represents the possible build
    variants.
    """
    debug = "Debug"
    release_debug_info = "RelWithDebInfo"
    release = "Release"
    minimum_size_release = "MinSizeRel"
