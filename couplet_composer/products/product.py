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

import logging
import os

from ..support.variables import DOWNLOAD_DIR

from ..util import shell


class Product(object):
    """
    The base type of types that represent the products that are
    required or built by the composer.
    """
    def __init__(self, version):
        """Constructs the product."""
        self.version = version
        logging.debug(
            "Created the product %s with version %s",
            self.get_product_key(),
            self.version
        )

    def resolve_download_root(self):
        """
        Resolves the directory where all the sources of the
        different versions of the product are downloaded to.
        """
        return os.path.join(DOWNLOAD_DIR, self.get_product_key())

    def resolve_download_dir(self):
        """
        Resolves the directory where the sources of the current
        version of the product are downloaded to.
        """
        return os.path.join(self.resolve_download_root(), self.version)

    def create_download_dir(self):
        """
        Creates the directory where the sources of the current
        version of the product are downloaded to.
        """
        shell.makedirs(self.resolve_download_dir())

    def destroy_download_dir(self):
        """
        Destroys the directory where the sources of the current
        version of the product are downloaded to.
        """
        shell.rmtree(self.resolve_download_dir())

    @classmethod
    def get_product_key(cls):
        """
        Gives the identifier-style name to use for this product.
        """
        return cls.__name__.lower()
