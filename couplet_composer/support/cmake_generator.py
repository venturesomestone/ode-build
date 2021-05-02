# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains a helper enumeration that represents
the possible CMake generators.
"""

from enum import Enum, unique


@unique
class CMakeGenerator(Enum):
    """An enumeration that represents the possible CMake
    generators.
    """
    ninja = "Ninja"
