# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the base class for the objects that
represent the tools of the toolchain of the build script.
"""

import os

from abc import ABC, abstractmethod

from typing import Any

from .support.archive_action import ArchiveAction

from .support.install_status import InstallStatus

from .util import http, shell

from .build_directory import BuildDirectory

from .invocation import Invocation


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
    """

    def __init__(
        self,
        key: str,
        cmd: str,
        name: str,
        version: str,
        tool_files: Any
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

    def install(
        self,
        invocation: Invocation,
        build_dir: BuildDirectory
    ) -> str:
        """Downloads, builds, and installs the tool.

        Args:
            invocation (Invocation): The current invocation.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.

        Returns:
            An 'str' that is the path to the build tool
            executable.
        """
        source_dir = self._download(invocation=invocation, build_dir=build_dir)

        return self._build(
            source_path=source_dir,
            invocation=invocation,
            build_dir=build_dir
        )

    @abstractmethod
    def _download(
        self,
        invocation: Invocation,
        build_dir: BuildDirectory
    ) -> str:
        """Downloads the asset or the source code of the
        tool.

        Args:
            invocation (Invocation): The current invocation.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.

        Returns:
            A 'str' that points to the downloads.
        """
        pass

    @abstractmethod
    def _build(
        self,
        source_path: str,
        invocation: Invocation,
        build_dir: BuildDirectory
    ) -> str:
        """Builds the tool from the sources.

        Args:
            source_path (str): The path to the source directory
                of the tool.
            invocation (Invocation): The current invocation.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.

        Returns:
            An 'str' that is the path to the build tool
            executable.
        """
        pass

    def resolve_install_status(
        self,
        invocation: Invocation,
        build_dir: BuildDirectory
    ) -> InstallStatus:
        """Tells whether the tool is already installed and how it
        is installed.

        Args:
            invocation (Invocation): The current invocation.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script invocation.

        Returns:
            A value of the enumeration InstallStatus.
        """
        system_tool = shell.which(
            self.cmd,
            dry_run=invocation.args.dry_run,
            echo=invocation.args.verbose
        )

        if system_tool:
            return InstallStatus.system

        return InstallStatus.none  # TODO
