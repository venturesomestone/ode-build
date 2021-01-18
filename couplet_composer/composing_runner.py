# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
composing run mode of the build script.
"""

import os

from argparse import Namespace

from .support.cpp_standard import CppStandard

from .util import shell

from .runner_proper import RunnerProper

from .target import Target


class ComposingRunner(RunnerProper):
    """A class for creating callable objects that represent the
    composing mode runners of the build script.

    Attributes:
        cpp_std (CppStandard): The selected C++ standard.
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
        super().__init__(args=args, source_root=source_root, target=target)
        self.cpp_std = CppStandard[self.args.cpp_std.replace("+", "p")]

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        super().__call__()

        if not os.path.isdir(self.build_dir.build):
            shell.makedirs(
                self.build_dir.build,
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )

        cmake_call = [
            self.toolchain.cmake,
            os.path.join(
                self.source_root,
                self.args.repository
            ),
            "-G",
            self.cmake_generator.value,
            "-DCMAKE_BUILD_TYPE={}".format(
                self.build_variant.value
            ),
            "-DCMAKE_INSTALL_PREFIX={}".format(
                self.build_dir.destination.replace(os.path.sep, "/")
            ),
            "-DCOMPOSER_BUILD_TEST={}".format(
                "ON" if self.args.build_test else "OFF"
            ),
            "-DCOMPOSER_BUILD_BENCHMARK={}".format(
                "ON" if self.args.build_benchmark else "OFF"
            ),
            "-DCOMPOSER_BUILD_DOCS={}".format(
                "ON" if self.args.build_docs else "OFF"  # TODO Also check that Doxygen is found
            ),
            "-DCOMPOSER_CODE_COVERAGE={}".format(
                "ON" if self.args.coverage else "OFF"
            ),
            "-DCOMPOSER_CXX_STD={}".format(self.cpp_std.value),
            "-DCOMPOSER_LOCAL_PREFIX={}".format(
                self.build_dir.dependencies.replace(os.path.sep, "/")
            ),
            "-DCOMPOSER_OPENGL_VERSION_MAJOR={}".format(
                self.project.gl_version.split(".")[0]
            ),
            "-DCOMPOSER_OPENGL_VERSION_MINOR={}".format(
                self.project.gl_version.split(".")[1]
            )
        ]

        for key in self.project.project_keys:
            cmake_call.append("-DCOMPOSER_{}_VERSION={}".format(
                key.upper(),
                getattr(self.project, "{}_version".format(key))
            ))
            cmake_call.append("-DCOMPOSER_{}_NAME={}".format(
                key.upper(),
                getattr(self.project, "{}_name".format(key))
            ))

        with shell.pushd(self.build_dir.build):
            shell.call(
                cmake_call,
                env=None,
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )

        return 0
