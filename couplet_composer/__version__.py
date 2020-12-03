# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""The version data of the build script. The version number is
given according to Semantic Versioning.
"""

import os


def get_version() -> str:
    """
    Gives a string that represents the current version of Couplet
    Composer.
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), "version")) as f:
            return str(f.read()).strip()
    except Exception:
        return None


__version__ = get_version()
