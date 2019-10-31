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

"""
This module contains the functions for common set-up procedures.
"""

import importlib
import json
import logging
import os
import sys
import time

from .support.toolchain import host_toolchain, target_toolchain_file

from .support.values import PACKAGE_NAME

from .support.variables import COMPOSER_ROOT, DOWNLOAD_STATUS_FILE

from .util import shell

from . import config


def _set_up_tool_dependencies(json_data):
    return dict(json_data)


def _create_products():
    config.PRODUCTS = {}

    for product_key, product_data in config.TOOLS.items():
        logging.debug(
            "Creating the product for %s with data %s",
            product_key,
            product_data
        )
        product_module_name = "{}.products.{}".format(
            PACKAGE_NAME,
            product_key
        )
        product_module = importlib.import_module(product_module_name)
        logging.debug("Imported module %s", product_module_name)
        config.PRODUCTS[product_key] = getattr(
            product_module,
            product_data["class"]
        )(product_data["version"])


def _count_down_clean_delay():
    def _impl_write(index):
        sys.stdout.write("\b{!s}".format(index))
        sys.stdout.flush()
        time.sleep(1)
        return index
    sys.stdout.write("Starting a clean build in  ")
    index_list = [_impl_write(i) for i in reversed(range(0, 4))]
    print("\b\b\b\bnow.")
    return index_list


def _clean():
    """
    Deletes the existing build directories for a clean build.
    This function needs the dependency and product data to
    properly clean up the directories.
    """
    shell.rm(DOWNLOAD_STATUS_FILE)
    for product in config.PRODUCTS.values():
        product.destroy_download_dir()


def set_up():
    """Sets up the runtime values for the composer."""

    # Set up the tool dependency data
    tools_data = None
    tools_file = os.path.join(COMPOSER_ROOT, "tools.json")

    logging.debug(
        "Loading the tool dependency data from a file: %s",
        tools_file
    )

    with open(tools_file) as f:
        tools_data = json.load(f)
    config.TOOLS = _set_up_tool_dependencies(tools_data)

    logging.debug("The tool dependency data is: %s", config.TOOLS)

    _create_products()

    if config.ARGS.clean:
        _count_down_clean_delay()
        _clean()

    # Get the saved toolchain
    toolchain_data = None
    toolchain_file = target_toolchain_file(config.ARGS.host_target)

    if os.path.exists(toolchain_file):
        logging.debug("Loading the toolchain from a file: %s", toolchain_file)
        with open(toolchain_file) as json_file:
            toolchain_data = json.load(json_file)

    config.TOOLCHAIN = host_toolchain(toolchain_data)
