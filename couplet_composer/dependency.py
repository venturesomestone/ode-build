# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the base class for the objects that
represent the dependencies of the project that this build script
acts on.
"""


class Dependency:
    """A class for creating objects that represent the
    dependencies of the project that this build script acts on.

    Attributes:
        key (str): The simple identifier of this dependency.
        name (str): The full name of this dependency.
        version (str): The required version of the dependency.
    """

    def __init__(self, key: str, name: str, version: str) -> None:
        """Initializes the dependency object.

        Args:
            key (str): The simple identifier of this dependency.
            name (str): The full name of this dependency.
            version (str): The required version of the
                dependency.
        """
        self.key = key
        self.name = name
        self.version = version

    def __repr__(self) -> str:
        """Computes the string representation of the dependency.

        Returns:
            A string representation of the dependency.
        """
        return self.key

    def __str__(self) -> str:
        """Computes the formatted string representation of the dependency.

        Returns:
            A formatted string representation of the dependency.
        """
        return "{} {}".format(self.name, self.version)

    def build(self) -> None:
        """Builds the dependency.
        """
        pass
