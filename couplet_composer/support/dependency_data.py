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
This support module contains type DependencyData for creating the
dependencies and the functions for handling the creation of
DependencyData objects for each dependency for the project.
"""

import importlib

from collections import namedtuple

from .project_names import get_project_package_name


# The type 'DependencyData' represents the data to construct a
# dependency. Thus, the tuple contains various functions that the
# script utilizes when it constructs the dependencies.
#
# get_required_version -- Returns a string that represents the
# version of the dependency that is required by the project.
#
#  when the tool isn't
# found. Returns None if the tool can't be installed locally. The
# parameters for the function are: target, host_system
DependencyData = namedtuple("DependencyData", ["get_required_version"])


def create_dependency_data(module_name, data_node):
    """
    Creates a common DependencyData object of a dependency. This
    function isn't totally pure as it imports the module using
    importlib.

    module_name -- The name of the module from which the various
    functions are got.

    data_node -- The entry in the dependency JSON file containing
    the data for the dependency in question.
    """
    package_name = "{}.dependencies.{}".format(
        get_project_package_name(),
        module_name
    )
    dependency_module = importlib.import_module(package_name)
    return DependencyData(
        get_required_version=lambda: data_node["version"]
    )
