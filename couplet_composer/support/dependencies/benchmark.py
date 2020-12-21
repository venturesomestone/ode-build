# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the base class for the objects that
represent the dependencies of the project that this build script
acts on.
"""

import os

from ...build_directory import BuildDirectory

from ...dependency import Dependency

from ...invocation import Invocation

from ..system import System


class Benchmark(Dependency):
    """A class for creating object that represent the Google
    Benchmark dependency.
    """

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

        if invocation.platform is System.windows:
            lib_file = os.path.join(
                build_dir.dependencies,
                "lib",
                "benchmark.lib"
            )
            if not os.path.exists(lib_file):
                lib_file = os.path.join(
                    build_dir.dependencies,
                    "lib",
                    "benchmarkd.lib"
                )
                return not os.path.exists(lib_file)
            else:
                return False
        else:
            lib_file = os.path.join(
                build_dir.dependencies,
                "lib",
                "libbenchmark.a"
            )
            if not os.path.exists(lib_file):
                lib_file = os.path.join(
                    build_dir.dependencies,
                    "lib",
                    "libbenchmarkd.a"
                )
                return not os.path.exists(lib_file)
            else:
                return False
