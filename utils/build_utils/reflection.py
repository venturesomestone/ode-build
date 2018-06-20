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
    file = os.path.join(
        data.build.args.products_path, product, CHECKOUT_MODULE)
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            diagnostics.trace("Loading package {} from file {}".format(
                CHECKOUT_MODULE, file))
            spec = importlib.util.spec_from_file_location(
                CHECKOUT_MODULE, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            getattr(package, function)(*args, **kwargs)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(CHECKOUT_MODULE, file).load_module()
            getattr(package, function)(*args, **kwargs)
    else:
        import imp
        package = imp.load_source(CHECKOUT_MODULE, file)
        getattr(package, function)(*args, **kwargs)


def get_build_call(product, function):
    """
    Get a function in a product module.

    product -- the name of the product.
    function -- the name of the function.
    """
    file = os.path.join(data.build.args.products_path, product, BUILD_MODULE)
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            diagnostics.trace("Loading package {} from file {}".format(
                BUILD_MODULE, file))
            spec = importlib.util.spec_from_file_location(BUILD_MODULE, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return getattr(package, function)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(BUILD_MODULE, file).load_module()
            return getattr(package, function)
    else:
        import imp
        package = imp.load_source(BUILD_MODULE, file)
        return getattr(package, function)


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
    file = os.path.join(data.build.args.products_path, product, BUILD_MODULE)
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            diagnostics.trace("Loading package {} from file {}".format(
                BUILD_MODULE, file))
            spec = importlib.util.spec_from_file_location(BUILD_MODULE, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            if hasattr(package, function):
                diagnostics.trace(
                    "Package {} has function '{}'".format(file, function))
            else:
                diagnostics.trace(
                    "Package {} doesn't have function '{}'".format(
                        file, function))
            return hasattr(package, function)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(BUILD_MODULE, file).load_module()
            if hasattr(package, function):
                diagnostics.trace(
                    "Package {} has function '{}'".format(file, function))
            else:
                diagnostics.trace(
                    "Package {} doesn't have function '{}'".format(
                        file, function))
            return hasattr(package, function)
    else:
        import imp
        package = imp.load_source(BUILD_MODULE, file)
        if hasattr(package, function):
            diagnostics.trace("Package {} has function '{}'".format(
                file, function))
        else:
            diagnostics.trace("Package {} doesn't have function '{}'".format(
                file, function))
        return hasattr(package, function)


def product_exists(product):
    """
    Check whether a product module exists.

    product -- the name of the product.
    """
    file = os.path.join(data.build.args.products_path, product)
    diagnostics.trace("Looking for module {}".format(file))
    return os.path.isdir(file)


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
