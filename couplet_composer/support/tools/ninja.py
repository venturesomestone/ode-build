# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the object that
represents Ninja in the toolchain of the build script.
"""

import os

from ...util import http, shell

from ...build_directory import BuildDirectory

from ...tool import Tool

from ..archive_action import ArchiveAction

from ..system import System


class Ninja(Tool):
    """A class for creating object that represents Ninja in the
    toolchain of the build script.

    Attributes:
        key (str): The simple identifier of this tool.
        name (str): The full name of this tool.
        version (str): The required version of the tool.
        tool_files (str | list): A list of the names of the files
            or a name of the file that is used to check whether
            the tool is installed.
    """

    @staticmethod
    def resolve_binary(platform: System) -> str:
        """Gives the Ninja binary to look for on current system
        in the local directories.

        Args:
            platform (System): The platform that the build script
                is invoked on.
        """
        if platform is System.darwin or platform is System.linux:
            return "ninja"
        elif platform is System.windows:
            return "ninja.exe"
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

        download_file = os.path.join(tmp_dir, "{}.zip".format(self.key))

        download_url = "https://github.com/ninja-build/ninja/releases/" \
            "download/v{version}/ninja-{platform}.zip".format(
                version=self.version,
                platform=self._resolve_download_target(self.target.system)
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
            action=ArchiveAction.unzip,
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
            An 'str' that is the path to the build Ninja
            executable.
        """
        dest_dir = os.path.join(
            self.build_dir.tools,
            "{}-{}".format(self.key, self.target),
            "bin"
        )

        if os.path.isdir(dest_dir):
            shell.rmtree(
                dest_dir,
                dry_run=self.args.dry_run,
                echo=self.args.verbose
            )

        shell.makedirs(
            dest_dir,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )

        shell.copy(
            os.path.join(
                source_path,
                "ninja.exe" if self.target.system is System.windows
                else "ninja"
            ),
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

    def _resolve_download_target(self, platform: System) -> str:
        """Resolves the target platform of the Ninja archive that
        will be downloaded.

        Args:
            platform (System): The platform that the build script
                is invoked on.

        Returns:
            The name of the target platform to be used in the
            name of the archive that will be downloaded.
        """
        if platform is System.darwin:
            return "mac"
        elif platform is System.linux:
            return "linux"
        elif platform is System.windows:
            return "win"

        raise ValueError  # TODO Add explanation or logging.
