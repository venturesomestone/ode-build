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

            shared_version = None \
                if self.SHARED_VERSION_KEY not in json_data \
                else json_data[self.SHARED_VERSION_KEY]

            if self.ODE_KEY not in json_data:
                raise ValueError

            ode_data = json_data[self.ODE_KEY]

            if self.VERSION_KEY not in ode_data:
                if shared_version:
                    self.ode_version = shared_version
                else:
                    raise ValueError
            elif ode_data[self.VERSION_KEY] == self.SHARED_USAGE_KEY:
                self.ode_version = shared_version
            else:
                self.ode_version = ode_data[self.VERSION_KEY]

            if self.ANTHEM_KEY not in json_data:
                raise ValueError

            anthem_data = json_data[self.ANTHEM_KEY]

            if self.VERSION_KEY not in anthem_data:
                if shared_version:
                    self.anthem_version = shared_version
                else:
                    raise ValueError
            elif anthem_data[self.VERSION_KEY] == self.SHARED_USAGE_KEY:
                self.anthem_version = shared_version
            else:
                self.anthem_version = anthem_data[self.VERSION_KEY]
