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

from functools import partial

from .support.environment import get_build_root, get_project_root

from .support.file_paths import \
    get_preset_file_path, get_project_dependencies_file_path

from .support.project_names import get_ode_repository_name, get_project_name

from .support import tool_data

from .util.target import parse_target_from_argument_string

from .util import shell

from .composing_mode import \
    compose_project, create_composing_root, create_destination_root

from .configuring_mode import \
    create_build_root, create_dependencies_root, create_tools_root

from .dependency_set import construct_dependencies_data, install_dependencies

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


def _construct_tool_data_construction_info(arguments):
    """
    Constructs the dictionary containing the required information
    for creating the ToolData object for the toolchain.

    arguments -- The namespace containing the parsed command line
    arguments of the script.
    """
    return {
        "clang": partial(
            tool_data.create_clang_tool_data,
            version=arguments.compiler_version
        ),
        "clang++": partial(
            tool_data.create_clangxx_tool_data,
            version=arguments.compiler_version
        ),
        "gcc": partial(
            tool_data.create_gcc_tool_data,
            version=arguments.compiler_version
        ),
        "g++": partial(
            tool_data.create_gxx_tool_data,
            version=arguments.compiler_version
        ),
        "cmake": tool_data.create_cmake_tool_data,
        "ninja": tool_data.create_ninja_tool_data,
        "make": tool_data.create_make_tool_data,
        "git": tool_data.create_git_tool_data
    }


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
    build_target = parse_target_from_argument_string(arguments.host_target)

    # Check the directories.
    # build_root = create_build_root(source_root=source_root)
    tools_root = create_tools_root(
        source_root=source_root,
        target=build_target
    )

    logging.debug("Creating the toolchain for the run")

    # TODO Allow reading the user agent from some file on the
    # system
    github_user_agent = arguments.github_user_agent

    # TODO Allow reading the API token from some file on the
    # system
    github_api_token = arguments.github_api_token

    toolchain = create_toolchain(
        tools_data=construct_tools_data(
            _construct_tool_data_construction_info(arguments=arguments)
        ),
        compiler_toolchain=arguments.compiler_toolchain,
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=platform.system(),
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        tools_root=tools_root,
        build_root=get_build_root(source_root=source_root),
        read_only=False,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    logging.debug("The created toolchain is %s", toolchain)

    logging.debug("Starting to install the dependencies of the project")

    dependencies_root = create_dependencies_root(
        source_root=source_root,
        target=build_target
    )

    install_dependencies(
        dependencies_data=construct_dependencies_data(
            data_file=os.path.join(
                source_root,
                "unsung-anthem",
                get_project_dependencies_file_path()
            )
        ),
        toolchain=toolchain,
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=platform.system(),
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        opengl_version=arguments.opengl_version,
        dependencies_root=dependencies_root,
        build_root=get_build_root(source_root=source_root),
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )


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
    build_target = parse_target_from_argument_string(arguments.host_target)

    # Check the directories.
    # build_root = create_build_root(source_root=source_root)
    tools_root = create_tools_root(
        source_root=source_root,
        target=build_target
    )

    logging.debug("Creating the toolchain for the run")

    # TODO Allow reading the user agent from some file on the
    # system
    github_user_agent = arguments.github_user_agent

    # TODO Allow reading the API token from some file on the
    # system
    github_api_token = arguments.github_api_token

    toolchain = create_toolchain(
        tools_data=construct_tools_data(
            _construct_tool_data_construction_info(arguments=arguments)
        ),
        compiler_toolchain=arguments.compiler_toolchain,
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=platform.system(),
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        tools_root=tools_root,
        build_root=get_build_root(source_root=source_root),
        read_only=True,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    logging.debug("The created toolchain is %s", toolchain)

    compose_project(
        toolchain=toolchain,
        arguments=arguments,
        project_root=get_project_root(source_root=source_root),
        build_root=get_build_root(source_root=source_root),
        composing_root=create_composing_root(
            source_root=source_root,
            target=build_target
        ),
        destination_root=create_destination_root(
            source_root=source_root,
            target=build_target
        ),
        dependencies_root=create_dependencies_root(
            source_root=source_root,
            target=build_target
        )
    )
