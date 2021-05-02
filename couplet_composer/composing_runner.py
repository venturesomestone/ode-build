# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
composing run mode of the build script.
"""

import logging
import os

from argparse import Namespace

from .support.cmake_generator import CMakeGenerator

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
            "-DCMAKE_PREFIX_PATH={}".format(
                self.build_dir.dependencies.replace(os.path.sep, "/")
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
                "ON" if self.args.build_docs and self.toolchain.doxygen else "OFF"
            ),
            "-DCOMPOSER_CPP_STD={}".format(self.cpp_std.value),
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

        if self._resolve_make_program():
            cmake_call.append("-DCMAKE_MAKE_PROGRAM={}".format(
                self._resolve_make_program()
            ))

        for key in self.project.project_keys:
            cmake_call.append("-DCOMPOSER_{}_VERSION={}".format(
                key.upper(),
                getattr(self.project, "{}_version".format(key))
            ))
            cmake_call.append("-DCOMPOSER_{}_NAME={}".format(
                key.upper(),
                getattr(self.project, "{}_name".format(key))
            ))
            cmake_call.append("-DCOMPOSER_{}_TARGET={}".format(
                key.upper(),
                key
            ))

        if self.project.cmake_options:
            for key, value in self.project.cmake_options.items():
                if isinstance(value, bool):
                    cmake_call.append("-D{}={}".format(key.upper(), "ON" if value else "OFF"))
                else:
                    cmake_call.append("-D{}={}".format(key.upper(), str(value)))

        if self.args.cmake_options:
            for option in self.args.cmake_options:
                cmake_call.append("-D{}".format(option))

        # Print the warnings related to the CMake build
        if self.args.build_docs and not self.toolchain.doxygen:
            logging.warning(
                "Building the documentation is enabled but Doxygen wasn't "
                "found, thus, the documentation isn't built"
            )

        # TODO Run the lint before installing the docs
        with shell.pushd(self.build_dir.build):
            shell.call(
                cmake_call,
                env=None,
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )
            # TODO Take into account all of the different build
            # systems.
            shell.call(
                [self.toolchain.ninja],
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )
            shell.call(
                [self.toolchain.ninja, "install"],
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )

            if self.args.lint:
                self._run_linter()

            if self.args.build_docs:
                self._install_docs()

        shell.copytree(
            os.path.join(
                self.source_root,
                self.args.repository,
                "util",
                "bin"
            ),
            os.path.join(self.build_dir.destination, "bin"),
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        return 0

    def _resolve_make_program(self) -> str:
        """Resolves the path to the correct Make program for CMake.

        Returns:
            The path to the Make program.
        """
        if self.cmake_generator == CMakeGenerator.ninja:
            return self.toolchain.ninja

        return None

    def _run_linter(self) -> None:
        """Runs the linter on the project.
        """
        logging.warning("The run-clang-tidy is %s", self.toolchain.run_clang_tidy)

        linter_call = [
            self.toolchain.run_clang_tidy,
            "-clang-tidy-binary",
            self.toolchain.clang_tidy,
            "-j",
            str(self.args.jobs)
        ]
        shell.call(
            linter_call,
            env=None,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

    def _install_docs(self) -> str:
        """Runs a command during which system sleep is disabled.

        Args:
            data (Object): The data object read from the project
                data JSON file.
            key (str): The key for the data.

        Returns:
            The number, string, or object read from the project
            data JSON file.
        """
        if os.path.exists(self.build_dir.docs_destination):
            shell.rmtree(
                self.build_dir.docs_destination,
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )

        # TODO Add more possible docs formats besides HTML
        shell.makedirs(
            os.path.join(self.build_dir.docs_destination, "html"),
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        shell.copytree(
            os.path.join(self.build_dir.build, "docs", "doxygen", "html"),
            os.path.join(self.build_dir.docs_destination, "html"),
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
