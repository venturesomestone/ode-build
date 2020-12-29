# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains several shell helpers.
"""

import logging
import os
import pipes
import shutil
import subprocess
import sys
import tarfile
import zipfile

from contextlib import contextmanager

from typing import Any

from ..support.archive_action import ArchiveAction


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


def capture(
    command: list,
    stderr: Any = None,
    env: dict = None,
    dry_run: bool = None,
    echo: bool = None,
    optional: bool = False,
    allow_non_zero_exit: bool = False
) -> Any:
    """Runs the given command and returns its output.

    Args:
        command (list): The command to call.
        stderr (any): An optional stderr file to use.
        env (dict): Key-value pairs as the environment variables.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
        optional (bool): Whether the output of the command is
            optional.
        allow_non_zero_exit (bool): Whether the output is
            returned regardless of the success of the command.

    Returns:
        The output of the command.
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
        sys.exit(e.returncode)
    except OSError as e:
        if optional:
            return None
        logging.critical(
            "Couldn't execute '%s': %s",
            quote_command(command),
            e.strerror
        )
        sys.exit(1)


@contextmanager
def pushd(path: str, dry_run: bool = None, echo: bool = None) -> None:
    """Pushes the directory to the top of the directory stack
    and, thus, changes the current working directory.

    Args:
        path (str): The directory to switch to.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    old_dir = os.getcwd()
    if dry_run or echo:
        _echo_command(dry_run, ["pushd", path])
    if not dry_run:
        os.chdir(path)
    yield
    if dry_run or echo:
        _echo_command(dry_run, ["popd"])
    if not dry_run:
        os.chdir(old_dir)


def makedirs(path: str, dry_run: bool = None, echo: bool = None) -> None:
    """Creates the given directory and the in-between directories.

    Args:
        path (str): The directory to create.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["mkdir", "-p", path])
    if dry_run:
        return
    if not os.path.isdir(path):
        os.makedirs(path)


def copytree(
    src: str,
    dest: str,
    dry_run: bool = None,
    echo: bool = None
) -> None:
    """Copies a directory and its contents.

    Args:
        src (str): The directory to copy.
        dest (str): The directory where the source is copied to.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["cp", "-r", src, dest])
    if dry_run:
        return
    # A workaround
    if os.path.isdir(dest):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)  # , symlinks, ignore)
            else:
                shutil.copy2(s, d)
    else:
        shutil.copytree(src, dest)


def copy(
    src: str,
    dest: str,
    dry_run : bool = None,
    echo: bool = None
) -> None:
    """Copies a file.

    Args:
        src (str): The file to copy.
        dest (str): The directory or file where the source is
            copied to.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["cp", "-p", src, dest])
    if dry_run:
        return
    if os.path.islink(src):
        link = os.readlink(src)
        os.symlink(link, dest)
    else:
        shutil.copy2(src, dest)


def rmtree(path: str, dry_run: bool = None, echo: bool = None) -> None:
    """Removes a directory and its contents.

    Args:
        path (str): The directory to delete.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["rm", "-rf", path])
    if dry_run:
        return
    if os.path.exists(path):
        # TODO Find out if 'ignore_errors' is required
        shutil.rmtree(path, ignore_errors=True)


def rm(file: str, dry_run: bool = None, echo: bool = None) -> None:
    """Removes a file.

    Args:
        file (str): The file to delete.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["rm", "-f", file])
    if dry_run:
        return
    if os.path.islink(file):
        os.unlink(file)
    if os.path.exists(file):
        os.remove(file)


def which(command: str, dry_run: bool = None, echo: bool = None) -> str:
    """Returns path to an executable which would be run if the
    given command was called.

    If no command would be called, returns None.

    Args:
        command (str): The command to find.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.

    Returns:
        The full path of the command or None if the command is
        not found.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["which", command])
    if dry_run:
        return
    return shutil.which(command)


def tar(
    path: str,
    action: ArchiveAction = ArchiveAction.extract,
    dest: str = None,
    dry_run: bool = None,
    echo: bool = None
) -> None:
    """Performs actions on archives.

    Args:
        path (str): The tar archive that the utility acts on or
            that the tar archive is formed from.
        action (ArchiveAction): The action that is performed.
        dest (str): Either the destination that the archive is
            extracted to or the archive file that is created from
            the path.
        dry_run (bool): Whether or not dry run is enabled.
        echo (bool): Whether or not the command must be printed.
    """
    if dry_run or echo:
        if action is ArchiveAction.extract:
            if dest:
                _echo_command(dry_run, ["tar", "-xf", path, "-C", dest])
            else:
                _echo_command(dry_run, ["tar", "-xf", path])
        elif action is ArchiveAction.unzip:
            if dest:
                _echo_command(dry_run, ["unzip", "-d", dest, path])
            else:
                _echo_command(dry_run, ["unzip", path])

    if dry_run:
        return

    if action is ArchiveAction.extract:
        with tarfile.open(path) as archive:
            if dest:
                archive.extractall(dest)
            else:
                archive.extractall()
    elif action is ArchiveAction.unzip:
        with zipfile.ZipFile(path, "r") as archive:
            if dest:
                archive.extractall(dest)
            else:
                archive.extractall()
