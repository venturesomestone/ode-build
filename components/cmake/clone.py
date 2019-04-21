# ------------------------------------------------------------- #
#                 Obliging Ode & Unsung Anthem
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""
This support module has the info necessary for downloading CMake.
"""

from util import workspace


SOURCE = False
GITHUB = False


def resolve_platform():
    """
    Resolve the platform which is used in the URL from which CMake is
    downloaded.
    """
    product = data.build.products.cmake
    if platform.system() == "Windows":
        return "win32-x86"
    elif platform.system() == "Linux":
        return _resolve_linux()
    elif platform.system() == "Darwin":
        return _resolve_darwin()

    diagnostics.warn(
        "{} will not be downloaded as the platform is not "
        "supported".format(product.repr))
    return None


def get_dependency(component):
    """Downloads the dependency."""
    with workspace.clone_directory(component):
        version_data = component.version_data
        major_minor = "{}.{}".format(version_data.major, version_data.minor)
