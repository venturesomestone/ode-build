# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains functions for creating the parser for
the command line arguments and options of the build script.
"""

import multiprocessing

from argparse import ArgumentParser

from .support.build_variant import BuildVariant

from .support.cmake_generator import CMakeGenerator

from .support.command_line import DESCRIPTION, EPILOG

from .support.cpp_standard import CppStandard

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
        "-V",
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
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="build the tests",
        dest="build_test"
    )
    parser.add_argument(
        "-b",
        "--benchmark",
        action="store_true",
        help="build the benchmarks",
        dest="build_benchmark"
    )

    parser.add_argument(
        "--docs",
        action="store_true",
        help="build the documentation",
        dest="build_docs"
    )

    parser.add_argument(
        "--lint",
        action="store_true",
        help="run cland-tidy on the project"
    )

    # --------------------------------------------------------- #
    # Build variant options

    variant_group = parser.add_argument_group("Build variant options")

    variant_selection_group = variant_group.add_mutually_exclusive_group(
        required=False
    )

    default_build_variant = BuildVariant.debug.name

    parser.set_defaults(build_variant=default_build_variant)

    variant_selection_group.add_argument(
        "--build-variant",
        default=default_build_variant,
        choices=[name for name, value in BuildVariant.__members__.items()],
        help="use the selected build variant (default: {})".format(
            default_build_variant
        ),
        dest="build_variant"
    )
    variant_selection_group.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const=BuildVariant.debug.name,
        help="build the project using the Debug variant",
        dest="build_variant"
    )
    variant_selection_group.add_argument(
        "-r",
        "--release-debuginfo",
        action="store_const",
        const=BuildVariant.release_debug_info.name,
        help="build the project using the RelWithDebInfo variant",
        dest="build_variant"
    )
    variant_selection_group.add_argument(
        "-R",
        "--release",
        action="store_const",
        const=BuildVariant.release.name,
        help="build the project using the Release variant",
        dest="build_variant"
    )
    variant_selection_group.add_argument(
        "-M",
        "--minsize-release",
        action="store_const",
        const=BuildVariant.minimum_size_release.name,
        help="build the project using the MinSizeRel variant",
        dest="build_variant"
    )

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

    # --------------------------------------------------------- #
    # Build generator options

    generator_group = parser.add_mutually_exclusive_group(required=False)

    default_cmake_generator = CMakeGenerator.ninja.name

    parser.set_defaults(cmake_generator=default_cmake_generator)

    generator_group.add_argument(
        "-G",
        "--cmake-generator",
        default=default_cmake_generator,
        choices=[name for name, value in CMakeGenerator.__members__.items()],
        help="generate the build files using the selected CMake generator",
        dest="cmake_generator"
    )
    generator_group.add_argument(
        "-N",
        "--ninja",
        action="store_const",
        const=CMakeGenerator.ninja.name,
        help="generate the build files using the CMake generator for Ninja",
        dest="cmake_generator"
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
            subparsers.add_parser(RunMode.configure.value)
        )
    )
    compose = _add_common_build_arguments(  # noqa: F841
        _add_common_arguments(subparsers.add_parser(RunMode.compose.value))
    )

    # --------------------------------------------------------- #
    # Preset: Positional arguments

    preset.add_argument(
        "preset_run_mode",
        choices=[RunMode.configure.value, RunMode.compose.value],
        help="run preset invocation in the given mode"
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

    # --------------------------------------------------------- #
    # Compose: C++ standard options

    cpp_std_group = compose.add_mutually_exclusive_group(required=False)

    default_cpp_std = CppStandard.cpp17.name

    cpp_std_choices = [name for name, value in CppStandard.__members__.items()]

    cpp_std_choices.extend([
        name.replace("p", "+")
        for name, value in CppStandard.__members__.items()
    ])

    cpp_std_group.add_argument(
        "--std",
        default=default_cpp_std,
        choices=cpp_std_choices,
        help="use the given C++ standard (default: {})".format(
            default_cpp_std
        ),
        dest="cpp_std"
    )
    cpp_std_group.add_argument(
        "--c++17",
        action="store_const",
        const=CppStandard.cpp17.name,
        help="use C++17 standard",
        dest="cpp_std"
    )
    cpp_std_group.add_argument(
        "--c++20",
        action="store_const",
        const=CppStandard.cpp20.name,
        help="use C++20 standard",
        dest="cpp_std"
    )

    # --------------------------------------------------------- #
    # Compose: CMake options

    compose.add_argument(
        "--cmake-options",
        action="append",
        # nargs="+",
        help="add a list of additional CMake option to pass to the build"
    )

    return parser
