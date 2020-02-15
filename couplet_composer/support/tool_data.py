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
# that is used if the tool is looked for from the system or a
# predefined path to the tool executable. TODO: Parameters
#
# use_predefined_path -- Returns boolean indicating whether or
# not the function 'get_searched_tool' contains a predefined path
# to the tool executable. TODO: Parameters
#
# get_required_local_version -- Returns a string that represents
# version of the tool that is downloaded when the tool isn't
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
    "use_predefined_path",
    "get_required_local_version",
    "get_local_executable",
    "install_tool"
])


# The type 'CompilerToolPair' represents data of a compiler on a
# system that has separate executables for C and C++. It also
# contains a name for the whole compiler toolchain.
CompilerToolPair = namedtuple("CompilerToolPair", [
    "get_tool_name",
    "cc",
    "cxx"
])


@cached
def list_tool_types():
    """
    Creates a list of the possible tool types for the toolchain.
    """
    return ["compiler", "cmake", "build_system", "scm", "make"]


def _create_tool_data(module_name, tool_name):
    """
    Creates a common ToolData object of a tool for toolchain.
    This function isn't totally pure as it imports the module
    using importlib.

    module_name -- The name of the module from which the various
    functions are got.

    tool_name -- The name of the tool.
    """
    package_name = "{}.tools.{}".format(
        get_project_package_name(),
        module_name
    )
    tool_module = importlib.import_module(package_name)
    return ToolData(
        get_tool_key=lambda: module_name,
        get_tool_name=lambda: tool_name,
        get_searched_tool=lambda: module_name,
        use_predefined_path=lambda: False,
        get_required_local_version=getattr(tool_module, "get_version"),
        get_local_executable=getattr(tool_module, "get_local_executable"),
        install_tool=getattr(tool_module, "install_tool")
    )


def create_unix_compiler_tool_data(
    cc_name,
    cxx_name,
    tool_name,
    version=None,
    cc_path=None,
    cxx_path=None
):
    """
    Creates the ToolData object of a compiler tool on a Unix
    system.

    cc_name -- The name of the C compiler.

    cxx_name -- The name of the C++ compiler.

    tool_name -- The name of the tool.

    version -- The version of compiler tool to search for.

    cc_path -- An optional predefined path to the C compiler.

    cxx_path -- An optional predefined path to the C++ compiler.
    """
    def _create_compiler_tool_data(tool_key):
        return ToolData(
            get_tool_key=lambda: tool_key,
            get_tool_name=lambda: tool_name,
            get_searched_tool=(lambda: tool_key) if not version
            else (lambda: "{}-{}".format(tool_key, version)),
            use_predefined_path=lambda: False,
            get_required_local_version=None,
            get_local_executable=None,
            install_tool=None
        )

    def _create_compiler_tool_data_with_path(tool_key, tool_path):
        return ToolData(
            get_tool_key=lambda: tool_key,
            get_tool_name=lambda: tool_name,
            get_searched_tool=lambda: tool_path,
            use_predefined_path=lambda: True,
            get_required_local_version=None,
            get_local_executable=None,
            install_tool=None
        )

    return CompilerToolPair(
        get_tool_name=lambda: tool_name,
        cc=_create_compiler_tool_data(tool_key=cc_name) if not cc_path
        else _create_compiler_tool_data_with_path(
            tool_key=cc_name,
            tool_path=cc_path
        ),
        cxx=_create_compiler_tool_data(tool_key=cxx_name) if not cxx_path
        else _create_compiler_tool_data_with_path(
            tool_key=cxx_name,
            tool_path=cxx_path
        )
    )


def create_windows_compiler_tool_data(
    tool_key,
    tool_name,
    version=None,
    tool_path=None
):
    """
    Creates the ToolData object of a compiler tool on a Windows
    system.

    tool_key -- The name of the compiler.

    tool_name -- The name of the tool.

    version -- The version of compiler tool to search for. This
    parameter isn't currently used in the function.

    tool_path -- An optional predefined path to the compiler.
    """
    return ToolData(
        get_tool_key=lambda: tool_key,
        get_tool_name=lambda: tool_name,
        get_searched_tool=(lambda: tool_name) if not tool_path
        else (lambda: tool_path),
        use_predefined_path=(lambda: True) if tool_path else (lambda: False),
        get_required_local_version=None,
        get_local_executable=None,
        install_tool=None
    )


def create_clang_tool_data(version=None, cc_path=None, cxx_path=None):
    """
    Creates the ToolData objects of Clang for toolchain. Returns
    a named tuple of type 'CompilerToolPair'.

    version -- The version of Clang to search for.

    cc_path -- An optional predefined path to the C compiler.

    cxx_path -- An optional predefined path to the C++ compiler.
    """
    return create_unix_compiler_tool_data(
        cc_name="clang",
        cxx_name="clang++",
        tool_name="Clang",
        version=version
    )


def create_gcc_tool_data(version=None, cc_path=None, cxx_path=None):
    """
    Creates the ToolData objects of GCC for toolchain. Returns
    a named tuple of type 'CompilerToolPair'.

    version -- The version of GCC to search for.

    cc_path -- An optional predefined path to the C compiler.

    cxx_path -- An optional predefined path to the C++ compiler.
    """
    return create_unix_compiler_tool_data(
        cc_name="gcc",
        cxx_name="g++",
        tool_name="GCC",
        version=version
    )


def create_msvc_tool_data(tool_path=None):
    """
    Creates the ToolData object of MSVC.

    tool_path -- An optional predefined path to the compiler.
    """
    return create_windows_compiler_tool_data(
        tool_key="cl",
        tool_name="MSVC",
        tool_path=tool_path
    )


def create_make_tool_data():
    """Creates the ToolData object of Make for toolchain."""
    return ToolData(
        get_tool_key=lambda: "make",
        get_tool_name=lambda: "Make",
        get_searched_tool=lambda: "make",
        use_predefined_path=lambda: False,
        get_required_local_version=None,
        get_local_executable=None,
        install_tool=None
    )


def create_msbuild_tool_data(tool_path=None):
    """
    Creates the ToolData object of MSBuild for toolchain.

    tool_path -- An optional predefined path to MSBuild.
    """
    if tool_path:
        return ToolData(
            get_tool_key=lambda: "msbuild",
            get_tool_name=lambda: "MSBuild",
            get_searched_tool=lambda: tool_path,
            use_predefined_path=lambda: True,
            get_required_local_version=None,
            get_local_executable=None,
            install_tool=None
        )
    else:
        return ToolData(
            get_tool_key=lambda: "msbuild",
            get_tool_name=lambda: "MSBuild",
            get_searched_tool=lambda: "msbuild",
            use_predefined_path=lambda: False,
            get_required_local_version=None,
            get_local_executable=None,
            install_tool=None
        )


def create_git_tool_data():
    """Creates the ToolData object of Git for toolchain."""
    return ToolData(
        get_tool_key=lambda: "git",
        get_tool_name=lambda: "Git",
        get_searched_tool=lambda: "git",
        use_predefined_path=lambda: False,
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
    return _create_tool_data(module_name="cmake", tool_name="CMake")


def create_ninja_tool_data():
    """
    Creates the ToolData object of Ninja for toolchain. This
    function isn't totally pure as it imports the module using
    importlib.
    """
    return _create_tool_data(module_name="ninja", tool_name="Ninja")
