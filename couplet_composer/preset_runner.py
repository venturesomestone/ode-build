# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
preset run mode of the build script.
"""

import logging
import os
import platform
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
            self.source_root,
            self.args.repository,
            environment.PRESET_FILE_PATH
        )]

        # TODO Include the preset files from the command line
        # arguments
        logging.debug("The preset files are %s", ", ".join(preset_file_names))

        if self.args.show_presets:
            return self._show_presets(file_names=preset_file_names)

        if not self.args.preset_name:
            logging.critical("Missing the '--name' option")

        build_call = self._compose_call(preset_file_names=preset_file_names)

        logging.info(
            "Using preset '%s', which expands to \n\n%s\n",
            self.args.preset_name,
            shell.quote_command(build_call)
        )

        logging.debug(
            "The script will use '%s' as the Python executable\n",
            sys.executable
        )

        if self.args.expand_script_invocation:
            logging.debug("The build script invocation is printed")
            return 0

        self.caffeinate(command=build_call, echo=True)

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
            preset_name=self.args.preset_name,
            run_mode=RunMode(self.args.preset_run_mode)
        )

        build_call = [sys.argv[0]]

        build_call.append(self.args.preset_run_mode)

        if self.args.dry_run:
            build_call.append("--dry-run")
        build_call.extend(["--jobs", str(self.args.jobs)])
        if self.args.clean:
            build_call.append("--clean")
        if self.args.verbose:
            build_call.append("--verbose")
        build_call.extend(["--repository", self.args.repository])

        for key, value in options.items():
            if value:
                if isinstance(value, list):
                    for entry in value:
                        build_call.append("--{}={}".format(key, entry))
                else:
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

    def clean(self) -> None:
        """Cleans the directories and files of the runner before
        building when clean build is run.
        """
        pass

    def caffeinate(
        self,
        command: list,
        env: dict = None,
        dry_run: bool = None,
        echo: bool = None
    ) -> None:
        """Runs a command during which system sleep is disabled.

        Args:
            command (list): The command to call.
            env (dict): Key-value pairs as the environment
                variables.
            dry_run (bool): Whether or not dry run is enabled.
            echo (bool): Whether or not the command must be
                printed.
        """
        command_to_run = list(command)
        # Disable system sleep, if possible.
        if platform.system() == "Darwin":
            command_to_run = ["caffeinate"] + list(command)
        shell.call(command_to_run, env=env, dry_run=dry_run, echo=echo)
