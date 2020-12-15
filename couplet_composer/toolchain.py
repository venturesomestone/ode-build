# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the toolchain
of the build script.
"""

from .preset_runner import PresetRunner

from .runner import Runner


class Toolchain:
    """A class that that represents the toolchain of the build
    script.

    Attributes:
        runner (Runner): The runner that this toolchain belongs
            to.
    """

    def __init__(self, runner: Runner) -> None:
        """Initializes the toolchain object.

        Args:
            runner (Runner): The runner that this toolchain
                belongs to.
        """
        self.runner = runner

        # There is no need for toolchain in the preset mode.
        if isinstance(self.runner, PresetRunner):
            return
