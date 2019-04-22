# ------------------------------------------------------------- #
#                         Ode Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""The entry point of Ode Composer."""

import os
import sys

from datetime import datetime

from support.variables import ODE_SOURCE_ROOT

from util import diagnostics

from util.date import date_difference, to_date_string

from .core import run_bootstrap


def _run():
    if sys.version_info.major == 2:
        if sys.version_info.minor < 7:
            diagnostics.fatal(
                "You're using Python {}, and the smallest supported version "
                "is {}".format(sys.version, "2.7"))
        else:
            diagnostics.warn("You're using Python {}".format(sys.version))
            diagnostics.warn(
                "You should really update to Python 3 to make the world a "
                "better place!")
            eol_date = datetime.strptime(
                "2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            diagnostics.warn(
                "Also, the end of life of Python 2.7 is in {}, on 1 January, "
                "2020".format(to_date_string(date_difference(now, eol_date))))
    else:
        diagnostics.fine("You're using Python {}".format(sys.version))
        diagnostics.fine("You seem to have an excellent taste!")

    if not ODE_SOURCE_ROOT:
        diagnostics.fatal(
            "Couldn't work out the source root directory (did you forget to "
            "set the '$ODE_SOURCE_ROOT' environment variable?)")

    if not os.path.isdir(ODE_SOURCE_ROOT):
        diagnostics.fatal(
            "The source root directory '{}' doesn't exist (did you forget to "
            "set $ODE_SOURCE_ROOT environment variable?)".format(
                ODE_SOURCE_ROOT))

    if sys.argv[1] == "bootstrap" or sys.argv[1] == "boot":
        return run_bootstrap()
    else:
        diagnostics.fatal(
            "Using Ode Composer to build the project isn't supported yet")
        return 4


def main():
    """Enters the program and runs it."""
    sys.exit(_run())


if __name__ == "__main__":
    sys.exit(_run())
