# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the toolchain
of the build script.
"""

from typing import Any

from .support.tools.cmake import CMake

from .support.tools.git import Git

from .support.tools.make import Make

from .support.tools.ninja import Ninja

from .util.cache import cached

from .util import shell

from .runner import Runner


class Toolchain:
    """A class that that represents the toolchain of the build
    script.

    Private attributes:
        _tools (dict): A dictionary containing the internal
            objects for handling the data related to the tools.
        _tool_paths (dict): A dictionary containing the resolved
            paths to use the tools in the toolchain. The
            dictionary is modified in the invocation each time a
            new tool is required and found.

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
        self._tools = {
            "cmake": CMake(
                key="cmake",
                cmd="cmake",
                name="CMake",
                version="3.18.4",
                tool_files=CMake.resolve_binary(
                    platform=self.runner.invocation.platform
                )
            ),
            "git": Git(),
            "make": Make(),
            "ninja": Ninja(
                key="ninja",
                cmd="ninja",
                name="Ninja",
                version="1.9.0",
                tool_files=Ninja.resolve_binary(
                    platform=self.runner.invocation.platform
                )
            )
        }
        self._tool_paths = {}

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
        if name in self._tool_paths and self._tool_paths[name]:
            return self._tool_paths[name]
        else:
            tool_path = self._tools[name].find(
                invocation=self.runner.invocation,
                build_dir=self.runner.build_dir
            )

            if tool_path:
                self._tool_paths[name] = tool_path
                return tool_path

            tool_path = self._tools[name].install(
                invocation=self.runner.invocation,
                build_dir=self.runner.build_dir
            )

            if tool_path:
                self._tool_paths[name] = tool_path
                return tool_path

        raise AttributeError
