# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the toolchain
of the build script.
"""

from argparse import Namespace

from typing import Any

from .support.tools.cmake import CMake

from .support.tools.doxygen import Doxygen

from .support.tools.git import Git

from .support.tools.llvm import LLVM

from .support.tools.make import Make

from .support.tools.ninja import Ninja

from .util.cache import cached

from .build_directory import BuildDirectory

from .target import Target


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

    LLVM_TOOL_NAME = "llvm"
    RUN_CLANG_TIDY_TOOL_NAME = "run_clang_tidy"

    def __init__(
        self,
        args: Namespace,
        build_dir: BuildDirectory,
        target: Target
    ) -> None:
        """Initializes the toolchain object.

        Args:
            args (Namespace): A namespace that contains the
                parsed command line arguments.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                run.
            target (Target): The current target.
        """
        self._tools = {
            "cmake": CMake(
                key="cmake",
                cmd="cmake",
                name="CMake",
                version="3.18.4",
                tool_files=CMake.resolve_binary(platform=target.system),
                args=args,
                build_dir=build_dir,
                target=target
            ),
            "doxygen": Doxygen(args=args, build_dir=build_dir, target=target),
            "git": Git(args=args, build_dir=build_dir, target=target),
            "llvm": LLVM(
                key="llvm",
                cmd="llvm",
                name="LLVM",
                version="10.0.0",
                tool_files=None,
                args=args,
                build_dir=build_dir,
                target=target
            ),
            "make": Make(args=args, build_dir=build_dir, target=target),
            "ninja": Ninja(
                key="ninja",
                cmd="ninja",
                name="Ninja",
                version="1.9.0",
                tool_files=Ninja.resolve_binary(platform=target.system),
                args=args,
                build_dir=build_dir,
                target=target
            )
        }
        self._tool_paths = {}

    @cached
    def __getattr__(self, name: str) -> str:
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
        if name == self.RUN_CLANG_TIDY_TOOL_NAME:
            if name in self._tool_paths and self._tool_paths[name]:
                return self._tool_paths[name]
            else:
                tool_path = self._tools[self.LLVM_TOOL_NAME].find_tool_extra("run-clang-tidy.py")

                if tool_path:
                    self._tool_paths[name] = tool_path
                    return tool_path

                tool_path = self._tools[self.LLVM_TOOL_NAME].install_run_clang_tidy()

                if tool_path:
                    self._tool_paths[name] = tool_path
                    return tool_path

            raise AttributeError
        elif name.startswith("clang_"):
            if name in self._tool_paths and self._tool_paths[name]:
                return self._tool_paths[name]
            else:
                tool_path = self._tools[self.LLVM_TOOL_NAME].find_tool_extra(name.replace("_", "-"))

                if tool_path:
                    self._tool_paths[name] = tool_path
                    return tool_path

                tool_path = self._tools[self.LLVM_TOOL_NAME].install_extra_tool(name.replace("_", "-"))

                if tool_path:
                    self._tool_paths[name] = tool_path
                    return tool_path

            raise AttributeError
        else:
            if name in self._tool_paths and self._tool_paths[name]:
                return self._tool_paths[name]
            else:
                tool_path = self._tools[name].find()

                if tool_path:
                    self._tool_paths[name] = tool_path
                    return tool_path

                tool_path = self._tools[name].install()

                if tool_path:
                    self._tool_paths[name] = tool_path
                    return tool_path

            raise AttributeError
