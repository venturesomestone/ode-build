# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
configuring run mode of the build script.
"""

import json
import logging

from .util import shell

from .runner_proper import RunnerProper


class ConfiguringRunner(RunnerProper):
    """A class for creating callable objects that represent the
    configuring mode runners of the build script.
    """

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        super().__call__()

        version_data = self.build_dir.installed_versions \
            if self.build_dir.installed_versions else dict()

        for dependency in self.project.dependencies:
            if dependency.should_install(
                runner=self,
                build_dir=self.build_dir
            ):
                logging.info(
                    "Going to install %s version %s",
                    dependency.name,
                    dependency.version
                )
                dependency.install(runner=self, build_dir=self.build_dir)

                version_data.update({dependency.key: dependency.version})

                with open(self.build_dir.versions_file, "w") as json_file:
                    json.dump(version_data, json_file)

                logging.info(
                    "Installed version %s of %s",
                    dependency.version,
                    dependency.name
                )

        return 0

    def clean(self) -> None:
        """Cleans the directories and files of the runner before
        building when clean build is run.
        """
        super().clean()

        shell.rmtree(
            self.build_dir.dependencies,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.rmtree(
            self.build_dir.tools,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
        shell.rm(
            self.build_dir.versions_file,
            dry_run=self.args.dry_run,
            echo=self.args.verbose
        )
