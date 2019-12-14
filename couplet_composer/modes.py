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
import platform
import sys

from .support.environment import get_build_root

from .support.file_paths import get_preset_file_path

from .support.project_names import get_ode_repository_name, get_project_name

from .support import tooldata

from .util.target import parse_target_from_argument_string

from .util import shell

from .configuring_mode import create_build_root, create_tools_root

from .preset_mode import \
    compose_preset_call, print_script_invocation, show_presets

from .toolchain import construct_tools_data, create_toolchain


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

    build_target = parse_target_from_argument_string(arguments.host_target)

    # Check the directories.
    # build_root = create_build_root(source_root=source_root)
    tools_root = create_tools_root(
        source_root=source_root,
        target=build_target
    )

    toolchain = create_toolchain(
        tools_data=construct_tools_data({
            "clang": tooldata.create_clang_tool_data,
            "clang++": tooldata.create_clangxx_tool_data,
            "cmake": tooldata.create_cmake_tool_data,
            "ninja": tooldata.create_ninja_tool_data
        }),
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=platform.system(),
        tools_root=tools_root,
        build_root=get_build_root(source_root=source_root),
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    logging.debug("The created toolchain is %s", toolchain)


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
