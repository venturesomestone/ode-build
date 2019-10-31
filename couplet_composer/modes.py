# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem project.
#
# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License
#
# ------------------------------------------------------------- #


"""
This support module contains the functions for running the
different modes of the script.
"""

import logging
import os
import sys

from .support.file_paths import get_preset_file_path

from .support.project_names import get_ode_repository_name, get_project_name

from .util import shell

from .preset_mode import \
    compose_preset_call, print_script_invocation, show_presets


def run_in_preset_mode(arguments, source_root):
    """
    Runs the script in the preset mode. This function isn't pure
    as the functions called by it may modify the file system and
    run other scripts.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    logging.debug("Running %s in preset mode", get_project_name())

    preset_file_names = [os.path.join(
        source_root,
        get_ode_repository_name(),
        get_preset_file_path()
    )]

    logging.debug("The preset files are %s", ", ".join(preset_file_names))

    if arguments.show_presets:
        return show_presets(file_names=preset_file_names)

    if not arguments.preset:
        logging.critical("Missing the '--preset' option")

    build_call = compose_preset_call(
        arguments=arguments,
        file_names=preset_file_names
    )

    print_script_invocation(
        build_call=build_call,
        preset_name=arguments.preset,
        executable=sys.executable
    )

    if arguments.expand_script_invocation:
        logging.debug("The build script invocation is printed")
        return 0

    command_to_run = [sys.executable] + build_call

    shell.caffeinate(command_to_run, dry_run=False, echo=True)


def run_in_configuring_mode(arguments, source_root):
    """
    Runs the script in configuration mode and sets up the
    development and build environment. This function isn't pure
    as the functions called by it may modify the file system and
    run other scripts.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    # set_up.set_up()
    # clone.clone_dependencies()
    # TODO Write the JSON file for toolchain here.


def run_in_composing_mode(arguments, source_root):
    """
    Runs the script in build mode. This function isn't pure as
    the functions called by it may modify the file system and run
    other scripts.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
