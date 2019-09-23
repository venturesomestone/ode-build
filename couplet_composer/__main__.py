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

import sys

from absl import app, logging


def main(argv):
    """Enters the program and runs it."""


def run():
    """
    Runs the script if Couplet Composer is invoked through
    'run.py'.

    This functions is impure.
    """
    # The flag validators must be registered before running the
    # app as the app runs the validators and parses the flags.
    register_flag_validators()
    app.run(main)
    return 0


if __name__ == "__main__":
    sys.exit(run())
