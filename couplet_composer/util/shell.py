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
This utility module contains several shell helpers.

The functions in the module are intentionally and especially
internally not functional-like as the shell functionalities do
inherently not satisfy the requirements of functional-like code.
The functions that do shell calls can also end the execution of
the script on failure.

Nevertheless, the basic principles are preserved, i.e. functions
don't modify their parameters.
"""

from __future__ import print_function

import logging
import os
import pipes
import platform
import shutil
import subprocess
import sys

from ..support.platform_names import get_darwin_system_name

from .cache import cached


@cached
def get_dev_null():
    """
    Gives the pipe to which the ignored shell output is put to.
    """
    return getattr(subprocess, "DEVNULL", subprocess.PIPE)


def _quote(arg):
    return pipes.quote(str(arg))


def quote_command(args):
    """Quotes a command for printing it."""
    return " ".join([_quote(a) for a in args])


def _echo_command(dry_run, command, env=None, prompt="+ "):
    """
    Echoes a command to command line. Thus this function isn't
    pure.
    """
    output = []
    if env is not None:
        output.extend(["env"] + [
            _quote("%s=%s" % (k, v)) for (k, v) in sorted(env.items())
        ])
    output.extend([_quote(arg) for arg in command])
    file = sys.stderr
    if dry_run:
        file = sys.stdout
    print(prompt + " ".join(output), file=file)
    file.flush()


def call(command, stderr=None, env=None, dry_run=None, echo=None):
    """Runs the given command."""
    if dry_run or echo:
        _echo_command(dry_run, command, env=env)
    if dry_run:
        return
    _env = None
    if env is not None:
        _env = dict(os.environ)
        _env.update(env)
    try:
        subprocess.check_call(command, env=_env, stderr=stderr)
    except subprocess.CalledProcessError as e:
        logging.critical(
            "Command ended with status %d, stopping",
            e.returncode
        )
    except OSError as e:
        logging.critical(
            "Couldn't run '%s': %s",
            quote_command(command),
            e.strerror
        )


def capture(
    command,
    stderr=None,
    env=None,
    dry_run=None,
    echo=None,
    optional=False,
    allow_non_zero_exit=False
):
    """Runs the given command and returns its output."""
    if dry_run or echo:
        _echo_command(dry_run, command, env=env)
    if dry_run:
        return
    _env = None
    if env is not None:
        _env = dict(os.environ)
        _env.update(env)
    try:
        out = subprocess.check_output(command, env=_env, stderr=stderr)
        # Coerce to 'str' hack. Not py3 'byte', not py2
        # 'unicode'.
        return str(out.decode())
    except subprocess.CalledProcessError as e:
        if allow_non_zero_exit:
            return e.output
        if optional:
            return None
        logging.critical(
            "Command ended with status %d, stopping",
            e.returncode
        )
    except OSError as e:
        if optional:
            return None
        logging.critical(
            "Couldn't execute '%s': %s",
            quote_command(command),
            e.strerror
        )


def makedirs(path, dry_run=None, echo=None):
    """
    Creates the given directory and the in-between directories.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["mkdir", "-p", path])
    if dry_run:
        return
    if not os.path.isdir(path):
        os.makedirs(path)


def rmtree(path, dry_run=None, echo=None):
    """Removes a directory and its contents."""
    if dry_run or echo:
        _echo_command(dry_run, ["rm", "-rf", path])
    if dry_run:
        return
    if os.path.exists(path):
        # TODO Find out if ignore_errors is required
        shutil.rmtree(path, ignore_errors=True)


def rm(file, dry_run=None, echo=None):
    """Removes a file."""
    if dry_run or echo:
        _echo_command(dry_run, ["rm", "-f", file])
    if dry_run:
        return
    if os.path.islink(file):
        os.unlink(file)
    if os.path.exists(file):
        os.remove(file)


def caffeinate(command, env=None, dry_run=None, echo=None):
    """Runs a command during which system sleep is disabled."""
    command_to_run = list(command)
    # Disable system sleep, if possible.
    if platform.system() == get_darwin_system_name():
        command_to_run = ["caffeinate"] + list(command)
    call(command_to_run, env=env, dry_run=dry_run, echo=echo)
