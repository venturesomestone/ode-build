#!/usr/bin/env python

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

"""
Helper script that is used to run the project in development
mode.
"""

import sys

from absl import app

from couplet_composer import __main__


if __name__ == "__main__":
    app.run(__main__.main)
