# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
preset run mode of the build script.
"""

import logging
import os
import sys

from typing import List

from .support.run_mode import RunMode

from .support import environment, preset

from .util import shell

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

        if not self.invocation.args.preset_name:
            logging.critical("Missing the '--name' option")

        build_call = self._compose_call(preset_file_names=preset_file_names)

        logging.info(
            "Using preset '%s', which expands to \n\n%s\n",
            self.invocation.args.preset_name,
            shell.quote_command(build_call)
        )

        logging.debug(
            "The script will use '%s' as the Python executable\n",
            sys.executable
        )

        if self.invocation.args.expand_script_invocation:
            logging.debug("The build script invocation is printed")
            return 0

        # TODO Run the build call.

        return 0

    @staticmethod
    def _show_presets(file_names):
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

    def _compose_call(self, preset_file_names: List[str]) -> list:
        """Creates a list that contains the complete call to
        invoke the build script using the selected preset.

        Args:
            preset_file_names (list): The files from which the
                presets are read.

        Returns:
            A list that contains the complete build call
            including the Python executable.
        """
        options, options_after_end = preset.get_preset_options(
            file_names=preset_file_names,
            preset_name=self.invocation.args.preset_name,
            run_mode=RunMode(self.invocation.args.preset_run_mode)
        )

        build_call = [sys.argv[0]]

        build_call.append(self.invocation.args.preset_run_mode)

        if self.invocation.args.dry_run:
            build_call.append("--dry-run")
        build_call.extend(["--jobs", str(self.invocation.args.jobs)])
        if self.invocation.args.clean:
            build_call.append("--clean")
        if self.invocation.args.verbose:
            build_call.append("--verbose")
        build_call.extend(["--repository", self.invocation.args.repository])

        for key, value in options.items():
            if value:
                build_call.append("--{}={}".format(key, value))
            else:
                build_call.append("--{}".format(key))

        # TODO build_call.append("--")

        for key, value in options_after_end.items():
            if value:
                build_call.append("--{}={}".format(key, value))
            else:
                build_call.append("--{}".format(key))

        return build_call
