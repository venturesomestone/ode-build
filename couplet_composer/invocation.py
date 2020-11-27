# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
A module that contains the class that represents an invocation of
the build script.
"""


class Invocation:
    """A class that represents an invocation of the build script.

    Attributes:
        run_mode (RunMode): The run mode selected for the
            invocation instance
    """

    def __init__(self, run_mode):
        """Initializes the invocation object for the current run.

        Args:
            run_mode (RunMode): The run mode selected for this
                invocation
        """
        self.run_mode = run_mode
