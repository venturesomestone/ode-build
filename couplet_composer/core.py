# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

import sys

from . import bootstrap


def _is_preset_mode():
    return any([(opt.startswith("--preset") or opt == "--show-presets")
               for opt in sys.argv[1:]])


def run_bootstrap():
    """Runs the program in bootstrap mode."""
    if _is_preset_mode():
        return bootstrap.run_preset()
    else:
        return bootstrap.run()
