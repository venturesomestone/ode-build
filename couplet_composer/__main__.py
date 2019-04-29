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

from __future__ import print_function

import multiprocessing
import os
import sys

from datetime import datetime

from absl import app, flags, logging

from support import defaults

from support.defaults import SCRIPT_NAME

from support.presets import get_all_preset_names, get_preset_options

from support.variables import \
    HOME, \
    ODE_BUILD_ROOT, \
    ODE_REPO_NAME, \
    ODE_SOURCE_ROOT

from util import shell

from util.date import date_difference, to_date_string

from util.mapping import Mapping

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
    None,
    "Get GitHub authentication token from the given file. If '--auth-token' "
    "is specified, it overrides this options."
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


def _register_flag_validators():
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


# ------------------------------------------------------------- #


def _is_preset_mode():
    return any([(opt.startswith("--preset") or opt == "--show-presets")
               for opt in sys.argv[1:]])


def _run_preset():
    logging.debug(
        "Running %s in preset mode and thus the only flags that aren't "
        "ignored are: %s",
        defaults.SCRIPT_NAME,
        ", ".join([
            "dry-run",
            "debug",
            "clean",
            "jobs",
            "auth-token-file",
            "auth-token",
            "preset-files",
            "preset",
            "show-presets",
            "expand-build-script-invocation"
        ])
    )
    if not FLAGS["preset-files"].value:
        preset_file_names = [
            os.path.join(HOME, ".anthem-build-presets"),
            os.path.join(HOME, ".ode-build-presets"),
            os.path.join(
                ODE_SOURCE_ROOT,
                ODE_REPO_NAME,
                "util",
                "build-presets.ini"
            )
        ]
    else:
        preset_file_names = FLAGS["preset-files"].value

    logging.debug("The preset files are %s", ", ".join(preset_file_names))

    if FLAGS["show-presets"].value:
        logging.info("The available presets are:")
        for name in sorted(
            get_all_preset_names(preset_file_names),
            key=str.lower
        ):
            print(name)
        return

    if not FLAGS.preset:
        logging.fatal("Missing the '--preset' option")

    preset_args = get_preset_options(None, preset_file_names, FLAGS.preset)

    build_script_args = [sys.argv[0]]
    build_script_args += [sys.argv[1]]

    if FLAGS["dry-run"].value and FLAGS["dry-run"].present:
        build_script_args += ["--dry-run"]
    if FLAGS.debug and FLAGS["debug"].present:
        build_script_args += ["--debug"]
    if FLAGS.clean and FLAGS["clean"].present:
        build_script_args += ["--clean"]
    if FLAGS.jobs and FLAGS["jobs"].present:
        build_script_args += ["--jobs", str(FLAGS.jobs)]
    if FLAGS["auth-token-file"].value and FLAGS["auth-token-file"].present:
        build_script_args += [
            "--auth-token-file", str(FLAGS["auth-token-file"].value)
        ]
    if FLAGS["auth-token"].value and FLAGS["auth-token"].present:
        build_script_args += ["--auth-token", str(FLAGS["auth-token"].value)]

    build_script_args += preset_args

    logging.info("Using preset '{}', which expands to \n\n{}\n".format(
        FLAGS.preset,
        shell.quote_command(build_script_args)
    ))
    logging.debug(
        "The script will have '{}' as the Python executable\n".format(
            sys.executable
        )
    )

    if FLAGS["expand-build-script-invocation"].value:
        logging.debug("The build script invocation is printed")
        return

    command_to_run = [sys.executable] + build_script_args

    shell.caffeinate(command_to_run)


def _run_bootstrap():
    logging.debug("%s was run in bootstrap mode", SCRIPT_NAME)


def _run_build():
    logging.debug("%s was run in build mode", SCRIPT_NAME)


def main(argv):
    """Enters the program and runs it."""
    # for flag, value in FLAGS.items():
    #     name = flag.replace("-", "_")
    #     FLAGS[name] = value
    #     FLAGS[flag] = None
    # for flag in FLAGS:
    #     ARGS["hi"] = None
    if FLAGS.debug:
        logging.set_verbosity(logging.DEBUG)
    logging.debug("The non-flag arguments are %s", argv)
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

    if not ODE_SOURCE_ROOT:
        logging.fatal(
            "Couldn't work out the source root directory (did you forget to "
            "set the '$ODE_SOURCE_ROOT' environment variable?)"
        )

    if _is_preset_mode():
        _run_preset()
    else:
        if sys.argv[1] == "bootstrap" or sys.argv[1] == "boot":
            _run_bootstrap()
        elif sys.argv[1] == "build" or sys.argv[1] == "compose":
            _run_build()
        else:
            logging.fatal(
                "%s wasn't in either bootstrap or build mode",
                SCRIPT_NAME
            )


def run():
    """
    Runs the script if Couplet Composer is invoked through
    'run.py'.
    """
    _register_flag_validators()
    app.run(main)


if __name__ == "__main__":
    _register_flag_validators()
    app.run(main)
