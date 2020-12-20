# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents the project
that the build script acts on.
"""

import importlib
import json
import logging
import os

from typing import Any

from .support import environment

from .dependency import Dependency


class Project:
    """A class that that represents the project that the build
    script acts on.

    Attributes:
        ode_version (str): The version number of Obliging Ode.
        anthem_version (str): The version number of Unsung
            Anthem.
        dependencies (dict): A dictionary containing the names
            and representation objects of the dependencies of the
            project.
    """

    SHARED_VERSION_KEY = "shared_version"
    SHARED_USAGE_VALUE = "shared"
    VERSION_KEY = "version"
    ODE_KEY = "ode"
    ANTHEM_KEY = "anthem"
    DEPENDENCIES_KEY = "dependencies"
    MODULE_KEY = "module"
    MODULE_DEFAULT_VALUE = "default"
    CLASS_KEY = "class_name"
    LIBRARY_FILE_KEY = "libraryFile"
    TEST_ONLY_KEY = "testOnly"
    BENCHMARK_ONLY_KEY = "benchmarkOnly"

    def __init__(
        self,
        source_root: str,
        repo: str,
        script_package: str
    ) -> None:
        """Initializes the project object.

        Arguments:
            source_root (str): The root directory of the
                invocation in which the project and the build
                files are.
            repo (str): The name of the repository directory of
                the project that is being built.
            script_package (str): The name of the root Python
                package of the build script.
        """
        if not environment.is_path_source_root(path=source_root, repo=repo):
            logging.critical(
                "The root directory for the build script invocation is "
                "invalid: %s",
                source_root
            )
            raise ValueError

        project_json = os.path.join(source_root, repo, "util", "project.json")
        dependency_data = None

        try:
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

                dependency_data = self._get_from_project_data(
                    data=json_data,
                    key=self.DEPENDENCIES_KEY
                )

        except Exception:
            logging.critical(
                "The project value file wasn't found: %s",
                project_json
            )
            raise ValueError

        if not dependency_data:
            raise ValueError

        self.dependencies = dict()

        for key, value in dependency_data:
            self.dependencies[key] = self._create_dependency_object(
                key=key,
                data=value,
                root_package=script_package
            )

    def _get_from_project_data(self, data: object, key: str) -> Any:
        """Reads and resolves the given entry from the data got
        from the project data JSON file.

        Args:
            data (Object): The data object read from the project
                data JSON file.
            key (str): The key for the data.

        Returns:
            The number, string, or object read from the project
            data JSON file.
        """
        if key not in data:
            raise ValueError

        return data[key]

    def _get_version_from_project_data(self, data: object, key: str) -> str:
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
        elif key_data[self.VERSION_KEY] == self.SHARED_USAGE_VALUE:
            return shared
        else:
            return key_data[self.VERSION_KEY]

    def _create_dependency_object(self, key: str, data: dict, root_package: str) -> Dependency:
        """Creates the representation object of the given
        dependency by resolving the correct module and class to
        use.

        Args:
            key (str): The simple identifier of the dependency.
            data (dict): The dependency data for the given key
                read from the project data file.
            root_package (str): The name of the root Python
                package of the build script.

        Returns:
            The constructed dependency object.
        """
        library_file = None if self.LIBRARY_FILE_KEY not in data \
            else data[self.LIBRARY_FILE_KEY]

        test_only = False

        if self.TEST_ONLY_KEY in data:
            test_only = data[self.TEST_ONLY_KEY]

        benchmark_only = False

        if self.BENCHMARK_ONLY_KEY in data:
            benchmark_only = data[self.BENCHMARK_ONLY_KEY]

        if self.MODULE_KEY not in data or \
                data[self.MODULE_KEY] == self.MODULE_DEFAULT_VALUE:
            return Dependency(
                key=key,
                name=data["name"],
                version=data["version"],
                library_file=library_file,
                test_only=test_only,
                benchmark_only=benchmark_only
            )
        else:
            if self.CLASS_KEY not in data:
                raise ValueError  # TODO Add explanation or logging.

            package_name = "{}.support.dependencies.{}".format(
                root_package,
                data[self.MODULE_KEY]
            )
            module = importlib.import_module(package_name)
            dependency_class = getattr(module, self.CLASS_KEY)

            return dependency_class(
                key=key,
                name=data["name"],
                version=data["version"],
                library_file=library_file,
                test_only=test_only,
                benchmark_only=benchmark_only
            )
