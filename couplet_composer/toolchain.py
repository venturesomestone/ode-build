# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the toolchain
of the build script.
"""

from typing import Any

from .util.cache import cached

from .preset_runner import PresetRunner

from .runner import Runner


class Toolchain:
    """A class that that represents the toolchain of the build
    script.

    Attributes:
        runner (Runner): The runner that this toolchain belongs
            to.
    """

    def __init__(self, runner: Runner) -> None:
        """Initializes the toolchain object.

        Args:
            runner (Runner): The runner that this toolchain
                belongs to.
        """
        self.runner = runner

    @cached
    def __getattr__(self, name: str) -> Any:
        """Gives the attributes of the toolchain that aren't
        implemented to be found with '__getattribute__'.

        In toolchain this method is used to find the tools in the
        toolchain. If the tool isn't found by traditional search,
        it will be downloaded and built on demand by this
        function.

        The return value is cached to that the search and build
        isn't done twice.

        Args:
            name (str): The name of the attribute.

        Returns:
            The tool.

        Throws:
            AttributeError: Is thrown if the given tool isn't
                found or possible to be built.
        """
        return None
