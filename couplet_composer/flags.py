# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""The command line flags of Couplet Composer."""

from __future__ import print_function

import multiprocessing
import os

from absl import flags

from support import defaults

from support.variables import ODE_BUILD_ROOT

from util.target import host_target


__all__ = ["FLAGS", "register_flag_validators"]


FLAGS = flags.FLAGS

# ------------------------------------------------------------- #
# Top-level options
# ------------------------------------------------------------- #

flags.DEFINE_boolean(
    "dry-run",
    False,
    "Don't actually run any commands; just print them.",
    short_name="n"
)
flags.DEFINE_alias("just-print", "dry-run")
flags.DEFINE_boolean("print-debug", False, "Produce debugging output.")
flags.DEFINE_integer(
    "jobs",
    multiprocessing.cpu_count(),
    "Specify the number of parallel build jobs to use.",
    short_name="j"
)

# ------------------------------------------------------------- #
# Common build options
# ------------------------------------------------------------- #

flags.DEFINE_string(
    "install-prefix",
    os.path.join(ODE_BUILD_ROOT, "local"),
    "Install the final build products to the given path."
)
flags.DEFINE_string(
    "ode-version",
    defaults.ODE_VERSION,
    "Set the version of the built {} product.".format(defaults.ODE_NAME)
)
flags.DEFINE_string(
    "anthem-version",
    defaults.ANTHEM_VERSION,
    "Set the version of the built {} product.".format(defaults.ANTHEM_NAME)
)
flags.DEFINE_string(
    "darwin-deployment-version",
    defaults.DARWIN_DEPLOYMENT_VERSION,
    "Set minimum deployment target version of macOS."
)

# ------------------------------------------------------------- #
# Extra action options
# ------------------------------------------------------------- #

# TODO
flags.DEFINE_boolean(
    "sandbox",
    False,
    "Only use tools and dependencies that the build script sets up into its "
    "environment.",
    short_name="s"
)
flags.DEFINE_boolean(
    "clean",
    False,
    "Delete the build files before build.",
    short_name="c"
)
flags.DEFINE_boolean(
    "development-stack",
    False,
    "Use the local development copies of the projects.",
    short_name="S"
)

# ------------------------------------------------------------- #
# TODO Host and cross-compilation targets
# ------------------------------------------------------------- #

flags.DEFINE_string(
    "host-target",
    host_target().name,
    "Build the project for the host target."
)
flags.DEFINE_list(
    "cross-compile-hosts",
    [],
    "Cross-compile the project for the cross-compile targets."
)

# ------------------------------------------------------------- #
# Project-selecting options
# ------------------------------------------------------------- #

flags.DEFINE_boolean(
    "test",
    False,
    "Build the tests and test the project.",
    short_name="t"
)
flags.DEFINE_boolean(
    "benchmarking",
    False,
    "Build the benchmarkings with the tests for the project.",
    short_name="b"
)
flags.DEFINE_boolean("gcov", False, "Generate code coverage information.")

# ------------------------------------------------------------- #
# Build generator options
# ------------------------------------------------------------- #

# The CMake generators you can use
CMAKE_GENERATORS = [
    "Ninja",
    "ninja",
    "Eclipse CDT4 - Ninja",
    "eclipse",
    "Unix Makefiles",
    "make",
    "Xcode",
    "xcode",
    "Visual Studio 14 2015",
    "visual-studio-14",
    "Visual Studio 15 2017",
    "visual-studio-15"
]

flags.DEFINE_enum(
    "cmake-generator",
    defaults.CMAKE_GENERATOR,
    CMAKE_GENERATORS,
    "Generate the build files for the selected program.",
    short_name="G"
)
flags.DEFINE_boolean(
    "ninja",
    False,
    "Generate the build files for Ninja regardless of '--cmake-generator'.",
    short_name="N"
)
flags.DEFINE_boolean(
    "eclipse",
    False,
    "Generate the build files for Eclipse regardless of '--cmake-generator'.",
    short_name="e"
)
flags.DEFINE_boolean(
    "make",
    False,
    "Generate Makefiles regardless of '--cmake-generator'.",
    short_name="m"
)
flags.DEFINE_boolean(
    "xcode",
    False,
    "Generate the build files for Xcode regardless of '--cmake-generator'.",
    short_name="x"
)
flags.DEFINE_boolean(
    "visual-studio-14",
    False,
    "Generate the build files for Visual Studio 2015 regardless of "
    "'--cmake-generator'."
)
flags.DEFINE_boolean(
    "visual-studio-15",
    False,
    "Generate the build files for Visual Studio 2017 regardless of "
    "'--cmake-generator'."
)

# ------------------------------------------------------------- #
# Build variant options
# ------------------------------------------------------------- #

# The build variants you can use
BUILD_VARIANTS = [
    "Debug",
    "debug",
    "RelWithDebInfo",
    "release-debuginfo",
    "Release",
    "release"
]

flags.DEFINE_enum(
    "build-variant",
    defaults.BUILD_VARIANT,
    BUILD_VARIANTS,
    "Build the given variant of the project."
)
flags.DEFINE_boolean(
    "debug",
    False,
    "Build the debug configuration of the project regardless of "
    "'--build-variant'.",
    short_name="d"
)
flags.DEFINE_boolean(
    "release-debuginfo",
    False,
    "Build the release configuration of the project with debug information "
    "regardless of '--build-variant'.",
    short_name="r"
)
flags.DEFINE_boolean(
    "release",
    False,
    "Build the release configuration of the project regardless of "
    "'--build-variant'.",
    short_name="R"
)
flags.DEFINE_boolean(
    "debug-ode",
    None,
    "Build the debug configuration of {} regardless of the build "
    "variant.".format(defaults.ODE_NAME)
)
flags.DEFINE_boolean(
    "debug-anthem",
    False,
    "Build the debug configuration of {} regardless of the build "
    "variant.".format(defaults.ANTHEM_NAME)
)
flags.DEFINE_boolean(
    "debug-sdl",
    False,
    "Build the debug configuration of {} regardless of the build "
    "variant.".format(defaults.SDL_NAME)
)

# ------------------------------------------------------------- #
# Feature options
# ------------------------------------------------------------- #

flags.DEFINE_boolean("assertions", False, "Enable assertions in the project.")
flags.DEFINE_boolean(
    "ode-assertions",
    False,
    "Enable assertions in {}.".format(defaults.ODE_NAME)
)
flags.DEFINE_boolean(
    "anthem-assertions",
    False,
    "Enable assertions in {}.".format(defaults.ANTHEM_NAME)
)
flags.DEFINE_boolean(
    "multithread",
    False,
    "Enable multithreading in the project."
)
flags.DEFINE_alias("multithreading", "multithread")
flags.DEFINE_boolean(
    "developer-build",
    False,
    "Enable developer features in the project."
)
flags.DEFINE_boolean(
    "std-clock",
    False,
    "Use the C++ standard library clock instead of the clock of {}.".format(
        defaults.SDL_NAME
    )
)
flags.DEFINE_boolean(
    "log-tests",
    False,
    "Let the tests write logger output to a non-null sink."
)
flags.DEFINE_boolean("disable-gl-calls", False, "Disable OpenGL calls.")
flags.DEFINE_boolean("xvfb", False, "Use X virtual framebuffer.")

# ------------------------------------------------------------- #
# OAuth token options
# ------------------------------------------------------------- #

flags.DEFINE_string(
    "auth-token-file",
    None,
    "Get GitHub authentication token from the given file."
)
flags.DEFINE_string(
    "auth-token",
    None,
    "Access the GitHub API with the given token."
)

# ------------------------------------------------------------- #
# MSBuild options
# ------------------------------------------------------------- #

flags.DEFINE_string(
    "msbuild-logger",
    None,
    "Specify absolute path to desired logger for MSBuild."
)

# ------------------------------------------------------------- #
# Preset mode options
# ------------------------------------------------------------- #

flags.DEFINE_list(
    "preset-files",
    None,
    "Search for build presets in the given files."
)
flags.DEFINE_string(
    "preset",
    None,
    "Use the given build preset.",
    short_name="P"
)
flags.DEFINE_boolean(
    "show-presets",
    False,
    "Only list the presets in the preset files."
)
flags.DEFINE_boolean(
    "expand-build-script-invocation",
    False,
    "Only show the command that the build would be called with."
)

# ------------------------------------------------------------- #
# Flags validators
# ------------------------------------------------------------- #


def _mark_flag_as_preset_only(flag_name):
    pass


def _mark_flag_as_preset(flag_name):
    pass


def register_flag_validators():
    """
    Registers the flag validators to be called before the app is
    run.
    """
    # TODO Currently these are ignored
    _mark_flag_as_preset_only("preset-files")
    _mark_flag_as_preset_only("preset")
    _mark_flag_as_preset_only("show-presets")
    _mark_flag_as_preset_only("expand-build-script-invocation")

    _mark_flag_as_preset("dry-run")
    _mark_flag_as_preset("debug")
    _mark_flag_as_preset("clean")
    _mark_flag_as_preset("jobs")
    _mark_flag_as_preset("auth-token-file")
    _mark_flag_as_preset("auth-token")

    # CMake generator validators
    flags.mark_bool_flags_as_mutual_exclusive([
        "ninja",
        "eclipse",
        "make",
        "xcode",
        "visual-studio-14",
        "visual-studio-15"
    ])

    # Build variant validators
    flags.mark_bool_flags_as_mutual_exclusive(
        ["debug", "release-debuginfo", "release"]
    )

    # GitHub OAuth token validators
    flags.mark_flags_as_mutual_exclusive(["auth-token-file", "auth-token"])
