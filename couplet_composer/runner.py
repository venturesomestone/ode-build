# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class base for the objects that run
a run mode of the build script.
"""

import logging
import os

from .support.system import System

from .util import shell

from .invocation import Invocation


class Runner:
    """A class for creating callable objects that represent the
    run mode runners of the build script.

    Attributes:
        invocation (Invocation): The invocation that this runner
            belongs to.
    """

    def __init__(self, invocation: Invocation) -> None:
        """Initializes the runner object.

        Args:
            invocation (Invocation): The invocation that this
                runner belongs to.
        """
        self.invocation = invocation

    def __call__(self, invocation: Invocation) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        pass

    def caffeinate(
        self,
        command: list,
        env: dict = None,
        dry_run: bool = None,
        echo: bool = None
    ) -> None:
        """Runs a command during which system sleep is disabled.

        Args:
            command (list): The command to call.
            env (dict): Key-value pairs as the environment
                variables.
            dry_run (bool): Whether or not dry run is enabled.
            echo (bool): Whether or not the command must be
                printed.
        """
        command_to_run = list(command)
        # Disable system sleep, if possible.
        if self.invocation.platform is System.darwin:
            command_to_run = ["caffeinate"] + list(command)
        shell.call(command_to_run, env=env, dry_run=dry_run, echo=echo)
