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

"""
This support module contains constants that are needed in the
build.
"""

import os


# The name of the project.
NAME = "Couplet Composer"

# The name of the package.
PACKAGE_NAME = "couplet_composer"

# The path to the file containing the default values, relative to
# the Obliging Ode repository.
DEFAULTS_FILE_PATH = os.path.join("util", "composer", "defaults.json")

# The path to the default file containing the presets, relative
# to the Obliging Ode repository.
PRESET_FILE_PATH = os.path.join("util", "composer-presets.ini")
