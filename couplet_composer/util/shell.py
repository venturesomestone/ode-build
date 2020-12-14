# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains contains several shell helpers.
"""

import logging
import os
import pipes
import subprocess
import sys

from typing import Any


def _quote(arg: str) -> str:
    """Gives a shell-escaped version of the argument.

    Args:
        arg (str): The argument to escape.

    Returns:
        An 'str'.
    """
    return pipes.quote(str(arg))


def quote_command(args: list) -> str:
    """Quotes a command for printing it.

    Args:
        args (list): A list that is a command line argument.

    Returns:
        A shell-escaped 'str' version of the given command line
        argument.
    """
    return " ".join([_quote(a) for a in args])


def _echo_command(
    dry_run: bool,
    command: list,
    env: dict = None,
    prompt: str = "+ "
) -> None:
    """Echoes a command to command line.

    Args:
        dry_run (bool): Whether or not dry run is enabled.
        command (list): The command to print.
        env (dict): Key-value pairs as the environment variables.
        prompt (str): The prompt to print before the command.
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


def call(
    command: list,
    stderr: Any = None,
    env: dict = None,
    dry_run: bool = None,
    echo: bool = None
) -> None:
    """Runs the given command.

    Args:
        command (list): The command to call.
        stderr (any): An optional stderr file to use.
        env (dict): Key-value pairs as the environment variables.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
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
        sys.exit(e.returncode)
    except OSError as e:
        logging.critical(
            "Couldn't run '%s': %s",
            quote_command(command),
            e.strerror
        )
        sys.exit(1)
