# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the base class for the objects that
represent the dependencies of the project that this build script
acts on.
"""

import os

from collections import namedtuple

from typing import Any

from .support.archive_action import ArchiveAction

from .support.cmake_generator import CMakeGenerator

from .support.system import System

from .util import http, shell

from .build_directory import BuildDirectory

from .runner import Runner


class Dependency:
    """A class for creating objects that represent the
    dependencies of the project that this build script acts on.

    Attributes:
        key (str): The simple identifier of this dependency.
        name (str): The full name of this dependency.
        version (str): The required version of the dependency.
        commit (str): A required commit of the dependency.
        files (list): A list of the names of the files or file
            dictionaries with source and destination files that
            is used to check whether the dependency is installed
            and to copy the files on installation. The entries
            can be strings or tuples.
        test_only (bool): Whether or not the dependency is needed
            only when building the tests.
        benchmark_only (bool): Whether or not the dependency is
            needed only when building the benchmarkings.
        asset_name (str): The name of the asset that will be
            downloaded from GitHub by default.
        owner (str): The owner of the GitHub repository of this
            dependency.
        repository (str): The name of the GitHub repository of
            this dependency.
    """

    SOURCE_KEY = "src"
    DESTINATION_KEY = "dest"

    FileInfo = namedtuple("FileInfo", [SOURCE_KEY, DESTINATION_KEY])

    def __init__(
        self,
        key: str,
        name: str,
        version: str,
        commit: str,
        files: Any,
        test_only: bool,
        benchmark_only: bool,
        asset_name: str,
        repository: str
    ) -> None:
        """Initializes the dependency object.

        Args:
            key (str): The simple identifier of this dependency.
            name (str): The full name of this dependency.
            version (str): The required version of the
                dependency.
            commit (str): The required commit of the dependency.
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
        """
        self.key = key
        self.name = name
        self.version = version
        self.commit = commit
        self.library_files = list()

        # The possible configurations for the library files are
        # the following:
        # - a string
        # - a list with strings
        # - a dictionary with lists or strings
        if isinstance(files, str):
            self.library_files.append(os.path.join(*files.split("/")))
        elif isinstance(files, list):
            for f in files:
                if isinstance(f, dict):
                    self.library_files.append(self.FileInfo(
                        src=os.path.join(*f[self.SOURCE_KEY].split("/")),
                        dest=os.path.join(*f[self.DESTINATION_KEY].split("/"))
                    ))
                elif isinstance(f, str):
                    self.library_files.append(os.path.join(*f.split("/")))
                else:
                    raise ValueError  # TODO Add explanation or logging.
        elif isinstance(files, dict):
            # There are two cases: either the dict is the object
            # with source and destination or it is the object
            # with the different directories as keys. The 'source
            # and destination' case requires that both the source
            # and destination keys are present.
            if self.SOURCE_KEY in files and self.DESTINATION_KEY:
                self.library_files.append(self.FileInfo(
                    src=os.path.join(*f[self.SOURCE_KEY].split("/")),
                    dest=os.path.join(key, *f[self.DESTINATION_KEY].split("/"))
                ))
            else:
                for key, value in files.items():
                    if isinstance(value, str):
                        self.library_files.append(os.path.join(
                            key, *value.split("/")
                        ))
                    elif isinstance(value, list):
                        for f in files:
                            if isinstance(f, dict):
                                self.library_files.append(self.FileInfo(
                                    src=os.path.join(
                                        *f[self.SOURCE_KEY].split("/")
                                    ),
                                    dest=os.path.join(
                                        key,
                                        *f[self.DESTINATION_KEY].split("/")
                                    )
                                ))
                            elif isinstance(f, str):
                                self.library_files.append(os.path.join(
                                    key,
                                    *f.split("/")
                                ))
                            else:
                                raise ValueError  # TODO Add explanation or logging.
        else:
            self.library_files = None

        self.test_only = test_only
        self.benchmark_only = benchmark_only
        self.asset_name = asset_name

        if repository:
            self.owner, self.repository = repository.split("/")
        else:
            self.owner = None
            self.repository = None

    def __repr__(self) -> str:
        """Computes the string representation of the dependency.

        Returns:
            A string representation of the dependency.
        """
        return self.key

    def __str__(self) -> str:
        """Computes the formatted string representation of the dependency.

        Returns:
            A formatted string representation of the dependency.
        """
        return "{} {}".format(self.name, self.version)

    def install(
        self,
        runner: Runner,
        build_dir: BuildDirectory
    ) -> None:
        """Downloads, builds, and installs the dependency.

        Args:
            runner (Runner): The current runner.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.
        """
        source_dir = self._download(runner=runner, build_dir=build_dir)

        self._build(
            source_path=source_dir,
            runner=runner,
            build_dir=build_dir
        )

        shell.rmtree(
            build_dir.temporary,
            dry_run=runner.invocation.args.dry_run,
            echo=runner.invocation.args.verbose
        )

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

        if self.commit:
            with shell.pushd(
                tmp_dir,
                dry_run=runner.invocation.args.dry_run,
                echo=runner.invocation.args.verbose
            ):
                shell.call(
                    [
                        runner.toolchain.git,
                        "clone",
                        "https://github.com/{owner}/{repo}.git".format(
                            owner=self.owner,
                            repo=self.repository
                        )
                    ],
                    dry_run=runner.invocation.args.dry_run,
                    echo=runner.invocation.args.verbose
                )
            with shell.pushd(
                os.path.join(tmp_dir, self.repository),
                dry_run=runner.invocation.args.dry_run,
                echo=runner.invocation.args.verbose
            ):
                shell.call(
                    [runner.toolchain.git, "checkout", self.commit],
                    dry_run=runner.invocation.args.dry_run,
                    echo=runner.invocation.args.verbose
                )

            return os.path.join(tmp_dir, self.repository)
        else:
            download_file = os.path.join(tmp_dir, "{}.tar.gz".format(self.key))

            download_url = "https://api.github.com/repos/{owner}/{repo}/tarball/" \
                "refs/tags/v{version}".format(
                    owner=self.owner,
                    repo=self.repository,
                    version=self.version
                )

            http.stream(
                url=download_url,
                destination=download_file,
                headers={"Accept": "application/vnd.github.v3+json"},
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
        # if not os.path.isdir(os.path.join(build_dir.dependencies, "include")):
        #     shell.makedirs(
        #         os.path.join(build_dir.dependencies, "include"),
        #         dry_run=invocation.args.dry_run,
        #         echo=invocation.args.verbose
        #     )

        for f in self.library_files:
            dest_file = None
            src_file = None

            if isinstance(f, str):
                dest_file = os.path.join(build_dir.dependencies, f)
                src_file = os.path.join(source_path, f)
            elif isinstance(f, self.FileInfo):
                dest_file = os.path.join(build_dir.dependencies, f.dest)
                src_file = os.path.join(source_path, f.src)

            if os.path.isdir(dest_file):
                shell.rmtree(
                    dest_file,
                    dry_run=runner.invocation.args.dry_run,
                    echo=runner.invocation.args.print_debug
                )
            elif os.path.exists(dest_file):
                shell.rm(
                    dest_file,
                    dry_run=runner.invocation.args.dry_run,
                    echo=runner.invocation.args.print_debug
                )


            if os.path.isdir(src_file):
                shell.copytree(
                    src_file,
                    dest_file,
                    dry_run=runner.invocation.args.dry_run,
                    echo=runner.invocation.args.print_debug
                )
            else:
                shell.copy(
                    src_file,
                    dest_file,
                    dry_run=runner.invocation.args.dry_run,
                    echo=runner.invocation.args.print_debug
                )

    def should_install(
        self,
        runner: Runner,
        build_dir: BuildDirectory
    ) -> bool:
        """Tells whether the build of the dependency should be
        skipped.

        Args:
            runner (Runner): The current runner.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.

        Returns:
            A 'bool' telling if the dependency should be built.
        """
        installed_version = build_dir.installed_versions[self.key]

        if not installed_version or self.version != installed_version:
            return True

        if not self.library_files:
            return True

        found_file = False

        for lib_file in self.library_files:
            if isinstance(lib_file, str):
                if os.path.exists(os.path.join(build_dir.dependencies, lib_file)):
                    found_file = True
            elif isinstance(lib_file, self.FileInfo):
                if os.path.exists(
                    os.path.join(build_dir.dependencies, lib_file.dest)
                ):
                    found_file = True

        return not found_file
