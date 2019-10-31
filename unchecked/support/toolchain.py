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

"""This support module handles the toolchain configuration."""

import logging
import os
import platform

from functools import partial

from .variables import ODE_BUILD_ROOT

from ..util import xcrun

from ..util.which import where, which

from .. import config


__all__ = ["write_toolchain", "read_toolchain", "host_toolchain"]


def target_toolchain_file(target):
    """
    Calculates path to the file that contains the written
    toolchain information for the given platform.
    """
    return os.path.join(ODE_BUILD_ROOT, "toolchain-{}".format(target))


# TODO This function essentially does nothing
def write_toolchain(toolchain, target):
    """
    Writes the toolchain to a JSON to be read later by the build.
    """
    ret = dict()
    ret[target] = dict()
    for key, value in toolchain.items():
        ret[target][key] = value
    return ret


# TODO This function essentially does nothing
def read_toolchain(target, json):
    """Reads the toolchain from a JSON data."""
    toolchain = dict()
    for key, value in json[target].items():
        toolchain[key] = value
    return toolchain


def _register_tool_names():
    """Registers the names for the tools for the search."""
    sys = platform.system()
    return {
        "cc": "clang-cl" if sys == "Windows" else "clang",
        "cxx": "clang-cl" if sys == "Windows" else "clang++",
        "msbuild": "msbuild",
        "ninja": "ninja",
        "cmake": "cmake",
        "git": "git",
        "make": "make"
    }


def _find_tools(tools, target, json, func):
    """Finds the executables of the given tools."""
    tool_dict = {}
    for key, name in tools.items():
        logging.debug("Looking for %s", name)
        found = func(cmd=name)
        if json is not None and target in json \
                and json[target] is not None \
                and key in json[target] \
                and json[target][key] is not None:
            logging.debug("%s is defined in the toolchain JSON", key)
            found = json[target][key]
        if found is None:
            logging.debug("%s wasn't found", key)
            tool_dict[key] = None
        else:
            logging.debug("Found %s", found)
            tool_dict[key] = found
    return tool_dict


def _mac_os(tools, target, json):
    """Finds the tools in the toolchain on macOS."""
    logging.debug("Creating toolchain for Darwin")
    # NOTE: xcrun searches from developer tools directory *and* from PATH.
    # Relatively slow, but 'which' is not necessary for Darwin.
    return _find_tools(tools, target, json, partial(xcrun.find))


def _unix(tools, target, json):
    """
    Finds the tools in the toolchain on a generic Unix system.
    """
    logging.debug("Creating toolchain for Unix-like system")
    return _find_tools(tools, target, json, which)


def _linux(tools, target, json):
    """Finds the tools in the toolchain on Linux."""
    logging.debug("Creating toolchain for Linux")
    return _unix(tools, target, json)


def _free_bsd(tools, target, json):
    """Finds the tools in the toolchain on FreeBSD."""
    logging.debug("Creating toolchain for FreeBSD")
    return _unix(tools, target, json)


def _cygwin(tools, target, json):
    """Finds the tools in the toolchain on Cygwin."""
    logging.debug("Creating toolchain for Cygwin")
    return _unix(tools, target, json)


def _windows(tools, target, json):
    """Finds the tools in the toolchain on Windows."""
    logging.debug("Creating toolchain for Windows")
    def _find(cmd):
        found = where(cmd)
        if found is not None:
            return found.replace("/c/", "C:\\").replace("/", "\\")
        return found
    return _find_tools(tools, target, json, _find)


def host_toolchain(json):
    """Makes the toolchain for the current host platform."""
    tool_names = _register_tool_names()
    sys = platform.system()
    target = config.ARGS.host_target
    if sys == "Darwin":
        return _mac_os(tool_names, target, json)
    elif sys == "Linux":
        return _linux(tool_names, target, json)
    elif sys == "FreeBSD":
        return _free_bsd(tool_names, target, json)
    elif sys.startswith("CYGWIN"):
        return _cygwin(tool_names, target, json)
    elif sys == "Windows":
        return _windows(tool_names, target, json)
    raise NotImplementedError(
        "The platform '{}' does not have a defined toolchain".format(sys)
    )
