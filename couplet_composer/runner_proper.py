# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class base for the objects that run
a run mode of the build script.
"""

import sys
import time

from argparse import Namespace

from .support.build_variant import BuildVariant

from .support.cmake_generator import CMakeGenerator

from .support.cpp_standard import CppStandard

from .support.system import System

from .util import shell

from .build_directory import BuildDirectory

from .project import Project

from .runner import Runner

from .target import Target

from .toolchain import Toolchain


class RunnerProper(Runner):
    """A class for creating callable objects that represent the
    run mode runners of the build script.

    Attributes:
        target (Target): The target host that this runner is for.
        build_variant (str): The current build variant.
        generator (str): The current CMake generator.
        build_dir (BuildDirectory): The build directory object
            that is the main build directory of the run.
        toolchain (Toolchain): The toolchain that contains the
            tools of this run.
    """

    def __init__(
        self,
        args: Namespace,
        source_root: str,
        target: Target
    ) -> None:
        """Initializes the runner object.

        Args:
            args (Namespace): A namespace that contains the
                parsed command line arguments.
            source_root (str): The current source root.
            target (Target): The target host that this runner is
                for.
        """
        super().__init__(args=args, source_root=source_root)
        self.target = target
        self.build_variant = BuildVariant[self.args.build_variant]
        self.cmake_generator = CMakeGenerator[self.args.cmake_generator]
        self.build_dir = BuildDirectory(
            args=self.args,
            source_root=self.source_root,
            build_variant=self.build_variant,
            generator=self.cmake_generator,
            target=self.target
        )
        self.project = Project(
            source_root=self.source_root,
            repo=self.args.repository,
            script_package="couplet_composer",  # TODO Remove hard-coded value
            platform=self.target.system
        )
        self.toolchain = Toolchain(
            args=self.args,
            build_dir=self.build_dir,
            target=self.target
        )

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        if self.args.clean:
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

        # The build directories should be removed even in clean
        # configuration to avoid errors.
        shell.rmtree(
            self.build_dir.build,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.rmtree(
            self.build_dir.destination,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

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
