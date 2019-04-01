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
This module is a wrapper around the standard argparse that
extends it with support for multi-destination actions, an
expressive DSL for constructing parsers and more argument types.
This module exposes a strict super-set of the argparse API and is
meant to be used as a drop-in replacement.
"""


from argparse import \
    ArgumentDefaultsHelpFormatter, ArgumentError, ArgumentTypeError, \
    FileType, HelpFormatter, Namespace, RawDescriptionHelpFormatter, \
    RawTextHelpFormatter
from argparse import ONE_OR_MORE, OPTIONAL, SUPPRESS, ZERO_OR_MORE

from .actions import Action, Nargs
from .parser import ArgumentParser
from .types import \
    BoolType, ClangVersionType, CompilerVersion, PathType, RegexType, \
    ShellSplitType, OdeVersionType


__all__ = [
    "Action",
    "ArgumentDefaultsHelpFormatter",
    "ArgumentError",
    "ArgumentParser",
    "ArgumentTypeError",
    "HelpFormatter",
    "Namespace",
    "Nargs",
    "RawDescriptionHelpFormatter",
    "RawTextHelpFormatter",

    "CompilerVersion",
    "BoolType",
    "FileType",
    "PathType",
    "RegexType",
    "ClangVersionType",
    "OdeVersionType",
    "ShellSplitType",

    "SUPPRESS",
    "OPTIONAL",
    "ZERO_OR_MORE",
    "ONE_OR_MORE"
]
