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

from .mapping import Mapping


PRODUCT_PACKAGE = "products"
CHECKOUT_MODULE = "checkout.py"
BUILD_MODULE = "build.py"
CMAKE_MODULE = "cmake.py"
DIRECTORY_MODULE = "directory.py"

COMMON_PRODUCT = Mapping(key="common")

PRODUCT_PATH = os.path.join(
    ANTHEM_SOURCE_ROOT, ANTHEM_REPO_NAME, "utils", "products")


def product_checkout_call(product, function, *args, **kwargs):
    """
    Call a function in a product module.

    product -- the product.
    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    name = product.key
    file = os.path.join(PRODUCT_PATH, product.key, CHECKOUT_MODULE)
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            diagnostics.trace("Loading package {} from file {}".format(
                CHECKOUT_MODULE, file))
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            getattr(package, function)(*args, **kwargs)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            getattr(package, function)(*args, **kwargs)
    else:
        import imp
        package = imp.load_source(name, file)
        getattr(package, function)(*args, **kwargs)


def get_build_call(product, function):
    """
    Get a function in a product module.

    product -- the product.
    function -- the name of the function.
    """
    name = product.key
    diagnostics.trace("The product path: {}".format(PRODUCT_PATH))
    diagnostics.trace("The product: {}".format(product))
    file = os.path.join(PRODUCT_PATH, product.key, BUILD_MODULE)
    diagnostics.trace(
        "Loading package {} from file {}".format(BUILD_MODULE, file))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return getattr(package, function)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            return getattr(package, function)
    else:
        import imp
        package = imp.load_source(name, file)
        return getattr(package, function)


def build_call(product, function, *args, **kwargs):
    """
    Call a function in a product module.

    product -- the product.
    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    return get_build_call(product, function)(*args, **kwargs)


def build_function_exists(product, function):
    """
    Check whether a function exists in a product module.

    product -- the product.
    function -- the name of the function.
    """
    name = product.key
    diagnostics.trace("The product path: {}".format(PRODUCT_PATH))
    diagnostics.trace("The product: {}".format(product))
    file = os.path.join(PRODUCT_PATH, product.key, BUILD_MODULE)
    diagnostics.trace(
        "Loading package {} from file {}".format(BUILD_MODULE, file))

    def _hasattr(package, function):
        if hasattr(package, function):
            diagnostics.trace("Package {} has function '{}'".format(
                file, function))
        else:
            diagnostics.trace(
                "Package {} doesn't have function '{}'".format(
                    file, function))
        return hasattr(package, function)
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return _hasattr(package, function)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            return _hasattr(package, function)
    else:
        import imp
        package = imp.load_source(name, file)
        return _hasattr(package, function)


def product_exists(product):
    """
    Check whether a product module exists.

    product -- the product.
    """
    file = os.path.join(PRODUCT_PATH, product.key)
    diagnostics.trace("Looking for module {}".format(file))
    return os.path.isdir(file)


def anthem_config_value(variable):
    """Get a configuration value from Unsung Anthem."""
    name = "config"
    file = os.path.join(PRODUCT_PATH, "config.py")
    diagnostics.trace(
        "Loading package {} from file {}".format(name, file))
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


def get_anthem_common_build_call(function):
    """
    Get a function in the common build module in the Unsung Anthem repository.

    function -- the name of the function.
    """
    name = COMMON_PRODUCT.key
    diagnostics.trace("The product path: {}".format(PRODUCT_PATH))
    diagnostics.trace("The product: {}".format(COMMON_PRODUCT))
    file = os.path.join(PRODUCT_PATH, COMMON_PRODUCT.key, BUILD_MODULE)
    diagnostics.trace(
        "Loading package {} from file {}".format(BUILD_MODULE, file))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return getattr(package, function)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            return getattr(package, function)
    else:
        import imp
        package = imp.load_source(name, file)
        return getattr(package, function)


def anthem_common_build_call(function, *args, **kwargs):
    """
    Call a function in the common build module in the Unsung Anthem repository.

    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    return get_anthem_common_build_call(function)(*args, **kwargs)


def get_anthem_common_cmake_call(function):
    """
    Get a function in the common CMake module in the Unsung Anthem repository.

    function -- the name of the function.
    """
    name = COMMON_PRODUCT.key
    diagnostics.trace("The product path: {}".format(PRODUCT_PATH))
    diagnostics.trace("The product: {}".format(COMMON_PRODUCT))
    file = os.path.join(PRODUCT_PATH, COMMON_PRODUCT.key, CMAKE_MODULE)
    diagnostics.trace(
        "Loading package {} from file {}".format(CMAKE_MODULE, file))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return getattr(package, function)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            return getattr(package, function)
    else:
        import imp
        package = imp.load_source(name, file)
        return getattr(package, function)


def anthem_common_cmake_call(function, *args, **kwargs):
    """
    Call a function in the common CMake module in the Unsung Anthem repository.

    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    return get_anthem_common_cmake_call(function)(*args, **kwargs)


def get_anthem_common_directory_call(function):
    """
    Get a function in the common directory module in the Unsung Anthem
    repository.

    function -- the name of the function.
    """
    name = COMMON_PRODUCT.key
    diagnostics.trace("The product path: {}".format(PRODUCT_PATH))
    diagnostics.trace("The product: {}".format(COMMON_PRODUCT))
    file = os.path.join(PRODUCT_PATH, COMMON_PRODUCT.key, DIRECTORY_MODULE)
    diagnostics.trace(
        "Loading package {} from file {}".format(DIRECTORY_MODULE, file))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, file)
            package = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(package)
            return getattr(package, function)
        else:
            from importlib.machinery import SourceFileLoader
            package = SourceFileLoader(name, file).load_module()
            return getattr(package, function)
    else:
        import imp
        package = imp.load_source(name, file)
        return getattr(package, function)


def anthem_common_directory_call(function, *args, **kwargs):
    """
    Call a function in the common directory module in the Unsung Anthem
    repository.

    function -- the name of the function.
    args -- the positional arguments to be passed into the function.
    kwargs -- the key-value arguments to be passed into the function.
    """
    return get_anthem_common_directory_call(function)(*args, **kwargs)
