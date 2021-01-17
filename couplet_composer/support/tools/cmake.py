# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the object that
represents CMake in the toolchain of the build script.
"""

import os

from argparse import Namespace

from ...util import http, shell

from ...build_directory import BuildDirectory

from ...tool import Tool

from ..archive_action import ArchiveAction

from ..system import System


class CMake(Tool):
    """A class for creating object that represents CMake in the
    toolchain of the build script.
    """

    @staticmethod
    def resolve_binary(platform: System) -> str:
        """Gives the CMake binary to look for on current system
        in the local directories.

        Args:
            platform (System): The platform that the build script
                is invoked on.
        """
        if platform is System.darwin:
            return os.path.join("CMake.app", "Contents", "bin", "cmake")
        elif platform is System.linux:
            return os.path.join("bin", "cmake")
        elif platform is System.windows:
            return os.path.join("bin", "cmake,exe")
        raise ValueError  # TODO Add explanation or logging.

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

        download_file = os.path.join(tmp_dir, "{}.{}".format(
            self.key,
            self._resolve_download_format(self.target.system)
        ))

        download_url = "https://github.com/Kitware/CMake/releases/download/" \
            "v{version}/cmake-{version}-{platform}.{format}".format(
                version=self.version,
                platform=self._resolve_download_target(self.target.system),
                format=self._resolve_download_format(self.target.system)
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
            action=ArchiveAction.unzip if self.target.system is System.windows
                   else ArchiveAction.extract,
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
            An 'str' that is the path to the build CMake
            executable.
        """
        cmake_dir = os.path.join(
            source_path,
            "cmake-{version}-{platform}".format(
                version=self.version,
                platform=self._resolve_download_target(self.target.system)
            )
        )
        dest_dir = os.path.join(
            self.build_dir.tools,
            "{}-{}".format(self.key, self.target)
        )

        if os.path.isdir(dest_dir):
            shell.rmtree(dest_dir)

        shell.copytree(
            cmake_dir,
            dest_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.rmtree(
            source_path,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        return os.path.join(
            dest_dir,
            self.resolve_binary(platform=self.target.system)
        )

    def _resolve_download_format(self, platform: System) -> str:
        """Resolves the file format of the CMake archive that
        will be downloaded.

        Args:
            platform (System): The current platform.

        Returns:
            The file format of the archive that will be
            downloaded.
        """
        if platform is System.darwin or platform is System.linux:
            return "tar.gz"
        elif platform is System.windows:
            return "zip"

        raise ValueError  # TODO Add explanation or logging.

    def _resolve_download_target(self, platform: System) -> str:
        """Resolves the target platform of the CMake archive that
        will be downloaded.

        Args:
            platform (System): The current platform.

        Returns:
            The name of the target platform to be used in the
            name of the archive that will be downloaded.
        """
        if platform is System.darwin:
            return "Darwin-x86_64"
        elif platform is System.linux:
            return "Linux-x86_64"
        elif platform is System.windows:
            return "win32-x86"

        raise ValueError  # TODO Add explanation or logging.
