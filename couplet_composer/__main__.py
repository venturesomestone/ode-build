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

"""The entry point of Couplet Composer."""

from __future__ import print_function

import logging
import os
import sys

from datetime import datetime

from .clone import clone

from .support.presets import get_all_preset_names, get_preset_options

from .support.values import NAME, PRESET_FILE_PATH

from .support.variables import HOME, ODE_REPO_NAME, ODE_SOURCE_ROOT

from .util import shell

from .util.date import date_difference, to_date_string

from . import args, config, set_up


def _parse_arguments_into_namespace():
    """
    Creates the argument parser for the composer and parses the
    arguments into a global namespace.
    """
    argument_parser = args.create_argument_parser()
    config.ARGS = argument_parser.parse_args()
    return argument_parser


def _set_logging_level():
    """
    Sets the logging level according to the global arguments
    namespace.
    """
    if config.ARGS.print_debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def _check_and_print_python_version():
    """Checks the current Python version and prints it."""
    if sys.version_info.major == 2:
        if sys.version_info.minor < 7:
            logging.critical(
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
            # The end-of-life time of Python 2
            python2_end_of_life = datetime.strptime(
                "2020-01-01 00:00:00",
                "%Y-%m-%d %H:%M:%S"
            )
            now = datetime.now()
            logging.warning(
                "Also, the end of life of Python 2.7 is in %s, on 1 January, "
                "2020",
                to_date_string(date_difference(now, python2_end_of_life))
            )
    else:
        logging.debug("You're using Python %s", sys.version)
        logging.debug("You seem to have an excellent taste!")


def _check_source_root():
    """
    Checks if the global source root variable is set correctly.
    """
    if not ODE_SOURCE_ROOT:
        logging.critical(
            "Couldn't work out the source root directory (did you forget to "
            "set the '$ODE_SOURCE_ROOT' environment variable?)"
        )


def _run_preset_mode():
    """Runs the composer in the preset mode."""
    logging.debug("Running %s in preset mode", NAME)
    logging.debug("Parsing the preset mode")

    if not config.ARGS.preset_file_names:
        preset_file_names = [
            os.path.join(HOME, ".anthem-composer-presets"),
            os.path.join(HOME, ".ode-composer-presets"),
            os.path.join(ODE_SOURCE_ROOT, ODE_REPO_NAME, PRESET_FILE_PATH)
        ]

    logging.debug("The preset files are %s", ", ".join(preset_file_names))

    if config.ARGS.show_presets:
        logging.info("The available presets are:")
        for name in sorted(
            get_all_preset_names(preset_file_names),
            key=str.lower
        ):
            print(name)
        return

    if not config.ARGS.preset:
        logging.critical("Missing the '--preset' option")

    preset_args = get_preset_options(
        None,
        preset_file_names,
        config.ARGS.preset
    )

    build_script_call_args = [sys.argv[0]]

    if config.ARGS.preset_run_mode == "configure":
        build_script_call_args += ["configure"]
    elif config.ARGS.preset_run_mode == "configure":
        build_script_call_args += ["compose"]

    if config.ARGS.dry_run:
        build_script_call_args += ["--dry-run"]
    # TODO Contemplate whether this should be able to be set from
    # preset mode
    if config.ARGS.jobs:
        build_script_call_args += ["--jobs", str(config.ARGS.jobs)]
    if config.ARGS.clean:
        build_script_call_args += ["--clean"]
    if config.ARGS.print_debug:
        build_script_call_args += ["--print-debug"]

    build_script_call_args += preset_args

    logging.info(
        "Using preset '%s', which expands to \n\n%s\n",
        config.ARGS.preset,
        shell.quote_command(build_script_call_args)
    )
    logging.debug(
        "The script will have '%s' as the Python executable\n",
        sys.executable
    )

    if config.ARGS.expand_build_script_invocation:
        logging.debug("The build script invocation is printed")
        return 0

    command_to_run = [sys.executable] + build_script_call_args

    shell.caffeinate(command_to_run)


def _run_configuring_mode():
    """
    Runs the composer in configuration mode and sets up the
    development and build environment.
    """
    set_up.set_up()
    clone.clone_dependencies()
    # TODO Write the JSON file for toolchain here.


def _run_composing_mode():
    """Runs the composer in build mode."""


def _main():
    """Enters the program and runs it."""
    argument_parser = _parse_arguments_into_namespace()

    # The logging level is the first thing to be set so it can be
    # utilized throughout the rest of the run.
    _set_logging_level()
    _check_and_print_python_version()
    _check_source_root()

    if config.ARGS.composer_mode == "preset":
        return _run_preset_mode()
    elif config.ARGS.composer_mode == "configure":
        return _run_configuring_mode()
    elif config.ARGS.composer_mode == "compose":
        return _run_composing_mode()

    argument_parser.error("{} wasn't in valid mode".format(NAME))


def run():
    """Runs the script when Couplet Composer is invoked."""
    sys.exit(_main())


if __name__ == "__main__":
    sys.exit(_main())
