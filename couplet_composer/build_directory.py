# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the main
build directory of the build script.
"""

import json
import os

from typing import Any

from .util import shell

from .invocation import Invocation


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
        temporary (str): The temporary directory.
        installed_versions (dict): The installed versions of the
            dependencies for the current configuration.
    """

    def __init__(self, invocation: Invocation) -> None:
        """Initializes the build directory object.

        Arguments:
            invocation (Invocation): The invocation that this
                build directory belongs to.
        """
        self._dry_run = invocation.args.dry_run
        self._verbose = invocation.args.verbose
        self._target = invocation.targets.host
        self._build_variant = "debug"  # TODO Use the correct value
        self._generator = "ninja"  # TODO Use the correct value

        self.path = os.path.join(invocation.source_root, "build")
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
        self.build = os.path.join(self.path, "build")
        self.destination = os.path.join(self.path, "dest")

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
            try:
                with open(self.versions_file) as f:
                    return json.load(f)
            except Exception:
                raise ValueError
        else:
            raise AttributeError
