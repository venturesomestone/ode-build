# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents a target
platform for the build.
"""


class Target:
    """A class for creating objects that represent the build
    target platforms of the invocations of the build script.

    Attributes:
        system (str): The name of the target operating system.
        machine (str): The name of the target machine type.
    """

    def __init__(self, system, machine):
        """Initializes a target platform object.

        Args:
            system (str): The name of the target operating
                system.
            machine (str): The name of the target machine type.
        """
        # TODO Check whether the values are valid
        self.system = system
        self.machine = machine

    @classmethod
    def to_target(cls, target):
        """Parses a target object from the given string
        representation of a build target platform.

        Args:
            target (str): The string representation of a build
                target platform.

        Returns:
            An object of the type Target.
        """
        return Target(system=target.split("-")[0], machine=target.split("-")[1])
