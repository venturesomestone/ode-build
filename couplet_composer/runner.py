# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class base for the objects that run
a run mode of the build script.
"""

import logging
import os

from .invocation import Invocation


class Runner:
    """A class for creating callable objects that represent the
    run mode runners of the build script.
    """

    def __init__(self, invocation: Invocation) -> None:
        """Initializes the runner object.

        Args:
            invocation (Invocation): The invocation that this
                runner belongs to.
        """
        self.invocation = invocation

    def __call__(self, invocation: Invocation) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        pass
