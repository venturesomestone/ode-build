# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that
represent the Glad dependency of the project that this build
script acts on.
"""

import sys

from typing import Any

from ...util import shell

from ...build_directory import BuildDirectory

from ...dependency import Dependency

from ...runner import Runner


class GladDependency(Dependency):
    """A class for creating objects that represent the Glad
    dependency of the project that this build script acts on.
    """

    def _build(
        self,
        source_path: str,
        runner: Runner,
        build_dir: BuildDirectory
    ) -> None:
        """Builds the dependency from the sources.

        Args:
            source_path (str): The path to the source directory
                of the dependency.
            runner (Runner): The current runner.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.
        """
        with shell.pushd(
            source_path,
            dry_run=runner.args.dry_run,
            echo=runner.args.verbose
        ):
            shell.call(
                [
                    sys.executable,
                    "-m",
                    "glad",
                    "--profile=core",
                    "--api=gl={}".format(runner.project.gl_version),
                    "--generator=c-debug",
                    "--spec=gl",
                    "--out-path={}".format(build_dir.dependencies)
                ],
                dry_run=runner.args.dry_run,
                echo=runner.args.verbose
            )
