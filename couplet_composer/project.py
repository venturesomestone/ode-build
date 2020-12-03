# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the project
that the build script acts on.
"""

import json
import logging
import os

from .support import environment


class Project:
    """A class that that represents the project that the build
    script acts on.

    Attributes:
        ode_version (str): The version number of Obliging Ode.
        anthem_version (str): The version number of Unsung
            Anthem.
    """

    SHARED_VERSION_KEY = "shared_version"
    SHARED_USAGE_KEY = "shared"
    VERSION_KEY = "version"
    ODE_KEY = "ode"
    ANTHEM_KEY = "ode"

    def __init__(self, source_root, repo):
        """Initializes the project object.

        Arguments:
            source_root (str): The root directory of the
                invocation in which the project and the build
                files are.
            repo (str): The name of the repository directory of
                the project that is being built.
        """
        if not environment.is_path_source_root(path=source_root, repo=repo):
            logging.critical(
                "The root directory for the build script invocation is "
                "invalid: %s",
                source_root
            )
            raise ValueError

        project_json = os.path.join(source_root, repo, "util", "project.json")

        with open(project_json) as f:
            json_data = json.load(f)

            self.ode_version = self._get_version_from_project_data(
                data=json_data,
                key=self.ODE_KEY
            )
            self.anthem_version = self._get_version_from_project_data(
                data=json_data,
                key=self.ANTHEM_KEY
            )

    def _get_version_from_project_data(self, data, key):
        """Reads and resolves the correct version from the data
        got from the project data JSON file.

        Args:
            data (Object): The data object read from the project
                data JSON file.
            key (str): The key for the project part that the
                version is resolved for.

        Returns:
            A 'str' that contains the resolved version number.
        """
        shared = None if self.SHARED_VERSION_KEY not in data \
            else data[self.SHARED_VERSION_KEY]

        if key not in data:
            raise ValueError

        key_data = data[key]

        if self.VERSION_KEY not in key_data:
            if shared:
                return shared
            else:
                raise ValueError
        elif key_data[self.VERSION_KEY] == self.SHARED_USAGE_KEY:
            return shared
        else:
            return key_data[self.VERSION_KEY]
