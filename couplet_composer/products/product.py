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

import os

from ..support.variables import DOWNLOAD_DIR

from ..util import shell


class Product(object):
    """
    The base type of types that represent the products that are
    required or built by the composer.
    """
    def resolve_download_root(self):
        """
        Resolves the directory where all the sources of the
        different versions of the product are downloaded to.
        """
        return os.path.join(DOWNLOAD_DIR, self.get_product_key())

    def create_download_root(self):
        """
        Creates the directory where all the sources of the
        different versions of the product are downloaded to.
        """
        shell.makedirs(self.resolve_download_root())

    @classmethod
    def get_product_key(cls):
        """
        Gives the identifier-style name to use for this product.
        """
        return cls.__name__.lower()
