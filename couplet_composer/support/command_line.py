# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains the desciption and the epilogue of the
build script for command line.
"""

import textwrap


__all__ = ["DESCRIPTION", "EPILOG"]


def _get_description() -> str:
    """Gives the brief command line description of the build
    script.

    Returns:
        An 'str' containing the command line description.
    """

    raw_description = "Use this tool to build, test, and prepare binary "
    "distribution archives of {ode} and {anthem}.  This tool contains "
    "configuration mode that is used prepare the build environment and "
    "composing mode that builds the project."

    return textwrap.fill(
        text=raw_description.format(ode="Obliging Ode", anthem="Unsung Anthem"),
        width=80
    )


def _get_epilog() -> str:
    """Gives the command line epilogue of the build script.

    Returns:
        An 'str' containing the epilogue for the command line.
    """

    raw_epilog = """
Using option presets:

  preset                use the option preset mode by specifying this argument

  --file=PATH           load presets from the specified file

  --name=NAME         use the specified option preset

  You cannot use the preset mode with other options.  It is not possible to add
  ad hoc customizations to a preset.  If you want to customize a preset, you
  need to create a new preset.


Environment
-----------

Couplet Composer expects the sources to be laid out in the following way:

    $root/unsung-anthem (source code of {ode} and {anthem})
         /build          (created automatically)
         /script         (created automatically)

The directory '$root/script' is created only if the script is run by using the
utility scripts in the repository of {ode} and {anthem}, which is the
recommended way.

Preparing to run this script
----------------------------

Make sure that your system has C and C++ compilers and Git.

That's it; you're ready to go!

Configuring mode
----------------

Before you can build the project by using so called composing mode, you need to
set up the build environment by using configuring mode of the script.  The you
can invoke configuring mode with the following command:

  [~/src/s]$ ./unsung-anthem/util/configure

You must run the configuring mode only once per one set of command line
options.  After that you can build the project without building the
dependencies every time.

Examples
--------

Given the above layout of sources, the simplest invocation of Couplet Composer
is just:

  [~/src/s]$ ./unsung-anthem/util/configure
  [~/src/s]$ ./unsung-anthem/util/compose

This builds {ode} and {anthem} in debug mode.  All builds are
incremental.  To incrementally build changed files, repeat the same command.

Typical uses of Couplet Composer
--------------------------------

To build everything with optimization without debug information:

  [~/src/s]$ ./unsung-anthem/util/compose -R

To run tests, add '-t':

  [~/src/s]$ ./unsung-anthem/util/compose -R -t

To build the libraries of the project to write add-ons:

  [~/src/s]$ ./unsung-anthem/util/compose --build-libs

To use 'make' instead of 'ninja', use '-m':

  [~/src/s]$ ./unsung-anthem/util/compose -m

Preset mode in Couplet Composer
-------------------------------

All automated environments use Couplet Composer in preset mode.  In preset
mode, the command line only specifies the preset name.  The actual options come
from the selected preset in 'util/composer-presets.ini'.

If you have your own favourite set of options, you can create your own, local,
preset.  For example, let's create a preset called 'release':

  $ cat > ~/.ode-build-presets
  [release]
  release
  test

To use it, invoke the script with the 'preset' command and specify the preset
to expand with the '--name=' argument:

  [~/src/s]$ ./unsung-anthem/util/configure preset --name=release
  Using preset 'release', which expands to

  composer --release --test --
  ...

You can find the existing presets in 'utils/build-presets.ini'

Philosophy
----------

While one can invoke CMake directly to build {anthem}, this tool will save
one's time by taking away the mechanical parts of the process, providing one
the controls for the important options.

For all automated build environments, this tool is regarded as the only way to
build {anthem}.  This is not a technical limitation of the {anthem}
build system.  It is a policy decision aimed at making the builds uniform
across all environments and easily reproducible by engineers who are not
familiar with the details of the setups of other systems or automated
environments.
    """

    return raw_epilog.format(ode="Obliging Ode", anthem="Unsung Anthem")


DESCRIPTION = _get_description()

EPILOG = _get_epilog()
