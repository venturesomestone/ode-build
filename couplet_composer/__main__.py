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

from .support.environment import is_path_source_root

from .support.mode_names import \
    get_composing_mode_name, get_configuring_mode_name, get_preset_mode_name

from .support.project_names import get_project_name

from .util.date import date_difference, to_date_string

from . import args, modes


def _create_argument_parser(source_root):
    """
    Creates the argument parser for the script and returns the
    namespace containing the parsed arguments. This function
    isn't pure but depends on the global Python variable
    containing the command line arguments.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return args.create_argument_parser(source_root=source_root)


def _parse_arguments(parser):
    """
    Creates the argument values for the script and returns the
    namespace containing the parsed arguments. This function
    isn't pure but depends on the global Python variable
    containing the command line arguments.

    parser -- The argument parser that is used to parse the
    arguments.
    """
    return parser.parse_args()


def _set_logging_level(print_debug):
    """
    Sets the logging level according to the given parameters.
    This function isn't pure.

    print_debug -- Whether or not the debug-level logging should
    be allowed.
    """
    log_format = "%(message)s"
    if print_debug:
        logging.basicConfig(format=log_format, level=logging.DEBUG)
    else:
        logging.basicConfig(format=log_format, level=logging.INFO)


def _check_and_print_python_version():
    """
    Checks the current Python version and prints it. This
    function isn't pure.
    """
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
                "Also, the end of life of Python 2.7 was %s ago, on 1 "
                "January, 2020",
                to_date_string(date_difference(python2_end_of_life, now))
            )
    else:
        logging.debug("You're using Python %s", sys.version)
        logging.debug("You seem to have an excellent taste!")


def run_script(runner, arguments, source_root):
    """
    Runs the script with the given runner and arguments and
    returns the end code of the program. This function isn't pure
    as the functions called by it may modify the file system and
    run other scripts.

    runner -- The function that runs the preferred mode of the
    script.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return runner(arguments=arguments, source_root=source_root)


def _main():
    """
    Enters the program and runs it. This function isn't pure.
    """
    source_root = os.getenv("ODE_SOURCE_ROOT", os.getcwd())

    if not is_path_source_root(source_root):
        logging.critical(
            "The source root directory is invalid: %s",
            source_root
        )
        logging.warning(
            "The script didn't find the required file '%s'",
            os.path.join(source_root, "unsung-anthem", "CMakeLists.txt")
        )
        sys.exit(1)

    argument_parser = _create_argument_parser(source_root=source_root)
    arguments = _parse_arguments(argument_parser)

    # The logging level is the first thing to be set so it can be
    # utilized throughout the rest of the run.
    _set_logging_level(print_debug=arguments.print_debug)

    _check_and_print_python_version()

    def _resolve_mode(mode):
        if mode == get_preset_mode_name():
            return modes.run_in_preset_mode
        elif mode == get_configuring_mode_name():
            return modes.run_in_configuring_mode
        elif mode == get_composing_mode_name():
            return modes.run_in_composing_mode
        else:
            def _(_1, _2):
                argument_parser.error("{} wasn't in valid mode".format(
                    get_project_name()
                ))
                return 1
            return _

    mode_runner = _resolve_mode(mode=arguments.composer_mode)

    return run_script(
        runner=mode_runner,
        arguments=arguments,
        source_root=source_root
    )


def run():
    """Runs the script when Couplet Composer is invoked."""
    sys.exit(_main())


# The script can also be invoked by calling this script
if __name__ == "__main__":
    sys.exit(_main())
