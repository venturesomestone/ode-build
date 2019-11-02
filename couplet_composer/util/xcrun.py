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

"""This utility module has the xcrun helpers."""

from .cache import cached

from . import shell


@cached
def find(command, dry_run=None, echo=None):
    """
    Returns the path for the given tool according to
    'xcrun --find'. If 'xcrun --find' cannot find the tool,
    return None. This function isn't pure.

    command -- The tool to be searched for.

    dry_run -- Whether to only print the command without running
    it.

    echo -- Whether to print the command before running it.
    """
    command_to_run = [
        "xcrun", "--find", command, "--sdk", "macosx", "--toolchain", "default"
    ]
    # "xcrun --find" prints to stderr when it fails to find the
    # given tool. TODO We swallow that output with a pipe.
    out = shell.capture(
        command_to_run,
        # stderr=shell.DEVNULL,
        dry_run=dry_run,
        echo=echo,
        optional=True
    )
    if out is None:
        return None
    return out.rstrip()
