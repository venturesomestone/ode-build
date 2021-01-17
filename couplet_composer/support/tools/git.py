# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the object that
represents Git in the toolchain of the build script.
"""

from argparse import Namespace

from ...build_directory import BuildDirectory

from ...target import Target

from ...tool import Tool


class Git(Tool):
    """A class for creating object that represents Git in the
    toolchain of the build script.
    """

    def __init__(
        self,
        args: Namespace,
        build_dir: BuildDirectory,
        target: Target
    ) -> None:
        """Initializes the Git tool object.

        Args:
            args (Namespace): A namespace that contains the
                parsed command line arguments.
            build_dir (BuildDirectory): The build directory
                object that is the main build directory of the
                run.
            target (Target): The current target.
        """
        super().__init__(
            key="git",
            cmd="git",
            name="Git",
            version=None,
            tool_files=None,
            args=args,
            build_dir=build_dir,
            target=target
        )

    def _download(self) -> str:
        """Downloads the asset or the source code of the
        tool.

        Returns:
            A 'str' that points to the downloads.
        """
        pass

    def _build(self, source_path: str) -> str:
        """Builds the tool from the sources.

        Args:
            source_path (str): The path to the source directory
                of the tool.

        Returns:
            An 'str' that is the path to the build Ninja
            executable.
        """
        pass
