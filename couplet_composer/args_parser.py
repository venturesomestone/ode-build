# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
A module that contains functions for creating the parser for the
command line arguments and options of the build script.
"""

import argparse
import textwrap

from .support.command_line import DESCRIPTION, EPILOG
from .support.run_mode import RunMode


def _add_common_arguments(parser):
    """Modifies the given arguments parser by adding the common
    command line options to it.

    Args:
        parser (ArgumentParser):  The parser that is modified.

    Returns:
        The given arguments parser modified.
    """
    return parser


def _add_common_build_arguments(parser):
    """Modifies the given arguments parser by adding the common
    command line options related to the build of the project to
    it.

    Args:
        parser (ArgumentParser):  The parser that is modified.

    Returns:
        The given arguments parser modified.
    """
    return parser


def create_args_parser() -> argparse.ArgumentParser:
    """Creates the parser for the command line arguments.

    Returns:
        An object of the type ArgumentParser.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)

    # TODO Add the options common to every run mode here.

    # --------------------------------------------------------- #
    # Sub-commands

    subparsers = parser.add_subparsers(dest="run_mode")

    preset = _add_common_arguments(subparsers.add_parser(RunMode.preset.value))
    configure = _add_common_build_arguments(
        _add_common_arguments(
            subparsers.add_parser(RunMode.preset.value)
        )
    )
    compose = _add_common_build_arguments(
        _add_common_arguments(subparsers.add_parser(RunMode.preset.value))
    )

    return parser
