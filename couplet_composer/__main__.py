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

"""The entry point of Couplet Composer."""

import sys

from datetime import datetime

from absl import app, logging

from .flags import FLAGS, register_flag_validators

from .support.values import NAME

from .support.variables import ODE_SOURCE_ROOT

from .util.date import date_difference, to_date_string


def _is_preset_mode():
    return FLAGS.preset or FLAGS["show-presets"].value


def _run_preset():
    """Runs the composer in the preset mode."""


def _run_configure():
    """
    Runs the composer in configuration mode and sets up the
    development and build environment.
    """


def _run_compose():
    """Runs the composer in build mode."""


def main(argv):
    """Enters the program and runs it."""
    if FLAGS["print-debug"].value:
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
            # The end-of-life date of Python 2
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

    if len(argv) <= 1:
        logging.fatal(
            "No build mode is defined: please use either 'configure' or "
            "'compose'"
        )

    # The preset mode is the same for both bootstrap and build
    # mode so it's checked for first.
    if _is_preset_mode():
        _run_preset()
    else:
        if sys.argv[1] == "configure":
            _run_configure()
        elif sys.argv[1] == "compose":
            _run_compose()
        else:
            # Composer must have either bootstrap or build
            # subcommand. However, this need should always be
            # satisfied as Composer should only be run via the
            # scripts that come with Obliging Ode.
            logging.fatal(
                "%s wasn't in either configure or compose mode",
                NAME
            )


def run():
    """
    Runs the script if Couplet Composer is invoked through
    'run.py'.
    """
    # The flag validators must be registered before running the
    # app as the app runs the validators and parses the flags.
    register_flag_validators()
    app.run(main)
    return 0
