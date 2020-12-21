# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the base class for the objects that
represent the dependencies of the project that this build script
acts on.
"""

import os

from .build_directory import BuildDirectory

from .invocation import Invocation


class Dependency:
    """A class for creating objects that represent the
    dependencies of the project that this build script acts on.

    Attributes:
        key (str): The simple identifier of this dependency.
        name (str): The full name of this dependency.
        version (str): The required version of the dependency.
        library_file (str): The name of the file that is used to
            check whether the dependency is installed.
        test_only (bool): Whether or not the dependency is needed
            only when building the tests.
        benchmark_only (bool): Whether or not the dependency is
            needed only when building the benchmarkings
    """

    def __init__(
        self,
        key: str,
        name: str,
        version: str,
        library_file: str,
        test_only: bool,
        benchmark_only: bool
    ) -> None:
        """Initializes the dependency object.

        Args:
            key (str): The simple identifier of this dependency.
            name (str): The full name of this dependency.
            version (str): The required version of the
                dependency.
            library_file (str): The name of the file that is used
                to check whether the dependency is installed.
            test_only (bool): Whether or not the dependency is
                needed only when building the tests.
            benchmark_only (bool): Whether or not the dependency
                is needed only when building the benchmarkings.
        """
        self.key = key
        self.name = name
        self.version = version
        self.library_file = os.path.join(*library_file.split("/")) \
            if library_file is not None else None
        self.test_only = test_only
        self.benchmark_only = benchmark_only

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

    def install(self) -> None:
        """Downloads, builds, and installs the dependency.
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

        return not self.library_file or not os.path.exists(os.path.join(
            build_dir.dependencies, self.library_file
        ))
