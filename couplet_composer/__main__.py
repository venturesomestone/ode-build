# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""The entry point of the build script.
"""

import sys

from .invocation import Invocation

from . import __version__


def _main():
    """Starts the script, creates the invocation instance, and
    runs it.

    This function isn't pure as it runs all of the other
    functions in the build script.

    Returns:
        An 'int' that is equal to the exit code of the build
        script.
    """
    invocation = Invocation(
        version=__version__.get_version(),
        name="Couplet Composer",
        project_name="Obliging Ode and Unsung Anthem"
    )

    exit_code = invocation()

    return exit_code


def run():
    """Runs the script when Couplet Composer is invoked.

    This function isn't pure as it runs the main function of the
    build script.

    This function doesn't return anything but exits with the
    function 'sys.exit' with the exit code of the build script.
    """
    sys.exit(_main())


# The script can also be invoked by calling the script itself.
if __name__ == "__main__":
    sys.exit(_main())
