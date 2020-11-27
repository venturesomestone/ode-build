# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
A module that contains the class that represents an invocation of
the build script.
"""

import sys

from .support.run_mode import RunMode

from .args_parser import create_args_parser


class Invocation:
    """A class that represents an invocation of the build script.

    Attributes:
        run_mode (RunMode): The run mode selected for the
            invocation instance
    """

    def __init__(self):
        """Initializes the invocation object for the current run.
        """
        self.args = create_args_parser().parse_args()
        self.run_mode = RunMode(self.args.run_mode)
