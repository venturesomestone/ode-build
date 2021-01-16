# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that
represent the Lua dependency of the project that this build
script acts on.
"""

import os
import sys

from typing import Any

from ...support.archive_action import ArchiveAction

from ...util import http, shell

from ...build_directory import BuildDirectory

from ...dependency import Dependency

from ...runner import Runner


class LuaDependency(Dependency):
    """A class for creating objects that represent the Lua
    dependency of the project that this build script acts on.
    """

    def _download(
        self,
        runner: Runner,
        build_dir: BuildDirectory
    ) -> str:
        """Downloads the asset or the source code of the
        dependency.

        Args:
            runner (Runner): The current runner.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.

        Returns:
            A 'str' that points to the downloads.
        """
        tmp_dir = build_dir.temporary

        download_file = os.path.join(tmp_dir, "{}.tar.gz".format(self.key))

        download_url = "{repo}/{key}-{version}.tar.gz".format(
                repo=self.repository,
                key=self.key,
                version=self.version
            )

        http.stream(
            url=download_url,
            destination=download_file,
            dry_run=runner.invocation.args.dry_run,
            echo=runner.invocation.args.verbose
        )

        source_dir = os.path.join(tmp_dir, self.key)

        shell.makedirs(
            path=source_dir,
            dry_run=runner.invocation.args.dry_run,
            echo=runner.invocation.args.verbose
        )
        shell.tar(
            path=download_file,
            action=ArchiveAction.extract,
            dest=source_dir,
            dry_run=runner.invocation.args.dry_run,
            echo=runner.invocation.args.verbose
        )

        return os.path.join(
            source_dir,
            [name for _, name, _ in os.walk(source_dir) if self.key in name][0]
        )

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
            dry_run=runner.invocation.args.dry_run,
            echo=runner.invocation.args.verbose
        ):
            shell.call(
                [runner.toolchain.make],
                dry_run=runner.invocation.args.dry_run,
                echo=runner.invocation.args.verbose
            )
            shell.call(
                [
                    runner.toolchain.make,
                    "install",
                    "INSTALL_TOP={}".format(build_dir.dependencies)
                ],
                dry_run=runner.invocation.args.dry_run,
                echo=runner.invocation.args.verbose
            )
