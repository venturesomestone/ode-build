# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class base for the objects that run
a run mode of the build script.
"""

import sys
import time

from .support.system import System

from .util import shell

from .build_directory import BuildDirectory

from .invocation import Invocation

from .target import Target

from .toolchain import Toolchain


class Runner:
    """A class for creating callable objects that represent the
    run mode runners of the build script.

    Attributes:
        invocation (Invocation): The invocation that this runner
            belongs to.
        build_dir (BuildDirectory): The build directory object
            that is the main build directory of the build script
            invocation.
        toolchain (Toolchain): The toolchain that contains the
            tools of this run.
        target (Target): The target host that this runner is for.
    """

    def __init__(self, invocation: Invocation, target: Target) -> None:
        """Initializes the runner object.

        Args:
            invocation (Invocation): The invocation that this
                runner belongs to.
            target (Target): The target host that this runner is
                for.
        """
        self.invocation = invocation
        self.build_dir = BuildDirectory(
            args=self.invocation.args,
            source_root=self.invocation.source_root,
            build_variant=self.invocation.build_variant,
            generator=self.invocation.generator,
            target=target
        )
        self.toolchain = Toolchain(runner=self)
        self.target = target

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        if self.invocation.args.clean:
            self.clean()

        return 0

    def clean(self) -> None:
        """Cleans the directories and files of the runner before
        building when clean build is run.
        """
        # Two spaces are required at the end of the first line as
        # the counter uses backspace characters.
        sys.stdout.write("\033[31mStarting a clean build in  \033[0m")
        for i in reversed(range(0, 4)):
            sys.stdout.write("\033[31m\b{!s}\033[0m".format(i))
            sys.stdout.flush()
            time.sleep(1)
        print("\033[31m\b\b\b\bnow.\033[0m")

        # TODO Delete the common directories

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
