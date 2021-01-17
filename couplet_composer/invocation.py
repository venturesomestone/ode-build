# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents an invocation
of the build script.
"""

import logging
import os
import platform

from collections import namedtuple

from .support.build_variant import BuildVariant

from .support.cmake_generator import CMakeGenerator

from .support.cpp_standard import CppStandard

from .support.run_mode import RunMode

from .support.system import System

from .util.formatter import Formatter

from .args_parser import create_args_parser

from .composing_runner import ComposingRunner

from .configuring_runner import ConfiguringRunner

from .preset_runner import PresetRunner

from .project import Project

from .runner_proper import RunnerProper

from .runner import Runner

from .target import Target


class Invocation:
    """A class for creating callable objects that represent
    invocations of the build script.

    Attributes:
        args (Namespace): A namespace that contains the parsed
            command line arguments.
        run_mode (RunMode): The run mode selected for the
            invocation instance.
        version (str): The version of the build script.
        name (str): The name of the build script.
        source_root (str): The root directory in which the
            project and the build files are.
        project (Project): The project object for the project
            this build script acts on.
        repository (str): The name of the repository directory of
            the project that is being built.
        platform (System): The platform that the build script is
            invoked on.
        targets (Targets): A named tuple of targets that contains
            the host target and other possible cross compile
            targets.
        runners (Runner): The runners for the targets.
    """

    TARGET_CATEGORIES = ["host", "cross_compile"]
    Targets = namedtuple("Targets", TARGET_CATEGORIES)
    Runners = namedtuple("Runners", TARGET_CATEGORIES)

    def __init__(self, version: str, name: str) -> None:
        """Initializes the invocation object for the current run.

        Args:
            version (str): The version of the build script.
            name (str): The name of the build script.
        """
        self.args, unknown_args = create_args_parser().parse_known_args()

        self.run_mode = RunMode(self.args.run_mode)
        self.version = version
        self.name = name
        self.source_root = os.getcwd()  # TODO Someone not playing by the rules might break this.

        # The logger must be initialized first.
        self._configure_logging()

        logging.info("Running %s version %s", self.name, self.version)

        if unknown_args:
            logging.warning(
                "The following command line arguments weren't "
                "recognized: {}".format(", ".join(unknown_args))
            )

        self.repository = self.args.repository
        self.platform = System(platform.system().lower())
        self.targets = self._resolve_targets()

        def _resolve_runner_type() -> RunnerProper:
            if self.run_mode is RunMode.configure:
                return ConfiguringRunner
            elif self.run_mode is RunMode.compose:
                return ComposingRunner
            else:
                raise ValueError

        if self.run_mode is not RunMode.preset:
            runner_type = _resolve_runner_type()

            self.runners = self.Runners(
                host=runner_type(
                    args=self.args,
                    source_root=self.source_root,
                    target=self.targets.host
                ),
                cross_compile=[
                    runner_type(
                        args=self.args,
                        source_root=self.source_root,
                        target=t
                    ) for t in self.targets.cross_compile
                ]
            )
        else:
            self.runners = self.Runners(
                host=PresetRunner(
                    args=self.args,
                    source_root=self.source_root
                ),
                cross_compile=list()
            )

    def __call__(self) -> int:
        """Invokes the build script with the current
        configuration.

        Returns:
            An 'int' that is equal to the exit code of the
            invocation.
        """
        logging.debug("Calling the invocation")

        # First the host runner should be run.
        self.runners.host()

        if self.run_mode is not RunMode.preset:
            for runner in self.runners.cross_compile:
                runner()

        return 0

    def _configure_logging(self) -> None:
        """Sets the logging level according to the configuration
        of the current run.

        This function isn't pure and doesn't return anything.
        """
        ch = logging.StreamHandler()

        if self.args.verbose:
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)

        ch.setFormatter(Formatter())

        # logging.getLogger().addHandler(ch)

    def _resolve_targets(self) -> namedtuple:
        """Resolves the target platforms for the build.

        Returns:
            A dictionary that contains the host target and the
            cross compile targets.
        """
        host_target = Target.resolve_host_target() \
            if self.run_mode is RunMode.preset \
            else Target.to_target(self.args.host_target)

        return self.Targets(host=host_target, cross_compile=list())
