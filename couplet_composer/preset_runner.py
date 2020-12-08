# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
preset run mode of the build script.
"""

import logging
import os


from .support.run_mode import RunMode

from .support import environment, preset

from .runner import Runner


class PresetRunner(Runner):
    """A class for creating callable objects that represent the
    preset mode runners of the build script.
    """

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        preset_file_names = [os.path.join(
            self.invocation.source_root,
            self.invocation.repository,
            environment.PRESET_FILE_PATH
        )]

        # TODO Include the preset files from the command line
        # arguments
        logging.debug("The preset files are %s", ", ".join(preset_file_names))

        if self.invocation.args.show_presets:
            return self._show_presets(file_names=preset_file_names)

        if not self.invocation.args.preset_names:
            logging.critical("Missing the '--name' option")

        # TODO Compose the build call here.

        # TODO Print the next build script invocation.

        if self.invocation.args.expand_script_invocation:
            logging.debug("The build script invocation is printed")
            return 0

        # TODO Run the build call.

        return 0

    def _show_presets(self, file_names):
        """Shows the available presets and returns the end code
        of this execution.

        Args:
            file_names (list): The list of the names of the
                preset files.

        Returns:
            An 'int' that represents the exit code of the
            showing.
        """
        logging.info("The available presets are:")

        all_preset_names = preset.get_all_preset_names(file_names)
        preset_names = []

        for name in all_preset_names:
            stripped_name = None

            if name.startswith(RunMode.configure.value):
                stripped_name = name[len(preset.CONFIGURATION_PRESET_PREFIX):]
            elif name.startswith(RunMode.compose.value):
                stripped_name = name[len(preset.COMPOSING_PRESET_PREFIX):]
            else:
                stripped_name = name

            if stripped_name not in preset_names:
                preset_names.append(stripped_name)

        for name in sorted(preset_names, key=str.lower):
            print(name)

        return 0
