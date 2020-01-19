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
This support module contains type ToolData for creating the
toolchain and the functions for handling the creation of ToolData
objects for each tool for the toolchain.
"""

import importlib

from collections import namedtuple

from .project_names import get_project_package_name

from ..util.cache import cached


# The type 'ToolData' represents the data to construct a tool.
# Thus, the tuple contains various functions that the toolchain
# utilizes when it constructs itself.
#
# get_tool_key -- Returns the simple lower-case name of the tool.
#
# get_tool_name -- Returns the name of the tool.
#
# get_searched_tool -- Returns a string that represents the name
# that is used if the tool is looked for from the system. TODO:
# Parameters
#
# get_required_local_version -- Returns a string that represents
# version of the tool that is donwloaded when the tool isn't
# found. Returns None if the tool can't be installed locally. The
# parameters for the function are: target, host_system
#
# get_local_executable -- Returns path to the local executable of
# the tool. Returns None if the tool can't be installed locally.
# The parameters for the function are: tools_root, version,
# target, host_system
#
# install_tool -- Installs the tool if it wasn't found on the
# system. The tool is downloaded and possibly built. The function
# ought to return path to the installed tool. The parameters for
# the function are: build_root, tools_root, version, target,
# host_system, github_user_agent, github_api_token, dry_run,
# print_debug
ToolData = namedtuple("ToolData", [
    "get_tool_key",
    "get_tool_name",
    "get_searched_tool",
    "get_required_local_version",
    "get_local_executable",
    "install_tool"
])


# The type 'CompilerToolPair' represents data of a compiler on a
# system that has separate executables for C and C++.
CompilerToolPair = namedtuple("CompilerToolPair", ["cc", "cxx"])


@cached
def list_tool_types():
    """
    Creates a list of the possible tool types for the toolchain.
    """
    return ["compiler", "cmake", "build_system", "scm", "make"]


def _create_tool_data(module_name):
    """
    Creates a common ToolData object of a tool for toolchain.
    This function isn't totally pure as it imports the module
    using importlib.

    module_name -- The name of the module from which the various
    functions are got.
    """
    package_name = "{}.tools.{}".format(
        get_project_package_name(),
        module_name
    )
    tool_module = importlib.import_module(package_name)
    return ToolData(
        get_tool_type=getattr(tool_module, "get_tool_type"),
        get_searched_tool=lambda: module_name,
        get_required_local_version=getattr(tool_module, "get_version"),
        get_local_executable=getattr(tool_module, "get_local_executable"),
        install_tool=getattr(tool_module, "install_tool")
    )


def create_compiler_tool_data(tool_type, tool_name, version=None):
    """
    Creates the ToolData object of a generic compiler tool.

    tool_type -- The type of the tool.

    tool_name -- The name of the tool.

    version -- The version of compiler tool to search for.
    """
    return ToolData(
        get_tool_type=lambda: tool_type,
        get_searched_tool=(lambda: tool_name)
        if not version
        else (lambda: "{}-{}".format(tool_name, version)),
        get_required_local_version=None,
        get_local_executable=None,
        install_tool=None
    )


def create_clang_tool_data(version=None):
    """
    Creates the ToolData object of Clang for toolchain.

    version -- The version of Clang to search for.
    """
    return create_compiler_tool_data(
        tool_type="cc",
        tool_name="clang",
        version=version
    )


def create_clangxx_tool_data(version=None):
    """
    Creates the ToolData object of Clang++ for toolchain.

    version -- The version of Clang to search for.
    """
    return create_compiler_tool_data(
        tool_type="cxx",
        tool_name="clang++",
        version=version
    )


def create_gcc_tool_data(version=None):
    """
    Creates the ToolData object of GCC for toolchain.

    version -- The version of GCC to search for.
    """
    return create_compiler_tool_data(
        tool_type="cc",
        tool_name="gcc",
        version=version
    )


def create_gxx_tool_data(version=None):
    """
    Creates the ToolData object of G++ for toolchain.

    version -- The version of GCC to search for.
    """
    return create_compiler_tool_data(
        tool_type="cxx",
        tool_name="g++",
        version=version
    )


def create_msvc_tool_data(version=None):
    """
    Creates the ToolData object of MSVC compiler.

    version -- The version of GCC to search for.
    """
    return create_compiler_tool_data(
        tool_type="cc",
        tool_name="cl",
        version=version
    )


def create_make_tool_data():
    """Creates the ToolData object of Make for toolchain."""
    return ToolData(
        get_tool_type=lambda: "build_system",
        get_searched_tool=lambda: "make",
        get_required_local_version=None,
        get_local_executable=None,
        install_tool=None
    )


def create_msbuild_tool_data():
    """Creates the ToolData object of MSBuild for toolchain."""
    return ToolData(
        get_tool_type=lambda: "build_system",
        get_searched_tool=lambda: "msbuild",
        get_required_local_version=None,
        get_local_executable=None,
        install_tool=None
    )


def create_git_tool_data():
    """Creates the ToolData object of Git for toolchain."""
    return ToolData(
        get_tool_type=lambda: "git",
        get_searched_tool=lambda: "git",
        get_required_local_version=None,
        get_local_executable=None,
        install_tool=None
    )


def create_cmake_tool_data():
    """
    Creates the ToolData object of CMake for toolchain. This
    function isn't totally pure as it imports the module using
    importlib.
    """
    return _create_tool_data("cmake")


def create_ninja_tool_data():
    """
    Creates the ToolData object of Ninja for toolchain. This
    function isn't totally pure as it imports the module using
    importlib.
    """
    return _create_tool_data("ninja")
