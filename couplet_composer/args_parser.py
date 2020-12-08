# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains functions for creating the parser for
the command line arguments and options of the build script.
"""

import multiprocessing

from argparse import ArgumentParser

from .support.command_line import DESCRIPTION, EPILOG

from .support.run_mode import RunMode

from .target import Target

from . import __version__


def _add_common_arguments(parser: ArgumentParser) -> ArgumentParser:
    """Modifies the given arguments parser by adding the common
    command line options to it.

    Args:
        parser (ArgumentParser):  The parser that is modified.

    Returns:
        The given arguments parser modified.
    """
    # --------------------------------------------------------- #
    # Special options

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__.get_version()
    )

    # --------------------------------------------------------- #
    # Top-level options

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="don't actually run any commands; just print them"
    )
    parser.add_argument(
        "-j",
        "--jobs",
        default=multiprocessing.cpu_count(),
        type=int,
        help="specify the number of parallel build jobs to use"
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="clean up the build environment before build"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print the debug-level logging output"
    )
    parser.add_argument(
        "--repository",
        default="unsung-anthem",
        help="set the name of the repository directory of the project that is "
             "being built"
    )

    return parser


def _add_common_build_arguments(parser: ArgumentParser) -> ArgumentParser:
    """Modifies the given arguments parser by adding the common
    command line options related to the build of the project to
    it.

    Args:
        parser (ArgumentParser):  The parser that is modified.

    Returns:
        The given arguments parser modified.
    """
    # --------------------------------------------------------- #
    # TODO Build target options

    target_group = parser.add_argument_group(
        "Build target options",
        "Please note that these option don't have any actual effect on the "
        "built binaries yet"
    )

    target_group.add_argument(
        "--host-target",
        default=str(Target.resolve_host_target()),
        help="set the main target for the build (default: {})".format(
            Target.resolve_host_target()
        )
    )

    return parser


def create_args_parser() -> ArgumentParser:
    """Creates the parser for the command line arguments.

    Returns:
        An object of the type ArgumentParser.
    """
    parser = ArgumentParser(description=DESCRIPTION, epilog=EPILOG)

    # TODO Add the options common to every run mode here.

    # --------------------------------------------------------- #
    # Sub-commands

    subparsers = parser.add_subparsers(dest="run_mode")

    preset = _add_common_arguments(  # noqa: F841
        subparsers.add_parser(RunMode.preset.value)
    )
    configure = _add_common_build_arguments(  # noqa: F841
        _add_common_arguments(
            subparsers.add_parser(RunMode.preset.value)
        )
    )
    compose = _add_common_build_arguments(  # noqa: F841
        _add_common_arguments(subparsers.add_parser(RunMode.preset.value))
    )

    # --------------------------------------------------------- #
    # Preset: Preset options

    preset_group = preset.add_argument_group("Preset options")

    preset_group.add_argument(
        "--file",
        action="append",
        default=[],
        help="load presets from the given file",
        metavar="PATH",
        dest="preset_file_names"
    )
    preset_group.add_argument(
        "--name",
        help="use the given option preset",
        metavar="NAME",
        dest="preset_name"
    )
    preset_group.add_argument(
        "--show",
        action="store_true",
        help="list all presets and exit",
        dest="show_presets"
    )
    preset_group.add_argument(
        "--expand-script-invocation",
        action="store_true",
        help="print the build-script invocation made by the preset, but don't "
             "run it"
    )

    return parser
