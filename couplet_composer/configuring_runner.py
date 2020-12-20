# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
configuring run mode of the build script.
"""

from .util import shell

from .runner import Runner


class ConfiguringRunner(Runner):
    """A class for creating callable objects that represent the
    configuring mode runners of the build script.
    """

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        super().__call__()

        return 0

    def clean(self) -> None:
        """Cleans the directories and files of the runner before
        building when clean build is run.
        """
        super().clean()

        shell.rmtree(
            self.build_dir.dependencies,
            dry_run=self.invocation.args.dry_run,
            echo=self.invocation.args.verbose
        )
        shell.rm(
            self.build_dir.versions_file,
            dry_run=self.invocation.args.dry_run,
            echo=self.invocation.args.verbose
        )
