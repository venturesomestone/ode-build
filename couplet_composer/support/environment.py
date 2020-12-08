# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A support module that contains helper functions for creating
and checking the build environment.
"""

import os


def is_path_source_root(path: str, repo: str) -> bool:
    """Checks whether the given path is a valid root directory
    for the build script invocation.

    Args:
        path (str): The path that is checked.
        repo (str): The name of the repository directory in which
            the project to be built is.

    Returns:
        A Boolean value that is true if the given path is valid.
    """
    return os.path.exists(os.path.join(path, repo, "CMakeLists.txt"))


PRESET_FILE_PATH = os.path.join("util", "composer-presets.ini")
