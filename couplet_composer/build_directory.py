# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the main
build directory of the build script.
"""

import os


class BuildDirectory:
    """A class that that represents the main build directory of
    the build script.

    Attributes:
        path (str): The path to the build directory root of the
            build script.
    """

    def __init__(self, source_root: str) -> None:
        """Initializes the build directory object.

        Arguments:
            source_root (str): The root directory of the
                invocation in which the project and the build
                files are.
        """
        self.path = os.path.join(source_root, "build")
