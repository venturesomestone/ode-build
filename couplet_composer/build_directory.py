# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the main
build directory of the build script.
"""

import json
import os

from typing import Any

from .invocation import Invocation


class BuildDirectory:
    """A class that that represents the main build directory of
    the build script.

    Private attributes:
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
        installed_versions (dict): The installed versions of the
            dependencies for the current configuration.
    """

    def __init__(self, invocation: Invocation) -> None:
        """Initializes the build directory object.

        Arguments:
            invocation (Invocation): The invocation that this
                build directory belongs to.
        """
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
        if "installed_versions" == name:
            versions_file = ".versions-{target}-{variant}".format(
                target=self._target,
                variant=self._build_variant
            )
            try:
                with open(os.path.join(self.local, versions_file)) as f:
                    return json.load(f)
            except:
                raise ValueError
        else:
            raise AttributeError
