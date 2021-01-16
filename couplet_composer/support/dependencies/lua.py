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

from ...invocation import Invocation


class LuaDependency(Dependency):
    """A class for creating objects that represent the Lua
    dependency of the project that this build script acts on.
    """

    def __init__(
        self,
        key: str,
        name: str,
        version: str,
        files: Any,
        test_only: bool,
        benchmark_only: bool,
        asset_name: str,
        repository: str
    ) -> None:
        """Initializes the Glad dependency object.

        Args:
            key (str): The simple identifier of this dependency.
            name (str): The full name of this dependency.
            version (str): The required version of the
                dependency.
            files (str | list | dict): The file or files that are
                used to check and copy the files of this
                dependency.
            test_only (bool): Whether or not the dependency is
                needed only when building the tests.
            benchmark_only (bool): Whether or not the dependency
                is needed only when building the benchmarkings.
            asset_name (str): The name of the asset that will be
                downloaded from GitHub by default.
            repository (str): The GitHub repository of this
                dependency.
            cmake_options (dict): The optional extra CMake
                options from the project's information file for
                this dependency.
        """
        super().__init__(
            key=key,
            name=name,
            version=version,
            files=files,
            test_only=test_only,
            benchmark_only=benchmark_only,
            asset_name=asset_name,
            repository=repository
        )

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

        download_url = "{repo}/{key}-{version}.tar.gz".format(
                repo=self.repository,
                key=self.key,
                version=self.version
            )

        http.stream(
            url=download_url,
            destination=download_file,
            headers={"Accept": "application/vnd.github.v3+json"},
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
        with shell.pushd(
            source_path,
            dry_run=invocation.args.dry_run,
            echo=invocation.args.verbose
        ):
            shell.call(
                [invocation.runner.toolchain.make],
                dry_run=invocation.args.dry_run,
                echo=invocation.args.verbose
            )
            shell.call(
                [
                    invocation.runner.toolchain.make,
                    "install",
                    "INSTALL_TOP={}".format(build_dir.dependencies)
                ],
                dry_run=invocation.args.dry_run,
                echo=invocation.args.verbose
            )
