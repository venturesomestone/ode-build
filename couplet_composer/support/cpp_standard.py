# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains a helper enumeration that represents
the possible C++ standard version.
"""

from enum import Enum, unique


@unique
class CppStandard(Enum):
    """An enumeration that represents the possible C++ standards.
    """
    cpp17 = "c++17"
    cpp20 = "c++20"
