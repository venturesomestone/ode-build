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

from .product import Product


class CMake(Product):
    """The type that represent the CMake product."""
    def __init__(self, version_data):
        """Constructs the CMake product."""
        super(CMake, self).__init__("{}.{}.{}".format(
            version_data["major"],
            version_data["minor"],
            version_data["patch"]
        ))
        self.version_data = version_data
