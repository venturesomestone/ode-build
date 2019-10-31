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

from __future__ import absolute_import

from . import cache_util, shell


@cache_util.cached
def find(cmd):
    """
    Returns the path for the given tool, according to
    'xcrun --find', using the given sdk and toolchain.

    If 'xcrun --find' cannot find the tool, return None.
    """
    command = [
        "xcrun", "--find", cmd, "--sdk", "macosx", "--toolchain", "default"
    ]
    # "xcrun --find" prints to stderr when it fails to find the
    # given tool. We swallow that output with a pipe.
    out = shell.capture(
        command,
        stderr=shell.DEVNULL,
        dry_run=False,
        echo=False,
        optional=True
    )
    if out is None:
        return None
    return out.rstrip()


@cache_util.cached
def sdk_path(sdk):
    """
    Return the path string for given SDK, according to
    'xcrun --show-sdk-path'. If 'xcrun --show-sdk-path' cannot
    find the SDK, return None.
    """
    command = ['xcrun', '--sdk', sdk, '--show-sdk-path']
    out = shell.capture(command, dry_run=False, echo=False, optional=True)
    if out is None:
        return None
    return out.rstrip()
