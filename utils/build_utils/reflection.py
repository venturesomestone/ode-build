#===---------------------------- reflection.py ---------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (C) 2019 Venturesome Stone
# All rights reserved

"""The support module containing the utilities for Python modules."""


import importlib
import os
import sys

from script_support import data

from script_support.variables import ANTHEM_SOURCE_ROOT, ANTHEM_REPO_NAME

from . import diagnostics

from .mapping import Mapping


PRODUCT_PACKAGE = "products"
CHECKOUT_MODULE = "checkout.py"
BUILD_MODULE = "build.py"
CMAKE_MODULE = "cmake.py"
DIRECTORY_MODULE = "directory.py"

COMMON_PRODUCT = Mapping(key="common")

ANTHEM_PATH = os.path.join(ANTHEM_SOURCE_ROOT, ANTHEM_REPO_NAME, "utils")

PRODUCT_PATH = os.path.join(ANTHEM_PATH, "products")


def load_module(name, path):
    """
    Loads a Python module.

    name -- the name of the module.
    path -- the path to the module file.
    """
    diagnostics.trace("The product path: {}".format(path))
    diagnostics.trace("The name of the module: {}".format(name))
    diagnostics.trace("Loading module {} from file {}".format(name, path))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        else:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(name, path).load_module()
            return module
    else:
        import imp
        module = imp.load_source(name, path)
        return module


def get_module_attribute(name, path, attr):
    """
    Gets an attribute from a Python module.

    name -- the name of the module.
    path -- the path to the module file.
    attr -- the name of the attribute to get.
    """
    module = load_module(name, path)
    return getattr(module, attr)


def has_module_attribute(name, path, attr):
    """
    Check whether a Python module has an attribute.

    name -- the name of the module.
    path -- the path to the module file.
    attr -- the name of the attribute to check.
    """
    module = load_module(name, path)
    if hasattr(module, attr):
        diagnostics.trace("Module {} has attribute '{}'".format(name, attr))
    else:
        diagnostics.trace(
            "Module {} doesn't have attribute '{}'".format(name, attr))
    return hasattr(module, attr)


def product_checkout_call(product, function, *args, **kwargs):
    """
    Call a function in a product module.

    product -- the product.
    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    path = os.path.join(PRODUCT_PATH, product.key, CHECKOUT_MODULE)
    return get_module_attribute(product.key, path, function)(*args, **kwargs)


def build_call(product, function, *args, **kwargs):
    """
    Call a function in a product module.

    product -- the product.
    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    path = os.path.join(PRODUCT_PATH, product.key, BUILD_MODULE)
    return get_module_attribute(product.key, path, function)(*args, **kwargs)


def build_function_exists(product, function):
    """
    Check whether a function exists in a product module.

    product -- the product.
    function -- the name of the function.
    """
    path = os.path.join(PRODUCT_PATH, product.key, BUILD_MODULE)
    return has_module_attribute(product.key, path, function)


def product_exists(product):
    """
    Check whether a product module exists.

    product -- the product.
    """
    path = os.path.join(PRODUCT_PATH, product.key)
    diagnostics.trace("Looking for module {}".format(path))
    return os.path.isdir(path)


def config_value(variable):
    """Get a configuration value from Unsung Anthem."""
    name = "config"
    path = os.path.join(ANTHEM_PATH, "config.py")
    return get_module_attribute(name, path, variable)


def product_config_value(variable):
    """Get a product configuration value from Unsung Anthem."""
    name = "product_config"
    path = os.path.join(PRODUCT_PATH, "config.py")
    return get_module_attribute(name, path, variable)


def anthem_common_build_call(function, *args, **kwargs):
    """
    Call a function in the common build module in the Unsung Anthem repository.

    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    path = os.path.join(PRODUCT_PATH, COMMON_PRODUCT.key, BUILD_MODULE)
    return get_module_attribute(COMMON_PRODUCT.key, path, function)(
        *args, **kwargs)


def anthem_common_cmake_call(function, *args, **kwargs):
    """
    Call a function in the common CMake module in the Unsung Anthem repository.

    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    path = os.path.join(PRODUCT_PATH, COMMON_PRODUCT.key, CMAKE_MODULE)
    return get_module_attribute(COMMON_PRODUCT.key, path, function)(
        *args, **kwargs)


def anthem_common_directory_call(function, *args, **kwargs):
    """
    Call a function in the common directory module in the Unsung Anthem
    repository.

    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    path = os.path.join(PRODUCT_PATH, COMMON_PRODUCT.key, DIRECTORY_MODULE)
    return get_module_attribute(COMMON_PRODUCT.key, path, function)(
        *args, **kwargs)
