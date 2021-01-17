# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the object that
represents CMake in the toolchain of the build script.
"""

import os

from ...util import http, shell

from ...build_directory import BuildDirectory

from ...runner import Runner

from ...tool import Tool

from ..archive_action import ArchiveAction

from ..system import System


class CMake(Tool):
    """A class for creating object that represents CMake in the
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

    def _download(
        self,
        runner: Runner,
        build_dir: BuildDirectory
    ) -> str:
        """Downloads the asset or the source code of the
        tool.

        Args:
            runner (Runner): The current runner.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script runner.

        Returns:
            A 'str' that points to the downloads.
        """
        tmp_dir = os.path.join(build_dir.temporary, self.key)

        if not os.path.isdir(tmp_dir):
            shell.makedirs(
                tmp_dir,
                dry_run=runner.args.dry_run,
                echo=runner.args.verbose
            )

        download_file = os.path.join(tmp_dir, "{}.{}".format(
            self.key,
            self._resolve_download_format(runner)
        ))

        download_url = "https://github.com/Kitware/CMake/releases/download/" \
            "v{version}/cmake-{version}-{platform}.{format}".format(
                version=self.version,
                platform=self._resolve_download_target(runner),
                format=self._resolve_download_format(runner)
            )

        http.stream(
            url=download_url,
            destination=download_file,
            headers={"Accept": "application/vnd.github.v3+json"},
            dry_run=runner.args.dry_run,
            echo=runner.args.verbose
        )

        source_dir = os.path.join(tmp_dir, self.key)

        shell.makedirs(
            path=source_dir,
            dry_run=runner.args.dry_run,
            echo=runner.args.verbose
        )
        shell.tar(
            path=download_file,
            action=ArchiveAction.unzip if runner.platform is System.windows
                   else ArchiveAction.extract,
            dest=source_dir,
            dry_run=runner.args.dry_run,
            echo=runner.args.verbose
        )

        return source_dir

    def _build(
        self,
        source_path: str,
        runner: Runner,
        build_dir: BuildDirectory
    ) -> str:
        """Builds the tool from the sources.

        Args:
            source_path (str): The path to the source directory
                of the tool.
            runner (Runner): The current runner.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                build script runner.

        Returns:
            An 'str' that is the path to the build CMake
            executable.
        """
        cmake_dir = os.path.join(
            source_path,
            "cmake-{version}-{platform}".format(
                version=self.version,
                platform=self._resolve_download_target(runner)
            )
        )
        dest_dir = os.path.join(
            build_dir.tools,
            "{}-{}".format(self.key, runner.targets.host)
        )

        if os.path.isdir(dest_dir):
            shell.rmtree(dest_dir)

        shell.copytree(
            cmake_dir,
            dest_dir,
            dry_run=runner.args.dry_run,
            echo=runner.args.verbose
        )
        shell.rmtree(
            source_path,
            dry_run=runner.args.dry_run,
            echo=runner.args.verbose
        )

        return os.path.join(
            dest_dir,
            self.resolve_binary(platform=runner.platform)
        )

    def _resolve_download_format(self, runner: Runner) -> str:
        """Resolves the file format of the CMake archive that
        will be downloaded.

        Args:
            runner (Runner): The current runner.

        Returns:
            The file format of the archive that will be
            downloaded.
        """
        if runner.platform is System.darwin or \
                runner.platform is System.linux:
            return "tar.gz"
        elif runner.platform is System.windows:
            return "zip"

        raise ValueError  # TODO Add explanation or logging.

    def _resolve_download_target(self, runner: Runner) -> str:
        """Resolves the target platform of the CMake archive that
        will be downloaded.

        Args:
            runner (Runner): The current runner.

        Returns:
            The name of the target platform to be used in the
            name of the archive that will be downloaded.
        """
        if runner.platform is System.darwin:
            return "Darwin-x86_64"
        elif runner.platform is System.linux:
            return "Linux-x86_64"
        elif runner.platform is System.windows:
            return "win32-x86"

        raise ValueError  # TODO Add explanation or logging.
