# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the object that
represents Make in the toolchain of the build script.
"""

from ...build_directory import BuildDirectory

from ...runner import Runner

from ...tool import Tool


class Make(Tool):
    """A class for creating object that represents Make in the
    toolchain of the build script.
    """

    def __init__(self) -> None:
        """Initializes the Make tool object.
        """
        super().__init__(
            key="make",
            cmd="make",
            name="Make",
            version=None,
            tool_files=None
        )

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
        pass

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
            An 'str' that is the path to the build Ninja
            executable.
        """
        pass
