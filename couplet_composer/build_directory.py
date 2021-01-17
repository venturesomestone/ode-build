# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the main
build directory of the build script.
"""

import argparse
import json
import os

from typing import Any

from .support.build_variant import BuildVariant

from .support.cmake_generator import CMakeGenerator

from .util import shell

from .target import Target


class BuildDirectory:
    """A class that that represents the main build directory of
    the build script.

    Private attributes:
        _dry_run (bool): Whether or not dry run is enabled.
        _verbose (bool): Whether or not verbose logging is
            enabled.
        _target (str): The string representation of the current
            target for creating paths.
        _build_variant (str): The string representation of the
            current build variant for creating paths.
        _generator (str): The string representation of the
            current CMake generator for creating paths.

    Attributes:
        path (str): The path to the build directory root of the
            build script.
        local (str): The path to the directory where the
            dependencies and tools are installed for the current
            configuration.
        dependencies (str): The root directory of the
            dependencies for the current configuration.
        versions_file (str): The file where the locally installed
            versions of the dependencies are.
        build (str): The path to the directory that is used to
            build the project.
        dest (str): The path to the directory where the build
            products are installed into.
        temporary (str): The temporary directory.
        installed_versions (dict): The installed versions of the
            dependencies for the current configuration.
    """

    def __init__(
        self,
        args: argparse.Namespace,
        source_root: str,
        build_variant: BuildVariant,
        generator: CMakeGenerator,
        target: Target
    ) -> None:
        """Initializes the build directory object.

        Arguments:
            args (Namespace): The parsed command line arguments
                of this run.
            source_root (str): The current source root.
            build_variant (BuildVariant): The build variant of
                this build.
            generator (CMakeGenerator): The CMake generator of
                this build.
            target (Target): The target that this build directory
                is for.
        """
        self._dry_run = args.dry_run
        self._verbose = args.verbose
        self._target = target
        self._build_variant = build_variant.name
        self._generator = generator.name

        self.path = os.path.join(source_root, "build")
        self.local = os.path.join(self.path, "local")
        self.dependencies = os.path.join(
            self.local,
            "lib",
            "{target}-{variant}".format(
                target=self._target,
                variant=self._build_variant
            )
        )
        self.tools = os.path.join(
            self.local,
            "bin",
            "{target}-{variant}".format(
                target=self._target,
                variant=self._build_variant
            )
        )
        versions_file_name = ".versions-{target}-{variant}".format(
            target=self._target,
            variant=self._build_variant
        )
        self.versions_file = os.path.join(self.local, versions_file_name)
        self.build = os.path.join(
            self.path,
            "build",
            "{target}-{variant}-{generator}".format(
                target=self._target,
                variant=self._build_variant,
                generator=self._generator
            )
        )
        self.destination = os.path.join(
            self.path,
            "dest",
            "{target}-{variant}".format(
                target=self._target,
                variant=self._build_variant
            )
        )

    def __getattr__(self, name) -> Any:
        """Gives the attributes of the build directory that
        aren't implemented to be found with '__getattribute__'.

        Args:
            name (str): The name of the attribute.

        Returns:
            The attribute.

        Throws:
            AttributeError: Is thrown if the given attribute
                isn't valid.
            ValueError: Is thrown if the value lookup fails.
        """
        if "temporary" == name:
            tmp_dir = os.path.join(self.path, "tmp")

            if not os.path.isdir(tmp_dir):
                shell.makedirs(
                    tmp_dir,
                    dry_run=self._dry_run,
                    echo=self._verbose
                )

            return tmp_dir
        elif "installed_versions" == name:
            if not os.path.exists(self.versions_file):
                return None
            try:
                with open(self.versions_file) as f:
                    return json.load(f)
            except OSError:
                raise ValueError
        else:
            raise AttributeError
