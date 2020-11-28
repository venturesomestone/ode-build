# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
A module that contains the class that represents an invocation of
the build script.
"""

import logging
import sys

from .support.run_mode import RunMode

from .args_parser import create_args_parser


class Invocation:
    """A class for creating callable objects that represent
    invocations of the build script.

    Attributes:
        args (Namespace): A namespace that contains the parsed
            command line arguments.
        run_mode (RunMode): The run mode selected for the
            invocation instance.
        version (str): The version of the build script.
        name (str): The name of the build script.
        project_name (str): The name of the project this
            invocation acts on.
    """

    def __init__(self, version, name, project_name):
        """Initializes the invocation object for the current run.

        Args:
            version (str): The version of the build script.
            name (str): The name of the build script.
            project_name (str): The name of the project this
                invocation acts on.
        """
        self.args = create_args_parser().parse_args()
        self.run_mode = RunMode(self.args.run_mode)
        self.version = version
        self.name = name
        self.project_name = project_name


    def __call__(self):
        """Invokes the build script with the current
        configuration.
        """
        # The logger must be initialized first.
        self._set_logging_level()

        logging.info("Running %s version %s", self.name, self.version)


    def _set_logging_level(self):
        """Sets the logging level according to the configuration
        of the current run.

        This function isn't pure and doesn't return anything.
        """
        log_format = "%(message)s"

        if self.args.verbose:
            logging.basicConfig(format=log_format, level=logging.DEBUG)
        else:
            logging.basicConfig(format=log_format, level=logging.INFO)
