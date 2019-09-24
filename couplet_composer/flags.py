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

"""The command line flags of Couplet Composer."""

import json
import multiprocessing
import os

from absl import flags

from .support.values import DEFAULTS_FILE_PATH

from .support.variables import \
    ANTHEM_NAME, ODE_BUILD_ROOT, ODE_NAME, ODE_REPO_NAME, ODE_SOURCE_ROOT


__all__ = ["FLAGS"]


FLAGS = flags.FLAGS


def _get_defaults():
    with open(
        os.path.join(ODE_SOURCE_ROOT, ODE_REPO_NAME, DEFAULTS_FILE_PATH)
    ) as f:
        return json.load(f)


ODE_VERSION = _get_defaults()["ode"]["version"]
ANTHEM_VERSION = _get_defaults()["anthem"]["version"]


# ------------------------------------------------------------- #
# Top-level options
# ------------------------------------------------------------- #

flags.DEFINE_boolean(
    "dry-run",
    False,
    "Don't actually run any commands; just print them.",
    short_name="n"
)
flags.DEFINE_alias("just-print", "dry-run")
flags.DEFINE_boolean("print-debug", False, "Produce debugging output.")
flags.DEFINE_integer(
    "jobs",
    multiprocessing.cpu_count(),
    "Specify the number of parallel build jobs to use.",
    short_name="j"
)


# ------------------------------------------------------------- #
# Common build options
# ------------------------------------------------------------- #

flags.DEFINE_string(
    "install-prefix",
    os.path.join(ODE_BUILD_ROOT, "local"),
    "Install the final build products to the given path."
)
flags.DEFINE_string(
    "ode-version",
    ODE_VERSION,
    "Set the version of the built {} product.".format(ODE_NAME)
)
flags.DEFINE_string(
    "anthem-version",
    ANTHEM_VERSION,
    "Set the version of the built {} product.".format(ANTHEM_NAME)
)


# ------------------------------------------------------------- #
# Preset mode options
# ------------------------------------------------------------- #

flags.DEFINE_list(
    "preset-files",
    None,
    "Search for build presets in the given files."
)
flags.DEFINE_string(
    "preset",
    None,
    "Use the given build preset.",
    short_name="P"
)
flags.DEFINE_boolean(
    "show-presets",
    False,
    "Only list the presets in the preset files."
)
flags.DEFINE_boolean(
    "expand-build-script-invocation",
    False,
    "Only show the command that the build would be called with."
)


# ------------------------------------------------------------- #
# Flags validators
# ------------------------------------------------------------- #

def register_flag_validators():
    """
    Registers the flag validators to be called before the app is
    run.
    """
