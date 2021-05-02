# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the object that
represents LLVM and various LLVM tools in the toolchain of the
build script.
"""

import os
import stat

from argparse import Namespace

from ...util import http, shell

from ...build_directory import BuildDirectory

from ...tool import Tool

from ..archive_action import ArchiveAction

from ..system import System


class LLVM(Tool):
    """A class for creating object that represents LLVM and
    various LLVM tools in the toolchain of the build script.
    """

    def _download(self) -> str:
        """Downloads the asset or the source code of the
        tool.

        Returns:
            A 'str' that points to the downloads.
        """
        tmp_dir = os.path.join(self.build_dir.temporary, self.key)

        if not os.path.isdir(tmp_dir):
            shell.makedirs(
                tmp_dir,
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )

        download_file = os.path.join(tmp_dir, "{}.{}".format(self.key, 'tar.xz'))

        download_url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/clang+llvm-{version}-{platform}.tar.xz".format(
            version=self.version,
            platform=self._resolve_download_target(self.target.system),
        )

        http.stream(
            url=download_url,
            destination=download_file,
            headers={"Accept": "application/vnd.github.v3+json"},
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        source_dir = os.path.join(tmp_dir, self.key)

        shell.makedirs(
            path=source_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.tar(
            path=download_file,
            action=ArchiveAction.extract,
            dest=source_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        return source_dir

    def _build(self, source_path: str) -> str:
        """Builds the tool from the sources.

        Args:
            source_path (str): The path to the source directory
                of the tool.

        Returns:
            An 'str' that is the path to the build tool
            executable.
        """
        raise NotImplementedError  # TODO Add explanation or logging

    def install_extra_tool(self, tool_name: str) -> str:
        """Downloads, builds, and installs the given Clang extra
        tool.

        Args:
            tool_name (str): The name of the extra tool to
                install.

        Returns:
            An 'str' that is the path to the build tool
            executable.
        """
        source_dir = self._download()

        return self._build_extra_tool(source_dir, tool_name)

    def install_run_clang_tidy(self) -> str:
        """Downloads, builds, and installs the run-clang-tidy.py
        utility script.

        Returns:
            An 'str' that is the path to the build tool
            executable.
        """
        source_dir = self._download_clang_tools_extra_source()

        return self._build_run_clang_tidy(source_dir)

    def _resolve_download_target(self, platform: System) -> str:
        """Resolves the target platform of the LLVM archive that
        will be downloaded.

        Args:
            platform (System): The current platform.

        Returns:
            The name of the target platform to be used in the
            name of the archive that will be downloaded.
        """
        if platform is System.darwin:
            return "x86_64-apple-darwin"
        elif platform is System.linux:
            return "x86_64-linux-gnu-ubuntu-18.04"
        elif platform is System.windows:
            return "win32"

        raise ValueError  # TODO Add explanation or logging.

    def _build_extra_tool(self, source_path: str, tool_name: str) -> str:
        """Builds the given LLVM extra tool from the sources.

        Args:
            source_path (str): The path to the source directory
                of the tool.
            tool_name (str): The name of the extra tool to
                install.

        Returns:
            An 'str' that is the path to the build extra tool
            executable.
        """
        bin_dir = os.path.join(
            source_path,
            "clang+llvm-{version}-{platform}".format(
                version=self.version,
                platform=self._resolve_download_target(self.target.system),
            ),
            "bin"
        )
        source_tool = os.path.join(bin_dir, tool_name)
        dest_dir = os.path.join(
            self.build_dir.tools,
            "{}-{}".format(self.key, self.target)
        )
        dest_tool = os.path.join(dest_dir, tool_name)

        if os.path.exists(dest_tool):
            shell.rm(dest_tool, dry_run=self.args.dry_run, echo=self.args.verbose)

        if not os.path.isdir(dest_dir):
            shell.makedirs(dest_dir, dry_run=self.args.dry_run, echo=self.args.verbose)

        shell.copy(
            source_tool,
            dest_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.rmtree(
            source_path,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        return dest_tool

    def _download_clang_tools_extra_source(self) -> str:
        """Downloads the asset or the source code of the
        tool.

        Returns:
            A 'str' that points to the downloads.
        """
        tmp_dir = os.path.join(self.build_dir.temporary, self.key)

        if not os.path.isdir(tmp_dir):
            shell.makedirs(
                tmp_dir,
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )

        download_file = os.path.join(tmp_dir, "{}.{}".format(self.key, 'tar.xz'))

        download_url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/clang-tools-extra-{version}.src.tar.xz".format(version=self.version)

        http.stream(
            url=download_url,
            destination=download_file,
            headers={"Accept": "application/vnd.github.v3+json"},
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        source_dir = os.path.join(tmp_dir, self.key)

        shell.makedirs(
            path=source_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.tar(
            path=download_file,
            action=ArchiveAction.extract,
            dest=source_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        return source_dir

    def _build_run_clang_tidy(self, source_path: str) -> str:
        """Builds the given LLVM extra tool from the sources.

        Args:
            source_path (str): The path to the source directory
                of the tool.
            tool_name (str): The name of the extra tool to
                install.

        Returns:
            An 'str' that is the path to the build extra tool
            executable.
        """
        bin_dir = os.path.join(
            source_path,
            "clang-tools-extra-{}.src".format(self.version),
            "clang-tidy",
            "tool"
        )
        source_tool = os.path.join(bin_dir, "run-clang-tidy.py")
        dest_dir = os.path.join(
            self.build_dir.tools,
            "{}-{}".format(self.key, self.target)
        )
        dest_tool = os.path.join(dest_dir, "run-clang-tidy.py")

        if os.path.exists(dest_tool):
            shell.rm(dest_tool, dry_run=self.args.dry_run, echo=self.args.verbose)

        if not os.path.isdir(dest_dir):
            shell.makedirs(dest_dir, dry_run=self.args.dry_run, echo=self.args.verbose)

        shell.copy(
            source_tool,
            dest_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.rmtree(
            source_path,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        shell.chmod(
            dest_tool,
            stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        return dest_tool
