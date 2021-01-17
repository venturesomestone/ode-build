# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class base for the objects that run
a run mode of the build script.
"""

import sys
import time

from abc import ABC, abstractmethod

from argparse import Namespace

from .support.build_variant import BuildVariant

from .support.cmake_generator import CMakeGenerator

from .support.system import System

from .util import shell

from .build_directory import BuildDirectory

from .target import Target

from .toolchain import Toolchain


class Runner(ABC):
    """A class for creating callable objects that represent the
    run mode runners of the build script.

    Attributes:
        args (Namespace): A namespace that contains the parsed
            command line arguments.
        source_root (str): The current source root.
    """

    def __init__(self, args: Namespace, source_root: str) -> None:
        """Initializes the runner object.

        Args:
            args (Namespace): A namespace that contains the
                parsed command line arguments.
            source_root (str): The current source root.
        """
        self.args = args
        self.source_root = source_root

    @abstractmethod
    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        pass

    @abstractmethod
    def clean(self) -> None:
        """Cleans the directories and files of the runner before
        building when clean build is run.
        """
        # Two spaces are required at the end of the first line as
        # the counter uses backspace characters.
        pass

    @abstractmethod
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
        pass
