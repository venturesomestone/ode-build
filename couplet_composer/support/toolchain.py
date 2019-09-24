# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem project.
#
# Copyright 2019 Antti Kivi
# Licensed under the EUPL, version 1.2
#
# ------------------------------------------------------------- #

"""This support module handles the toolchain configuration."""

import os
import platform

from functools import partial

from absl import logging

from .variables import ODE_BUILD_ROOT

from ..util import xcrun

from ..util.mapping import Mapping

from ..util.which import where, which

from ..flags import FLAGS


__all__ = ["write_toolchain", "read_toolchain", "host_toolchain"]


def target_toolchain_file(target):
    """
    Calculates path to the file that contains the written
    toolchain information for the given platform.
    """
    return os.path.join(
        ODE_BUILD_ROOT,
        "toolchain-{}-{}".format(FLAGS["ode-version"].value, target)
    )


def write_toolchain(toolchain, target):
    """
    Writes the toolchain to a JSON to be read later by the build.
    """
    ret = dict()
    ret[target] = dict()
    for key, value in toolchain.items():
        ret[target][key] = value
    return ret


def read_toolchain(target, json):
    """Reads the toolchain from a JSON data."""
    toolchain = dict()
    for key, value in json[target].items():
        toolchain[key] = value
    return toolchain


def _register_tools():
    tools = Mapping()
    sys = platform.system()
    # if args.search_cc is not None:
    #     tools.cc = args.search_cc
    # else:
    #     tools.cc = "clang-cl" if sys == "Windows" else "clang"
    tools.cc = "clang-cl" if sys == "Windows" else "clang"
    # if args.search_cxx is not None:
    #     tools.cxx = args.search_cxx
    # else:
    #     tools.cxx = "clang-cl" if sys == "Windows" else "clang++"
    tools.cxx = "clang-cl" if sys == "Windows" else "clang++"
    tools.msbuild = "msbuild"
    tools.ninja = "ninja"
    tools.cmake = "cmake"
    tools.git = "git"
    tools.make = "make"
    if FLAGS.xvfb:
        tools.xvfb_run = "xvfb-run"
    return tools


def _find_tools(tools, target, json, func):
    """Finds the executables of the given tools."""
    tool_mapping = Mapping()
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
            tool_mapping[key] = None
        else:
            logging.debug("Found %s", found)
            tool_mapping[key] = found
    return tool_mapping


def _mac_os(tools, target, json):
    """Finds the tools in the toolchain on macOS."""
    # NOTE: xcrun searches from developer tools directory *and* from PATH.
    # Relatively slow, but 'which' is not necessary for Darwin.
    return _find_tools(tools, target, json, partial(xcrun.find))


def _unix(tools, target, json):
    """
    Finds the tools in the toolchain on a generic Unix system.
    """
    return _find_tools(tools, target, json, which)


def _linux(tools, target, json):
    """Finds the tools in the toolchain on Linux."""
    return unix(tools, target, json)


def _free_bsd(tools, target, json):
    """Finds the tools in the toolchain on FreeBSD."""
    return unix(tools, target, json)


def _cygwin(tools, target, json):
    """Finds the tools in the toolchain on Cygwin."""
    return unix(tools, target, json)


def _windows(tools, target, json):
    """Finds the tools in the toolchain on Windows."""
    def _find(cmd):
        found = where(cmd)
        if found is not None:
            return found.replace("/c/", "C:\\").replace("/", "\\")
        return found
    return _find_tools(tools, target, json, _find)


def host_toolchain(target, json):
    """Makes the toolchain for the current host platform."""
    tools = _register_tools()
    sys = platform.system()
    if sys == "Darwin":
        return _mac_os(tools, target, json)
    elif sys == "Linux":
        return _linux(tools, target, json)
    elif sys == "FreeBSD":
        return _free_bsd(tools, target, json)
    elif sys.startswith("CYGWIN"):
        return _cygwin(tools, target, json)
    elif sys == "Windows":
        return _windows(tools, target, json)
    raise NotImplementedError(
        "The platform '{}' does not have a defined toolchain".format(sys)
    )
