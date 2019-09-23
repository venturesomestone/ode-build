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

import multiprocessing

from absl import flags


__all__ = ["FLAGS"]


FLAGS = flags.FLAGS


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
# Flags validators
# ------------------------------------------------------------- #


def register_flag_validators():
    """
    Registers the flag validators to be called before the app is
    run.
    """
