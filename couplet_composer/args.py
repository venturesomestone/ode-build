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

"""This module defines the argument parser for the project."""

import argparse
import json
import multiprocessing
import os

from .support.values import DEFAULTS_FILE_PATH

from .support.variables import \
    ANTHEM_NAME, ODE_NAME, ODE_REPO_NAME, ODE_SOURCE_ROOT

from .util.target import host_target


def _get_defaults():
    with open(
        os.path.join(ODE_SOURCE_ROOT, ODE_REPO_NAME, DEFAULTS_FILE_PATH)
    ) as f:
        return json.load(f)


def _add_common_arguments(parser):
    # --------------------------------------------------------- #
    # Top-level options

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        type=bool,
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
        type=bool,
        help="clean up the build environment before build"
    )
    parser.add_argument(
        "--print-debug",
        action="store_true",
        type=bool,
        help="print the debug-level logging output"
    )

    # --------------------------------------------------------- #
    # Sub-commands

    subparsers = parser.add_subparsers(required=True)

    configure = subparsers.add_parser("configure")
    compose = subparsers.add_parser("compose", aliases=["build"])

    return parser, configure, compose


def create_argument_parser():
    """Creates the argument parser of the program."""
    parser, configure, compose = _add_common_arguments(argparse.ArgumentParser(
        description=_DESCRIPTION, epilog=_EPILOG
    ))

    # --------------------------------------------------------- #
    # Common build options

    defaults_data = _get_defaults()

    parser.add_argument(
        "--ode-version",
        default=defaults_data["ode"]["version"],
        help="set the version of {}".format(ODE_NAME)
    )
    parser.add_argument(
        "--anthem-version",
        default=defaults_data["anthem"]["version"],
        help="set the version of {}".format(ANTHEM_NAME)
    )

    # --------------------------------------------------------- #
    # TODO Build target options

    target = parser.add_argument_group(
        "Build target options",
        "Please note that these option don't have any actual effect on the "
        "built binaries yet"
    )

    target.add_argument(
        "--host-target",
        default=host_target(),
        help="set the main target for the build"
    )
    target.add_argument(
        "--cross-compile-hosts",
        default=[],
        help="cross-compile the project for the given targets"
    )

    return parser


def create_preset_argument_parser():
    """Creates the argument parser of the preset mode."""
    parser, configure, compose = _add_common_arguments(argparse.ArgumentParser(
        description="Builds {} and {} using a preset".format(
            ODE_NAME,
            ANTHEM_NAME
        )
    ))

    # --------------------------------------------------------- #
    # Preset options

    preset = parser.add_argument_group("Preset options")

    preset.add_argument(
        "--preset-file",
        action="append",
        default=[],
        help="load presets from the given file",
        metavar="PATH",
        dest="preset_file_names"
    )
    preset.add_argument(
        "--preset",
        help="use the given option preset",
        metavar="NAME"
    )
    preset.add_argument(
        "--show-presets",
        action="store_true",
        help="list all presets and exit"
    )
    preset.add_argument(
        "--expand-build-script-invocation",
        action="store_true",
        help="print the build-script invocation made by the preset, but don't "
             "run it"
    )

    return parser


_DESCRIPTION = """
Use this tool to build, test, and prepare binary distribution archives of {ode}
and {anthem}.
""".format(ode=ODE_NAME, anthem=ANTHEM_NAME)

_EPILOG = """
Using option presets:

  --preset-file=PATH    load presets from the specified file

  --preset=NAME         use the specified option preset

  You cannot use the preset mode with other options.  It is not possible to add
  ad hoc customizations to a preset.  If you want to customize a preset, you
  need to create a new preset.


Environment variables
---------------------

This script respects a few environment variables if you set them:

ODE_SOURCE_ROOT: a directory containing the source for {anthem}

'build-script' expects the sources to be laid out in the following way:

   $ODE_SOURCE_ROOT/unsung-anthem (the directory name does not matter)

ODE_BUILD_ROOT: a directory in which to create out-of-tree builds

Preparing to run this script
----------------------------

Run the bootstrap script and make sure that your system has C and C++
compilers.

That's it; you're ready to go!

Preset mode in build-script
---------------------------

All buildbots and automated environments use 'build-script' in *preset mode*.
In preset mode, the command line only specifies the preset name.  The actual
options come from the selected preset in 'utils/build-presets.ini'.

If you have your own favourite set of options, you can create your own, local,
preset. For example, let's create a preset called 'doo' (which stands for Debug
{ode}):

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

While one can invoke CMake directly to build {anthem}, this tool will
save one's time by taking away the mechanical parts of the process, providing
one the controls for the important options.

For all automated build environments, this tool is regarded as *the* *only*
way to build {anthem}.  This is not a technical limitation of the {anthem}
build system.  It is a policy decision aimed at making the builds uniform
across all environments and easily reproducible by engineers who are not
familiar with the details of the setups of other systems or automated
environments.
""".format(ode=ODE_NAME, anthem=ANTHEM_NAME)
