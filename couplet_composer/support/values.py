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

"""
This support module contains constants that are needed in the
build.
"""

import os


# The name of the project.
NAME = "Couplet Composer"

# The path to the file containing the default values, relative to
# the Obliging Ode repository.
DEFAULTS_FILE_PATH = os.path.join("util", "composer", "defaults.json")

# The path to the default file containing the presets, relative
# to the Obliging Ode repository.
PRESET_FILE_PATH = os.path.join("util", "presets.ini")
