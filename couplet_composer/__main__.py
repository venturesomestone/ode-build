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

"""The entry point of Couplet Composer."""

import multiprocessing
import os
import sys

from datetime import datetime

from absl import app, flags, logging

from support import defaults

from support.variables import ODE_BUILD_ROOT

from util.date import date_difference, to_date_string

from util.target import host_target


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
flags.DEFINE_boolean("debug", False, "Produce debugging output.")
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
flags.DEFINE_spaceseplist(
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
    "Eclipse CDT4 - Ninja",
    "Unix Makefiles",
    "Xcode",
    "Visual Studio 14 2015",
    "Visual Studio 15 2017"
]

flags.DEFINE_enum(
    "cmake-generator",
    defaults.CMAKE_GENERATOR,
    CMAKE_GENERATORS,
    "Generate the build files for the selected program.",
    short_name="G"
)

# ------------------------------------------------------------- #
# Build variant options
# ------------------------------------------------------------- #

# The build variants you can use
BUILD_VARIANTS = ["Debug", "RelWithDebInfo", "Release"]

flags.DEFINE_enum(
    "build-variant",
    defaults.BUILD_VARIANT,
    BUILD_VARIANTS,
    "Build the given variant of the project."
)
flags.DEFINE_boolean(
    "debug-ode",
    False,
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
    os.path.join(ODE_BUILD_ROOT, "local"),
    "Get GitHub authentication token from the given file. If '--auth-token' "
    "is specified, it overrides this options."
)
flags.DEFINE_string(
    "auth-token",
    "None",
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


def main(argv):
    """Enters the program and runs it."""
    if sys.version_info.major == 2:
        if sys.version_info.minor < 7:
            logging.fatal(
                "You're using Python %s, and the smallest supported version "
                "is %s",
                sys.version,
                "2.7"
            )
        else:
            logging.warning("You're using Python %s", sys.version)
            logging.warning(
                "You should really update to Python 3 to make the world a "
                "better place!"
            )
            # The date when Python 2 is no longer supported
            eol_date = datetime.strptime(
                "2020-01-01 00:00:00",
                "%Y-%m-%d %H:%M:%S"
            )
            now = datetime.now()
            logging.warning(
                "Also, the end of life of Python 2.7 is in %s, on 1 January, "
                "2020",
                to_date_string(date_difference(now, eol_date))
            )
    else:
        logging.debug("You're using Python %s", sys.version)
        logging.debug("You seem to have an excellent taste!")


if __name__ == "__main__":
    app.run(main)
