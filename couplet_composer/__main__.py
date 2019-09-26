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

from __future__ import print_function

import logging
import os
import sys

from datetime import datetime

from .support.presets import get_all_preset_names, get_preset_options

from .support.values import NAME, PRESET_FILE_PATH

from .support.variables import HOME, ODE_REPO_NAME, ODE_SOURCE_ROOT

from .util import shell

from .util.date import date_difference, to_date_string

from . import args, clone, config, set_up


def _is_preset_mode():
    return any([(opt.startswith("--preset") or opt == "--show-presets")
                for opt in sys.argv[1:]])


def _is_configure_mode():
    return any([opt == "configure" for opt in sys.argv[1:]])


def _is_compose_mode():
    return any([(opt == "compose" or opt == "build") for opt in sys.argv[1:]])


def _run_preset():
    """Runs the composer in the preset mode."""
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

    build_script_args = [sys.argv[0]]

    # The sub-command before other arguments.
    if _is_configure_mode():
        build_script_args += ["configure"]
    elif _is_compose_mode():
        build_script_args += ["compose"]

    if config.ARGS.dry_run:
        build_script_args += ["--dry-run"]
    # TODO Contemplate whether this should be able to be set from
    # preset mode
    if config.ARGS.jobs:
        build_script_args += ["--jobs", str(config.ARGS.jobs)]
    if config.ARGS.clean:
        build_script_args += ["--clean"]
    if config.ARGS.print_debug:
        build_script_args += ["--print-debug"]

    build_script_args += preset_args

    logging.info(
        "Using preset '%s', which expands to \n\n%s\n",
        config.ARGS.preset,
        shell.quote_command(build_script_args)
    )
    logging.debug(
        "The script will have '%s' as the Python executable\n",
        sys.executable
    )

    if config.ARGS.expand_build_script_invocation:
        logging.debug("The build script invocation is printed")
        return 0

    command_to_run = [sys.executable] + build_script_args

    shell.caffeinate(command_to_run)


def _run_configure():
    """
    Runs the composer in configuration mode and sets up the
    development and build environment.
    """
    set_up.set_up()
    clone.download_dependencies()


def _run_compose():
    """Runs the composer in build mode."""


def _main():
    """Enters the program and runs it."""
    if _is_preset_mode():
        parser = args.create_preset_argument_parser()
    else:
        parser = args.create_argument_parser()

    config.ARGS = parser.parse_args()

    if config.ARGS.print_debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # logging.debug("The non-flag arguments are %s", argv)

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
        logging.critical(
            "Couldn't work out the source root directory (did you forget to "
            "set the '$ODE_SOURCE_ROOT' environment variable?)"
        )

    # Check the sub-command separately before selecting the mode
    # in which the script is run for clarity.
    if not _is_configure_mode() and not _is_compose_mode():
        # Composer must have either configure or compose
        # subcommand. However, this need should always be
        # satisfied as Composer should only be run via the
        # scripts that come with Obliging Ode.
        logging.critical("%s wasn't in either configure or compose mode", NAME)

    # The preset mode is the same for both configure and compose
    # mode so it's checked for first.
    if _is_preset_mode():
        return _run_preset()
    else:
        if _is_configure_mode():
            return _run_configure()
        elif _is_compose_mode():
            return _run_compose()
        else:
            # Composer must have either configure or compose
            # subcommand. However, this need should always be
            # satisfied as Composer should only be run via the
            # scripts that come with Obliging Ode.
            logging.critical(
                "%s wasn't in either configure or compose mode",
                NAME
            )


def run():
    """Runs the script when Couplet Composer is invoked."""
    sys.exit(_main())


if __name__ == "__main__":
    sys.exit(_main())
