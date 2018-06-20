#===---------------------------- reflection.py ---------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (c) 2018 Venturesome Stone
# Licensed under GNU Affero General Public License v3.0

"""The support module containing the utilities for Python modules."""


import importlib
import os
import sys

from script_support import data

from script_support.variables import ANTHEM_SOURCE_ROOT, ANTHEM_REPO_NAME

from . import diagnostics


PRODUCT_PACKAGE = "products"
CHECKOUT_MODULE = "checkout"
BUILD_MODULE = "build"


def product_checkout_call(product, function, *args, **kwargs):
    """
    Call a function in a product module.

    product -- the name of the product.
    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    package = "{}.{}.{}".format(PRODUCT_PACKAGE, product.key, CHECKOUT_MODULE)
    diagnostics.trace("Importing package {}".format(package))
    product_module = importlib.import_module(package)
    diagnostics.trace("Imported package {}".format(package))
    getattr(product_module, function)(*args, **kwargs)


def get_build_call(product, function):
    """
    Get a function in a product module.

    product -- the name of the product.
    function -- the name of the function.
    """
    package = "{}.{}.{}".format(PRODUCT_PACKAGE, product.key, BUILD_MODULE)
    diagnostics.trace("Importing package {}".format(package))
    product_module = importlib.import_module(package)
    diagnostics.trace("Imported package {}".format(package))
    return getattr(product_module, function)


def build_call(product, function, *args, **kwargs):
    """
    Call a function in a product module.

    product -- the name of the product.
    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    return get_build_call(product, function)(*args, **kwargs)


def build_function_exists(product, function):
    """
    Check whether a function exists in a product module.

    product -- the name of the product.
    function -- the name of the function.
    """
    package = "{}.{}.{}".format(PRODUCT_PACKAGE, product.key, BUILD_MODULE)
    diagnostics.trace(
        "Importing package {} for checking whether function {} exists".format(
            package, function))
    product_module = importlib.import_module(package)
    diagnostics.trace("Imported package {}".format(package))
    if hasattr(product_module, function):
        diagnostics.trace("Package {} has function '{}'".format(
            package, function))
    else:
        diagnostics.trace("Package {} doesn't have function '{}'".format(
            package, function))
    return hasattr(product_module, function)


def product_exists(product):
    """
    Check whether a product module exists.

    product -- the name of the product.
    """
    package = "{}.{}".format(PRODUCT_PACKAGE, product.key)
    diagnostics.trace("Looking for package {}".format(package))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            return importlib.util.find_spec(package) is not None
        else:
            return importlib.find_loader(package) is not None
    import imp
    try:
        products_info = imp.find_module(PRODUCT_PACKAGE)
        products = imp.load_module(PRODUCT_PACKAGE, *products_info)
        diagnostics.trace("Found package {}".format(PRODUCT_PACKAGE))
        imp.find_module(product.key, products.__path__)
        diagnostics.trace("Found package {}".format(product.key))
        return True
    except ImportError:
        return False


def anthem_config_value(variable):
    """Get a configuration value from Unsung Anthem."""
    name = "config"
    file = os.path.join(
        ANTHEM_SOURCE_ROOT, ANTHEM_REPO_NAME, "utils", "config.py")
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return getattr(package, variable)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            return getattr(package, variable)
    else:
        import imp
        package = imp.load_source(name, file)
        return getattr(package, variable)


def import_product_package(name):
    """Get a product configuration value from Unsung Anthem."""
    file = os.path.join(data.build.args.products_path, name)
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return package
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            return package
    else:
        import imp
        package = imp.load_source(name, file)
        return package
