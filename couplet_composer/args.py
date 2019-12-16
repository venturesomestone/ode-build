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

"""This module defines the argument parser for the project."""

import argparse
import multiprocessing

from .support.cmake_generators import \
    get_cmake_generator_names, get_make_cmake_generator_name, \
    get_ninja_cmake_generator_name

from .support.project_values import \
    get_anthem_name, get_anthem_version, get_ode_name, get_ode_version

from .util.cache import cached

from .util.target import resolve_host_target


def _add_common_arguments(parser):
    """
    Adds the options common to all parsers to the given parser.
    This function isn't pure as it modifies the given parser.
    Returns the parser that contains the added arguments.

    parser -- The parser to which the arguments are added.
    """
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
        "--print-debug",
        action="store_true",
        help="print the debug-level logging output"
    )

    # --------------------------------------------------------- #
    # GitHub options

    github_group = parser.add_argument_group("GitHub options")

    github_group.add_argument(
        "--github-user-agent",
        default=None,
        help="set the user agent used when accessing the GitHub API "
             "(default: {})".format(None)
    )
    github_group.add_argument(
        "--github-api-token",
        default=None,
        help="set the API token used when accessing the GitHub API "
             "(default: {})".format(None)
    )

    return parser


def _add_common_build_arguments(parser):
    """
    Adds the options common to configure and compose parsers to
    the given parser. This function isn't pure as it modifies the
    given parser. Returns the parser that contains the added
    arguments.

    parser -- The parser to which the arguments are added.
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
        default=resolve_host_target(),
        help="set the main target for the build (default: {})".format(
            resolve_host_target()
        )
    )
    # target_group.add_argument(
    #     "--cross-compile-hosts",
    #     default=[],
    #     help="cross-compile the project for the given targets"
    # )

    # --------------------------------------------------------- #
    # TODO Build generator options
    generator_group = parser.add_mutually_exclusive_group(required=False)

    default_cmake_generator = get_ninja_cmake_generator_name()

    parser.set_defaults(cmake_generator=default_cmake_generator)

    generator_group.add_argument(
        "-G",
        "--cmake-generator",
        default=default_cmake_generator,
        choices=get_cmake_generator_names(),
        help="generate the build files using the selected CMake generator",
        dest="cmake_generator"
    )
    generator_group.add_argument(
        "-m",
        "--make",
        action="store_const",
        const=get_make_cmake_generator_name(),
        help="generate the build files using the CMake generator for Unix "
             "Makefiles",
        dest="cmake_generator"
    )

    return parser


def create_argument_parser(source_root):
    """
    Creates the argument parser of the program.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    parser = argparse.ArgumentParser(
        description=_get_description(source_root=source_root),
        epilog=_get_epilog(source_root=source_root),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # The common arguments are added to the base parser so the
    # normal help command shows them
    parser = _add_common_arguments(parser)

    # --------------------------------------------------------- #
    # Sub-commands

    subparsers = parser.add_subparsers(dest="composer_mode")

    preset = _add_common_arguments(subparsers.add_parser("preset"))
    configure = _add_common_build_arguments(_add_common_arguments(
        subparsers.add_parser("configure")
    ))
    compose = _add_common_build_arguments(_add_common_arguments(
        subparsers.add_parser("compose")
    ))

    # --------------------------------------------------------- #
    # Preset: Positional arguments

    preset.add_argument(
        "preset_run_mode",
        choices=["configure", "compose"],
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
        dest="preset"
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
    # Compose: Common build options

    compose.add_argument(
        "--ode-version",
        default=get_ode_version(source_root=source_root),
        help="set the version of {}".format(get_ode_name(
            source_root=source_root
        ))
    )
    compose.add_argument(
        "--anthem-version",
        default=get_anthem_version(source_root=source_root),
        help="set the version of {}".format(get_anthem_name(
            source_root=source_root
        ))
    )

    return parser


@cached
def _get_description(source_root):
    """
    Gives the command line description of Couplet Composer.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return """
Use this tool to build, test, and prepare binary distribution archives of
Obliging Ode and Unsung Anthem.
""".format(
        ode=get_ode_name(source_root=source_root),
        anthem=get_anthem_name(source_root=source_root)
    )


@cached
def _get_epilog(source_root):
    """
    Gives the command line epilogue of Couplet Composer.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return """
Using option presets:

  --preset-file=PATH    load presets from the specified file

  --preset=NAME         use the specified option preset

  You cannot use the preset mode with other options.  It is not possible to add
  ad hoc customizations to a preset.  If you want to customize a preset, you
  need to create a new preset.


Environment variables
---------------------

This script respects a few environment variables if you set them:

ODE_SOURCE_ROOT: a directory containing the source for Obliging Ode

'build-script' expects the sources to be laid out in the following way:

   $ODE_SOURCE_ROOT/unsung-anthem (the directory name does not matter)

ODE_BUILD_ROOT: a directory in which to create out-of-tree builds

Preparing to run this script
----------------------------

Run the composer script and make sure that your system has C and C++ compilers.

That's it; you're ready to go!

Preset mode in build-script
---------------------------

All buildbots and automated environments use 'build-script' in *preset mode*.
In preset mode, the command line only specifies the preset name.  The actual
options come from the selected preset in 'utils/build-presets.ini'.

If you have your own favourite set of options, you can create your own, local,
preset. For example, let's create a preset called 'doo' (which stands for Debug
Obliging Ode):

  $ cat > ~/.ode-build-presets
  [preset: doo]
  release
  debug-ode
  test
  build-subdir=doo

To use it, specify the '--preset=' argument:

  [~/src/s]$ ./unsung-anthem/utils/build-script --preset=doo
  ./unsung-anthem/utils/build-script: using preset 'doo', which expands to
  ./unsung-anthem/utils/build-script --release --debug-ode --test \
--build-subdir=doo --
  ...

Philosophy
----------

While one can invoke CMake directly to build Unsung Anthem, this tool will
save one's time by taking away the mechanical parts of the process, providing
one the controls for the important options.

For all automated build environments, this tool is regarded as *the* *only*
way to build Unsung Anthem.  This is not a technical limitation of the Unsung
Anthem build system.  It is a policy decision aimed at making the builds
uniform across all environments and easily reproducible by engineers who are
not familiar with the details of the setups of other systems or automated
environments.
""".format(
        ode=get_ode_name(source_root=source_root),
        anthem=get_anthem_name(source_root=source_root)
    )
