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
This support module adds and parses the command line arguments.
"""

import multiprocessing
import os
import re

from util.target import host_target

from . import argparse, defaults

from .variables import ODE_SOURCE_ROOT, ODE_REPO_NAME


class _ApplyDefaultsArgumentParser(argparse.ArgumentParser):
    """
    A wrapper class around the default ArgumentParser that allows
    for post-processing the parsed argument namespace to apply
    default argument transformations.
    """

    def __init__(self, apply_defaults=None, *args, **kwargs):
        self._apply_defaults = apply_defaults
        super(_ApplyDefaultsArgumentParser, self).__init__(*args, **kwargs)

    def parse_known_args(self, args=None, namespace=None):
        args, argv = super(
            _ApplyDefaultsArgumentParser, self).parse_known_args(
                args, namespace)

        self._apply_defaults(args)
        return args, argv


def _apply_common_default_arguments(args):
    """
    Preprocess argument namespace to apply default behaviours for both the
    build script and bootstrap.
    """
    if args.verbosity < 0:
        args.verbosity = 0

    if args.ode_version and "[v]" in args.ode_version:
        args.ode_version = args.ode_version.replace(
            "[v]", defaults.ODE_VERSION)

    if args.anthem_version and "[v]" in args.anthem_version:
        args.anthem_version = args.anthem_version.replace(
            "[v]", defaults.ANTHEM_VERSION)

    env_var = re.compile(r"env\(\w+\)")

    if args.ode_version and env_var.search(args.ode_version):
        for var in env_var.findall(args.ode_version):
            var_name = var[4:-1]
            args.ode_version = args.ode_version.replace(
                var, os.environ[var_name])

    if args.anthem_version and env_var.search(args.anthem_version):
        for var in env_var.findall(args.anthem_version):
            var_name = var[4:-1]
            args.anthem_version = args.anthem_version.replace(
                var, os.environ[var_name])

    # Set the default build variant.
    if args.build_variant is None:
        args.build_variant = "Debug"

    if args.ode_build_variant is None:
        args.ode_build_variant = args.build_variant

    # TODO Add the build variants for rest of the projects if
    # needed


def _apply_default_arguments(args):
    """
    Preprocess argument namespace to apply default behaviours.
    """
    _apply_common_default_arguments(args)

    # Assertions are enabled by default.
    if args.assertions is None:
        args.assertions = True

    # Propagate the default assertions setting.
    # if args.ode_assertions is None:
    #     args.ode_assertions = args.assertions

    # if args.anthem_assertions is None:
    #     args.anthem_assertions = args.assertions

    # if args.std is None:
    #     args.std = "c++17"

    # Set the default CMake generator.
    if args.cmake_generator is None:
        args.cmake_generator = "Ninja"

    if args.enable_gcov:
        args.cmake_generator = "Unix Makefiles"

    if not args.auth_token and args.auth_token_file and os.path.exists(
            args.auth_token_file):
        with open(args.auth_token_file) as token_file:
            args.auth_token = str(token_file.read())


def _apply_default_bootstrap_arguments(args):
    """
    Preprocess argument namespace to apply default behaviours for
    the bootstrap script.
    """
    _apply_common_default_arguments(args)


def create_argument_parser(bootstrap):
    """
    Build a configured argument parser.

    bootstrap -- whether or not the parser is created for the
    bootstrap script and not the build script
    """
    if bootstrap:
        parser = _ApplyDefaultsArgumentParser(
            apply_defaults=_apply_default_bootstrap_arguments,
            formatter_class=argparse.RawDescriptionHelpFormatter, usage=USAGE,
            description=DESCRIPTION_BOOTSTRAP, epilog=EPILOG_BOOTSTRAP)
    else:
        parser = _ApplyDefaultsArgumentParser(
            apply_defaults=_apply_default_arguments,
            formatter_class=argparse.RawDescriptionHelpFormatter, usage=USAGE,
            description=DESCRIPTION, epilog=EPILOG)

    builder = parser.to_builder()

    # Prepare DSL functions
    option = builder.add_option
    set_defaults = builder.set_defaults
    in_group = builder.in_group
    mutually_exclusive_group = builder.mutually_exclusive_group

    # Prepare DSL actions
    append = builder.actions.append
    store = builder.actions.store
    store_true = builder.actions.store_true
    store_false = builder.actions.store_false
    store_int = builder.actions.store_int
    store_path = builder.actions.store_path
    toggle_true = builder.actions.toggle_true
    toggle_false = builder.actions.toggle_false
    unsupported = builder.actions.unsupported

    # --------------------------------------------------------- #
    # Top-level options

    option(
        ["-n", "--dry-run"],
        store_true,
        help="print the commands that would be executed, but don't execute "
             "them")

    option(
        "--build-subdir",
        store,
        metavar="PATH",
        help="name of the directory under $ODE_BUILD_ROOT where the build "
             "products will be placed")

    if not bootstrap:
        option(
            "--install-prefix",
            store_path,
            default=os.path.join(ODE_SOURCE_ROOT, "local"),
            help="the installation prefix. This is where built products (like "
                 "bin, lib, and include) will be installed.")

    option(
        ["-j", "--jobs"],
        store_int("build_jobs"),
        default=multiprocessing.cpu_count(),
        help="the number of parallel build jobs to use")
    option(
        "--cmake",
        store_path(executable=True),
        help="the path to a CMake executable that will be used to build the "
             "project")

    option(
        "--ode-version",
        store,
        default=defaults.ODE_VERSION,
        metavar="MAJOR.MINOR.PATCH",
        help="the version of {} where the token [v] in the value equals the "
             "default version and env(X) equals the environment variable "
             "$X".format(defaults.ODE_NAME))
    option(
        "--anthem-version",
        store,
        default=defaults.ANTHEM_VERSION,
        metavar="MAJOR.MINOR.PATCH",
        help="the version of {} where the token [v] in the value equals the "
             "default version and env(X) equals the environment variable "
             "$X".format(defaults.ANTHEM_NAME))

    option(
        "--darwin-deployment-version",
        store,
        default=defaults.DARWIN_DEPLOYMENT_VERSION,
        metavar="MAJOR.MINOR",
        help="minimum deployment target version for macOS")

    if not bootstrap:
        option(
            "--extra-cmake-options",
            append,
            type=argparse.ShellSplitType(),
            help="pass through extra options to CMake in the form of comma "
                 "separated options, for example "
                 "'-DCMAKE_VAR1=YES,-DCMAKE_VAR2=/tmp'")

    option(
        ["-v", "--verbose"],
        store_int("verbosity"),
        default=0,
        help="print the commands executed during the build")

    # --------------------------------------------------------- #
    in_group("TODO: Host and cross-compilation targets")

    option(
        "--host-target",
        store,
        default=host_target().name,
        help="the host target that the project is built for")
    option(
        "--cross-compile-hosts",
        append,
        type=argparse.ShellSplitType(),
        default=[],
        help="a space separated list of targets to cross-compile the project "
             "for")

    # --------------------------------------------------------- #
    if not bootstrap:
        in_group("Options to select projects")

        option(
            ["-t", "--test"],
            toggle_true("build_test"),
            help="build the tests for the project")
        option(
            ["-b", "--benchmarking"],
            toggle_true("build_benchmarking"),
            help="build the benchmarkings with tests")

    # --------------------------------------------------------- #
    if not bootstrap:
        in_group("Select the CMake generator")

        set_defaults(cmake_generator=defaults.CMAKE_GENERATOR)

        option(
            ["-e", "--eclipse"],
            store("cmake_generator"),
            const="Eclipse CDT4 - Ninja",
            help="use CMake's Eclipse generator (%(default)s by default)")
        option(
            ["-m", "--make"],
            store("cmake_generator"),
            const="Unix Makefiles",
            help="use CMake's Makefile generator (%(default)s by default)")
        option(
            ["-x", "--xcode"],
            store("cmake_generator"),
            const="Xcode",
            help="use CMake's Xcode generator (%(default)s by default)")
        option(
            "--visual-studio-14",
            store("cmake_generator"),
            const="Visual Studio 14 2015",
            help="use CMake's Visual Studio 2015 generator (%(default)s by "
                 "default)")
        option(
            "--visual-studio-15",
            store("cmake_generator"),
            const="Visual Studio 15 2017",
            help="use CMake's Visual Studio 2017 generator (%(default)s by "
                 "default)")

    # --------------------------------------------------------- #
    in_group("Extra actions to perform before or in addition to building")

    option(
        ["-c", "--clean"],
        store_true,
        help="do a clean build")

    if not bootstrap:
        option(
            "--gcov",
            store_true("enable_gcov"),
            help="use gcov and lcov to generate code coverage information")
        option(
            "--xvfb",
            store_true("enable_xvfb"),
            help="use X virtual framebuffer with the build")

    # --------------------------------------------------------- #
    in_group("Build variant")

    with mutually_exclusive_group():

        set_defaults(build_variant="Debug")

        option(
            ["-d", "--debug"],
            store("build_variant"),
            const="Debug",
            help="build the Debug variant (default is %(default)s)")

        option(
            ["-r", "--release-debuginfo"],
            store("build_variant"),
            const="RelWithDebInfo",
            help="build the RelWithDebInfo variant (default is %(default)s)")

        option(
            ["-R", "--release"],
            store("build_variant"),
            const="Release",
            help="build the Release variant (default is %(default)s)")

    # --------------------------------------------------------- #
    in_group("Override build variant for a specific project")

    option(
        "--debug-ode",
        store("ode_build_variant"),
        const="Debug",
        help="build the Debug variant of {}".format(defaults.ODE_NAME))

    # --------------------------------------------------------- #
    # Assertions group

    if not bootstrap:
        with mutually_exclusive_group():

            set_defaults(assertions=True)

            # TODO: Convert to store_true
            option(
                "--assertions",
                store,
                const=True,
                help="enable assertions in all projects")

            # TODO: Convert to store_false
            option(
                "--no-assertions",
                store("assertions"),
                const=False,
                help="disable assertions in all projects")

    # --------------------------------------------------------- #
    if bootstrap:
        in_group("Authentication options")

        with mutually_exclusive_group():

            option(
                "--auth-token-file",
                store,
                default=os.path.join(
                    ODE_SOURCE_ROOT,
                    ODE_REPO_NAME,
                    "token"),
                metavar="TOKEN",
                help="the file which contains the OAuth token which is used "
                     "to access the GitHub API")

            option(
                "--auth-token",
                store,
                metavar="TOKEN",
                help="the OAuth token which is used to access the GitHub API")

    # --------------------------------------------------------- #
    if not bootstrap:
        in_group("Feature options")

        option(
            "--std-clock",
            toggle_true,
            help="use the C++ standard library clock instead of the clock of "
                 "Simple DirectMedia Layer")

        option(
            "--log-tests",
            toggle_true,
            help="let the loggers in tests to write output into a non-null "
                 "sink")

        option(
            "--developer-build",
            toggle_true,
            help="build the project for development")

        option("--disable-gl-calls", toggle_true, help="disable OpenGL calls")

    # --------------------------------------------------------- #
    if not bootstrap:
        in_group("Threading options")

        with mutually_exclusive_group():
            set_defaults(multithreading=True)

            # TODO: Convert to store_true
            option(
                "--multithreading",
                store("multithreading"),
                const=True,
                help="use multithreading in the game")

            # TODO: Convert to store_false
            option(
                "--no-multithreading",
                store("multithreading"),
                const=False,
                help="use single thread in the game")

            # TODO: Convert to store_false
            option(
                "--single-thread",
                store("multithreading"),
                const=False,
                help="use single thread in the game")

    # --------------------------------------------------------- #
    in_group("MSBuild options")

    option(
        "--msbuild-logger",
        store_path,
        help="the absolute path to MSBuild logger",
        metavar="PATH")

    # --------------------------------------------------------- #

    return builder.build()


USAGE = """
  %(prog)s [-h | --help] [OPTION...]
  %(prog)s --preset=NAME [SUBSTITUTION...]
"""


DESCRIPTION = """
Use this tool to build, test, and prepare binary distribution archives of
{anthem}.
"""


DESCRIPTION_BOOTSTRAP = """
Use this tool to set up the building or development environment for {anthem}.
""".format(anthem=defaults.ANTHEM_NAME)


EPILOG = """
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
""".format(ode=defaults.ODE_NAME, anthem=defaults.ANTHEM_NAME)


EPILOG_BOOTSTRAP = """
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

Make sure that your system has C and C++ compilers.

That's it; you're ready to go!

Preset mode in bootstrap
---------------------------

All buildbots and automated environments use 'bootstrap' in *preset mode*.  In
preset mode, the command line only specifies the preset name.  The actual
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

  [~/src/s]$ ./unsung-anthem/utils/bootstrap --preset=doo
  ./unsung-anthem/utils/bootstrap: using preset 'doo', which expands to
  ./unsung-anthem/utils/bootstrap --release --debug-ode --test \
--build-subdir=doo --
  ...
""".format(ode=defaults.ODE_NAME, anthem=defaults.ANTHEM_NAME)
