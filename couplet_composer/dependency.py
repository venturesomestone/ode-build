# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the base class for the objects that
represent the dependencies of the project that this build script
acts on.
"""

import os

from typing import Any

from .support.system import System

from .build_directory import BuildDirectory

from .invocation import Invocation


class Dependency:
    """A class for creating objects that represent the
    dependencies of the project that this build script acts on.

    Attributes:
        key (str): The simple identifier of this dependency.
        name (str): The full name of this dependency.
        version (str): The required version of the dependency.
        library_files (str | list): A list of the names of the
            files or a name of the file that is used to check
            whether the dependency is installed.
        test_only (bool): Whether or not the dependency is needed
            only when building the tests.
        benchmark_only (bool): Whether or not the dependency is
            needed only when building the benchmarkings
        asset_name (str): The name of the asset that will be
            downloaded from GitHub by default.
    """

    def __init__(
        self,
        key: str,
        name: str,
        version: str,
        library_files: Any,
        test_only: bool,
        benchmark_only: bool,
        asset_name: str
    ) -> None:
        """Initializes the dependency object.

        Args:
            key (str): The simple identifier of this dependency.
            name (str): The full name of this dependency.
            version (str): The required version of the
                dependency.
            library_files (str | list): A list of the names of
                the files or a name of the file that is used to
                check whether the dependency is installed.
            test_only (bool): Whether or not the dependency is
                needed only when building the tests.
            benchmark_only (bool): Whether or not the dependency
                is needed only when building the benchmarkings.
            asset_name (str): The name of the asset that will be
                downloaded from GitHub by default.
        """
        self.key = key
        self.name = name
        self.version = version

        # The possible configurations for the library files are
        # the following:
        # - a string
        # - a list with strings
        # - a dictionary with lists or strings
        if isinstance(library_files, str):
            self.library_files = os.path.join(*library_files.split("/")) \
                if library_files is not None else None
        elif isinstance(library_files, list):
            self.library_files = list()

            for f in library_files:
                self.library_files.append(os.path.join(*f.split("/")))
        else:
            self.library_files = None

        self.test_only = test_only
        self.benchmark_only = benchmark_only
        self.asset_name = asset_name

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

    def install(self, build_dir: BuildDirectory) -> None:
        """Downloads, builds, and installs the dependency.

        Args:
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.
        """
        pass

    def should_install(
        self,
        invocation: Invocation,
        build_dir: BuildDirectory
    ) -> bool:
        """Tells whether the build of the dependency should be
        skipped.

        Args:
            invocation (Invocation): The current invocation.
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

        if isinstance(self.library_files, str):
            return os.path.exists(
                os.path.join(build_dir.dependencies, self.library_files)
            )
        elif isinstance(self.library_files, list):
            found = False

            for lib_file in self.library_files:
                if os.path.exists(
                    os.path.join(build_dir.dependencies, lib_file)
                ):
                    found = True

            return not found
        elif isinstance(self.library_files, dict):
            if invocation.platform in self.library_files:
                entry = self.library_files[invocation.platform]

                if isinstance(entry, str):
                    return os.path.exists(
                        os.path.join(build_dir.dependencies, entry)
                    )
                elif isinstance(entry, list):
                    found = False

                    for lib_file in entry:
                        if os.path.exists(
                            os.path.join(build_dir.dependencies, lib_file)
                        ):
                            found = True

                    return not found

        return False  # TODO Is this a good fallback value?
