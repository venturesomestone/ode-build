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

"""The support module containing shell helpers."""

from __future__ import print_function

import logging
import os
import pipes
import platform
import subprocess
import sys


DEVNULL = getattr(subprocess, "DEVNULL", subprocess.PIPE)
DRY_RUN = False
ECHO = False


def _quote(arg):
    return pipes.quote(str(arg))


def quote_command(args):
    """Quotes a command for printing it."""
    return " ".join([_quote(a) for a in args])


def _coerce_dry_run(dry_run_override):
    return DRY_RUN if dry_run_override is None else dry_run_override


def _coerce_echo(echo_override):
    return ECHO if echo_override is None else echo_override


def _echo_command(dry_run, command, env=None, prompt="+ "):
    output = []
    if env is not None:
        output += ["env"] + [
            _quote("%s=%s" % (k, v)) for (k, v) in sorted(env.items())
        ]
    output += [_quote(arg) for arg in command]
    file = sys.stderr
    if dry_run:
        file = sys.stdout
    print(prompt + " ".join(output), file=file)
    file.flush()


def call(command, stderr=None, env=None, dry_run=None, echo=None):
    """Runs the given command."""
    dry_run = _coerce_dry_run(dry_run)
    echo = _coerce_echo(echo)
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
            "Command ended with the status %d, stopping",
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
    """Runs the given command and return its output."""
    dry_run = _coerce_dry_run(dry_run)
    echo = _coerce_echo(echo)
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
            "Command ended with the status %d, stopping",
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
    dry_run = _coerce_dry_run(dry_run)
    echo = _coerce_echo(echo)
    if dry_run or echo:
        _echo_command(dry_run, ["mkdir", "-p", path])
    if dry_run:
        return
    if not os.path.isdir(path):
        os.makedirs(path)


def caffeinate(command, env=None, dry_run=False, echo=None):
    """
    Runs a command during which system sleep is disabled. By
    default, this ignores the 'shell.dry_run' flag.
    """
    # Disable system sleep, if possible.
    if platform.system() == "Darwin":
        # Don't mutate the caller's copy of the arguments.
        command = ["caffeinate"] + list(command)
    call(command, env=env, dry_run=dry_run, echo=echo)
