# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class that represents a target
platform for the build.
"""

import platform

from .support.system import System


class Target:
    """A class for creating objects that represent the build
    target platforms of the invocations of the build script.

    Attributes:
        system (System): The name of the target operating system.
        machine (str): The name of the target machine type.
    """

    LINUX_MACHINES = [
        "x86_64",
        "armv6",
        "armv7",
        "aarch64",
        "powerpc64",
        "powerpc64le",
        "s390x"
    ]
    WINDOWS_MACHINES = ["x86_64", "AMD64"]
    DARWIN_MACHINES = ["x86_64"]

    def __init__(self, system: str, machine: str) -> None:
        """Initializes a target platform object.

        Args:
            system (str): The name of the target operating
                system.
            machine (str): The name of the target machine type.
        """
        self.system = System(system.lower())

        if self.is_machine_valid(system=self.system, machine=machine):
            self.machine = machine
        else:
            raise ValueError

    def __repr__(self) -> str:
        """Computes the string representation of the target.

        The value returned by this function can be turned back to
        a target object with the 'to_target' method.

        Returns:
            A string representation of the target.
        """
        return "{}-{}".format(self.system.value, self.machine)

    @classmethod
    def resolve_host_target(cls):
        """Resolves the build platform that the build script is
        run on.

        Returns:
            An object of the type Target that represents the
            current build target platform.
        """
        try:
            return Target(system=platform.system(), machine=platform.machine())
        except ValueError:
            raise NotImplementedError(
                "The combination of '{}' as the operation system and '{}' as "
                "the machine architecture isn't supported".format(
                    platform.system(),
                    platform.machine()
                )
            )

    @classmethod
    def to_target(cls, target: str):
        """Parses a target object from the given string
        representation of a build target platform.

        Args:
            target (str): The string representation of a build
                target platform.

        Returns:
            An object of the type Target.
        """
        return Target(system=target.split("-")[0], machine=target.split("-")[1])

    @classmethod
    def is_machine_valid(cls, system: System, machine: str) -> bool:
        """Checks whether or not the given machine type is valid
        for the given operating system.

        Args:
            system (System): The operating system.
            machine (str): The name of the target machine type.

        Returns:
            A value of the type Boolean telling whether the
            machine was valid.
        """
        if system is System.linux:
            return machine in cls.LINUX_MACHINES
        elif system is System.windows:
            return machine in cls.WINDOWS_MACHINES
        elif system is System.darwin:
            return machine in cls.DARWIN_MACHINES
        else:
            return False
