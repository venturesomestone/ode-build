# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that
represent the SDL dependency of the project that this build
script acts on.
"""

import os
import sys

from typing import Any

from ...support.archive_action import ArchiveAction

from ...util import http, shell

from ...binary_dependency import BinaryDependency

from ...build_directory import BuildDirectory

from ...invocation import Invocation


class SdlDependency(BinaryDependency):
    """A class for creating objects that represent the SDL
    dependency of the project that this build script acts on.
    """

    def _download(
        self,
        invocation: Invocation,
        build_dir: BuildDirectory
    ) -> str:
        """Downloads the asset or the source code of the
        dependency.

        Args:
            invocation (Invocation): The current invocation.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.

        Returns:
            A 'str' that points to the downloads.
        """
        tmp_dir = build_dir.temporary

        download_file = os.path.join(tmp_dir, "{}.tar.gz".format(self.key))

        download_url = "{repo}/SDL2-{version}.tar.gz".format(
                repo=self.repository,
                version=self.version
            )

        http.stream(
            url=download_url,
            destination=download_file,
            dry_run=invocation.args.dry_run,
            echo=invocation.args.verbose
        )

        source_dir = os.path.join(tmp_dir, self.key)

        shell.makedirs(
            path=source_dir,
            dry_run=invocation.args.dry_run,
            echo=invocation.args.verbose
        )
        shell.tar(
            path=download_file,
            action=ArchiveAction.extract,
            dest=source_dir,
            dry_run=invocation.args.dry_run,
            echo=invocation.args.verbose
        )

        return os.path.join(
            source_dir,
            [name for _, name, _ in os.walk(source_dir) if self.key in name][0]
        )

    def _build(
        self,
        source_path: str,
        invocation: Invocation,
        build_dir: BuildDirectory
    ) -> None:
        """Builds the dependency from the sources.

        Args:
            source_path (str): The path to the source directory
                of the dependency.
            invocation (Invocation): The current invocation.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.
        """
        tmp_build_dir = os.path.join(build_dir.temporary, "build")

        shell.makedirs(
            tmp_build_dir,
            dry_run=invocation.args.dry_run,
            echo=invocation.args.verbose
        )

        with shell.pushd(
            tmp_build_dir,
            dry_run=invocation.args.dry_run,
            echo=invocation.args.verbose
        ):
            shell.call(
                [
                    os.path.join(source_path, "configure"),
                    "--prefix={}".format(build_dir.dependencies)
                ],
                dry_run=invocation.args.dry_run,
                echo=invocation.args.verbose
            )
            shell.call(
                [invocation.runner.toolchain.make],
                dry_run=invocation.args.dry_run,
                echo=invocation.args.verbose
            )
            shell.call(
                [invocation.runner.toolchain.make, "install"],
                dry_run=invocation.args.dry_run,
                echo=invocation.args.verbose
            )
