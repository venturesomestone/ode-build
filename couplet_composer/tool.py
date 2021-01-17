# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the base class for the objects that
represent the tools of the toolchain of the build script.
"""

import os

from abc import ABC, abstractmethod

from argparse import Namespace

from typing import Any

from .util import shell

from .build_directory import BuildDirectory

from .target import Target

class Tool(ABC):
    """A class for creating objects that represent the tools of
        the toolchain of the build script.

    Attributes:
        key (str): The simple identifier of this tool.
        cmd (str): The command that is normally used to use the
            tool. Here it is used to find the tool preinstalled
            on the system.
        name (str): The full name of this tool.
        version (str): The required version of the tool.
        tool_files (str | list): A list of the names of the files
            or a name of the file that is used to check whether
            the tool is installed.
        args (Namespace): A namespace that contains the parsed
            command line arguments.
        build_dir (BuildDirectory): The build directory object
            that is the main build directory of the run.
        target (Target): The target host that this runner is for.
    """

    def __init__(
        self,
        key: str,
        cmd: str,
        name: str,
        version: str,
        tool_files: Any,
        args: Namespace,
        build_dir: BuildDirectory,
        target: Target
    ) -> None:
        """Initializes the tool object.

        Args:
            key (str): The simple identifier of this tool.
            cmd (str): The command that is normally used to use
                the tool. Here it is used to find the tool
                preinstalled on the system.
            name (str): The full name of this tool.
            version (str): The required version of the tool.
            tool_files (str | list): A list of the names of the
                files or a name of the file that is used to check
                whether the tool is installed.
            args (Namespace): A namespace that contains the
                parsed command line arguments.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                run.
            target (Target): The current target.
        """
        self.key = key
        self.cmd = cmd
        self.name = name
        self.version = version

        # The possible configurations for the tool files are
        # the following:
        # - a string
        # - a list with strings
        # - a dictionary with lists or strings
        if isinstance(tool_files, str):
            self.tool_files = os.path.join(*tool_files.split("/")) \
                if tool_files is not None else None
        elif isinstance(tool_files, list):
            self.tool_files = list()

            for f in tool_files:
                self.tool_files.append(os.path.join(*f.split("/")))
        else:
            self.tool_files = None

        self.args = args
        self.build_dir = build_dir
        self.target = target

    def __repr__(self) -> str:
        """Computes the string representation of the tool.

        Returns:
            A string representation of the tool.
        """
        return self.key

    def __str__(self) -> str:
        """Computes the formatted string representation of the
        tool.

        Returns:
            A formatted string representation of the tool.
        """
        return "{} {}".format(self.name, self.version)

    def install(self) -> str:
        """Downloads, builds, and installs the tool.

        Returns:
            An 'str' that is the path to the build tool
            executable.
        """
        source_dir = self._download()

        return self._build(source_dir)

    @abstractmethod
    def _download(self) -> str:
        """Downloads the asset or the source code of the
        tool.

        Returns:
            A 'str' that points to the downloads.
        """
        pass

    @abstractmethod
    def _build(self, source_path: str) -> str:
        """Builds the tool from the sources.

        Args:
            source_path (str): The path to the source directory
                of the tool.

        Returns:
            An 'str' that is the path to the build tool
            executable.
        """
        pass

    def _resolve_directory_name(self) -> str:
        """Gives the name of the directory in the local tools
        directory where the binaries of this tool are.

        Returns:
            An 'str' that is the name of the directory.
        """
        return "{}-{}".format(self.key, self.target)

    def find(self) -> str:
        """Finds the tool if possible and returns the path to it.

        Returns:
            An 'str' with the path to the tool executable, or
            None if it wasn't found.
        """
        system_tool = shell.which(
            self.cmd,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        if system_tool:
            return system_tool

        return self.resolve_local_binary()

    def resolve_local_binary(self) -> str:
        """Gives the path of the tool in the local tools
        directory if it is already installed there.

        Returns:
            An 'str' that points to the executable, or None if
            the tool is not found.
        """
        if isinstance(self.tool_files, str):
            tool_path = os.path.join(
                self.build_dir.tools,
                self._resolve_directory_name(),
                self.tool_files
            )
            if os.path.exists(tool_path):
                return tool_path
        elif isinstance(self.tool_files, list):
            for tool_file in self.tool_files:
                tool_path = os.path.join(
                    self.build_dir.tools,
                    self._resolve_directory_name(),
                    tool_file
                )
                if os.path.exists(tool_path):
                    return tool_path

        return None
