# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class base for the objects that run
a run mode of the build script.
"""

import logging
import os

from argparse import Namespace

from .support.run_mode import RunMode

from .project import Project

from .target import Target


class Runner:
    """A class for creating callable objects that represent the
    run mode runners of the build script.
    """

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        pass
