# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions for running the
different modes of the script.
"""

from __future__ import print_function

import logging
import os
import platform
import sys
import time

from .support.cmake_generators import \
    get_make_cmake_generator_name, get_ninja_cmake_generator_name, \
    get_visual_studio_16_cmake_generator_name

from .support.compiler_toolchains import \
    get_clang_toolchain_name, get_gcc_toolchain_name, get_msvc_toolchain_name

from .support.environment import \
    get_build_root, get_composing_directory, get_dependencies_directory, \
    get_dependency_version_data_file, get_destination_directory, \
    get_project_root, get_tools_directory

from .support.file_paths import \
    get_preset_file_path, get_project_dependencies_file_path

from .support.mode_names import get_configuring_mode_name

from .support.project_names import get_ode_repository_name, get_project_name

from .support.tool_data import \
    create_clang_apply_replacements_tool_data, create_clang_tidy_tool_data, \
    create_clang_tool_data, create_cmake_tool_data, create_doxygen_tool_data, \
    create_gcc_tool_data, create_git_tool_data, create_make_tool_data, \
    create_msbuild_tool_data, create_msvc_tool_data, create_ninja_tool_data, \
    create_xvfb_tool_data

from .util.target import current_platform, parse_target_from_argument_string

from .util import shell

from .composing_mode import \
    compose_project, create_artefacts, create_composing_root, \
    create_destination_root, install_running_copies

from .configuring_mode import create_dependencies_root, create_tools_root

from .dependency_set import construct_dependencies_data, install_dependencies

from .preset_mode import \
    compose_preset_call, print_script_invocation, show_presets

from .toolchain import create_toolchain


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

    if arguments.in_tree_build:
        preset_file_names = [os.path.join(source_root, get_preset_file_path())]
    else:
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

    shell.caffeinate(build_call, dry_run=False, echo=True)

    return 0


def _clean(arguments, source_root):
    """
    Cleans the directories and files before building when clean
    build is invoked.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    # Two spaces are required at the end of the first line as the
    # counter uses backspace characters.
    sys.stdout.write("\033[31mStarting a clean build in  \033[0m")
    for i in reversed(range(0, 4)):
        sys.stdout.write("\033[31m\b{!s}\033[0m".format(i))
        sys.stdout.flush()
        time.sleep(1)
    print("\033[31m\b\b\b\bnow.\033[0m")

    build_target = parse_target_from_argument_string(arguments.host_target)
    build_root = get_build_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build
    )
    composing_root = get_composing_directory(
        build_root=build_root,
        target=build_target,
        cmake_generator=arguments.cmake_generator,
        build_variant=arguments.build_variant
    )
    destination_root = get_destination_directory(
        build_root=build_root,
        target=build_target,
        cmake_generator=arguments.cmake_generator,
        build_variant=arguments.build_variant,
        version=arguments.anthem_version
    )
    tools_root = get_tools_directory(
        build_root=build_root,
        target=build_target
    )
    dependencies_root = get_dependencies_directory(
        build_root=build_root,
        target=build_target,
        build_variant=arguments.build_variant
    )
    version_data_file = get_dependency_version_data_file(
            build_root=build_root,
            target=build_target,
            build_variant=arguments.build_variant
        )

    if arguments.composer_mode == get_configuring_mode_name():
        shell.rmtree(
            tools_root,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        shell.rmtree(
            dependencies_root,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        shell.rm(
            version_data_file,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
    shell.rmtree(
        composing_root,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.rmtree(
        destination_root,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )


def _get_github_api_access_values(
    source_root,
    value_file,
    user_agent,
    api_token
):
    """
    Resolves the user agent and API token to be used to access
    the version 4 of the GitHub API, if they can be resolved.
    Returns two values, the first of which is the user agent to
    be used and the second the API token.

    source_root -- Path to the directory that is the root of the
    script run.

    value_file -- The pat from arguments to the file from which
    the user agent and API token can be read.

    user_agent -- The user agent given through command line
    arguments that is used when accessing the GitHub API.

    api_token -- The GitHub API token given through command line
    arguments that is used to access the API.
    """
    repository_root = os.path.join(source_root, get_ode_repository_name())
    value_file_path = os.path.join(repository_root, value_file)
    api_file_content = []

    if value_file and os.path.exists(value_file_path):
        logging.debug(
            "Found a file containing the user agent and authorization token "
            "for GitHub API from %s",
            value_file_path
        )
        with open(value_file_path) as api_file:
            api_file_content = [line.strip() for line in api_file.readlines()]
    elif not os.path.exists(value_file_path):
        logging.debug(
            "The file containing the user agent and authorization token for "
            "GitHub API wasn't found from %s",
            value_file_path
        )

    return_user_agent = None
    return_api_token = None

    if api_file_content:
        logging.debug("Adding the user agent and the API token from the file")
        return_user_agent = api_file_content[0]
        return_api_token = api_file_content[1]

    if user_agent:
        logging.debug("Adding the user agent from command line")
        return_user_agent = user_agent

    if api_token:
        logging.debug("Adding the API token from command line")
        return_api_token = api_token

    if return_user_agent and return_api_token:
        logging.info(
            "Using the GraphQL API of GitHub as user agent and access token "
            "are given"
        )
    else:
        logging.info(
            "Using the REST API of GitHub as user agent and access token "
            "aren't given"
        )

    return return_user_agent, return_api_token


def _construct_tool_data(arguments, host_system):
    """
    Constructs a dictionary containing the required ToolData
    objects for the toolchain for the current host system.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    host_system -- The system this script is run on.
    """
    def _create_compiler_data(arguments):
        """
        Returns the tool data or tool data pair representing the
        compiler for the script.

        arguments -- The namespace containing the parsed command
        line arguments of the script.
        """
        def _should_use_separate_compilers(arguments):
            """
            Returns whether or not the script should use separate
            C and C++ compilers in the current configuration.

            arguments -- The namespace containing the parsed
            command line arguments of the script.
            """
            if arguments.host_compiler:
                logging.debug(
                    "Going to use single compiler tool as only one is given "
                    "in command line options"
                )
                return False
            elif arguments.compiler_toolchain == get_msvc_toolchain_name():
                logging.debug(
                    "Going to use single compiler tool as the selected "
                    "compiler is MSVC"
                )
                return False
            logging.debug("Going to use separate C and C++ compilers")
            return True

        if _should_use_separate_compilers(arguments=arguments):
            if arguments.host_cc and arguments.host_cxx:
                if "clang" in arguments.host_cc:
                    return create_clang_tool_data(
                        cc_path=arguments.host_cc,
                        cxx_path=arguments.host_cxx
                    )
                elif "gcc" in arguments.host_cc:
                    return create_gcc_tool_data(
                        cc_path=arguments.host_cc,
                        cxx_path=arguments.host_cxx
                    )
                else:
                    return None
            else:
                if arguments.compiler_toolchain == get_clang_toolchain_name():
                    return create_clang_tool_data(
                        version=arguments.compiler_version
                    )
                elif arguments.compiler_toolchain == get_gcc_toolchain_name():
                    return create_gcc_tool_data(
                        version=arguments.compiler_version
                    )
                else:
                    return None
        else:
            if arguments.host_compiler:
                if "msvc" in arguments.host_compiler.lower() \
                        or "cl.exe" in arguments.host_compiler.lower():
                    return create_msvc_tool_data(
                        tool_path=arguments.host_compiler
                    )
            else:
                if arguments.compiler_toolchain == get_msvc_toolchain_name():
                    return create_msvc_tool_data()
                else:
                    return None

    def _create_build_system_data(arguments):
        """
        Returns the tool data representing the build system for
        the script.

        arguments -- The namespace containing the parsed command
        line arguments of the script.
        """
        generator = arguments.cmake_generator
        if generator == get_ninja_cmake_generator_name():
            return create_ninja_tool_data()
        elif generator == get_make_cmake_generator_name():
            return create_make_tool_data()
        elif generator == get_visual_studio_16_cmake_generator_name():
            if arguments.host_msbuild:
                return create_msbuild_tool_data(
                    tool_path=arguments.host_msbuild
                )
            else:
                return create_msbuild_tool_data()

    return {
        "compiler": _create_compiler_data(arguments=arguments),
        "cmake": create_cmake_tool_data(),
        "build_system": _create_build_system_data(arguments=arguments),
        "scm": create_git_tool_data(),
        "make": create_make_tool_data(),
        "doxygen": create_doxygen_tool_data(),
        "linter": create_clang_tidy_tool_data(
            linter_required=arguments.lint,
            tool_path=arguments.clang_tidy_binary
        ),
        "linter_replacements": create_clang_apply_replacements_tool_data(
            linter_required=arguments.lint,
            tool_path=arguments.clang_apply_replacements_binary
        ),
        "xvfb": create_xvfb_tool_data()
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
    if arguments.clean:
        _clean(arguments=arguments, source_root=source_root)

    build_target = parse_target_from_argument_string(arguments.host_target)

    # Check the directories.
    # build_root = create_build_root(source_root=source_root)
    tools_root = create_tools_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build,
        target=build_target
    )

    logging.debug("Creating the toolchain for the run")

    github_user_agent, github_api_token = _get_github_api_access_values(
        source_root=source_root,
        value_file=arguments.github_auth_file,
        user_agent=arguments.github_user_agent,
        api_token=arguments.github_api_token
    )

    toolchain = create_toolchain(
        tools_data=_construct_tool_data(
            arguments=arguments,
            host_system=current_platform()
        ),
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=current_platform(),
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        tools_root=tools_root,
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        read_only=False,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    logging.debug("The created toolchain is %s", toolchain)

    logging.debug("Starting to install the dependencies of the project")

    dependencies_root = create_dependencies_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build,
        target=build_target,
        build_variant=arguments.build_variant
    )

    install_dependencies(
        dependencies_data=construct_dependencies_data(
            data_file=os.path.join(
                get_project_root(
                    source_root=source_root,
                    in_tree_build=arguments.in_tree_build
                ),
                get_project_dependencies_file_path()
            )
        ),
        toolchain=toolchain,
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=current_platform(),
        build_variant=arguments.build_variant,
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        opengl_version=arguments.opengl_version,
        dependencies_root=dependencies_root,
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        version_data_file=get_dependency_version_data_file(
            build_root=get_build_root(
                source_root=source_root,
                in_tree_build=arguments.in_tree_build
            ),
            target=build_target,
            build_variant=arguments.build_variant
        ),
        build_test=arguments.build_test,
        build_benchmark=arguments.build_benchmark,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    return 0


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
    if arguments.clean:
        _clean(arguments=arguments, source_root=source_root)

    build_target = parse_target_from_argument_string(arguments.host_target)

    # Check the directories.
    # build_root = create_build_root(source_root=source_root)
    tools_root = get_tools_directory(
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        target=build_target
    )

    logging.debug("Creating the toolchain for the run")

    github_user_agent, github_api_token = _get_github_api_access_values(
        source_root=source_root,
        value_file=arguments.github_auth_file,
        user_agent=arguments.github_user_agent,
        api_token=arguments.github_api_token
    )

    toolchain = create_toolchain(
        tools_data=_construct_tool_data(
            arguments=arguments,
            host_system=current_platform()
        ),
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=current_platform(),
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        tools_root=tools_root,
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        read_only=True,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    logging.debug("The created toolchain is %s", toolchain)

    compose_project(
        source_root=source_root,
        toolchain=toolchain,
        arguments=arguments,
        host_system=current_platform(),
        project_root=get_project_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        composing_root=create_composing_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build,
            target=build_target,
            cmake_generator=arguments.cmake_generator,
            build_variant=arguments.build_variant
        ),
        destination_root=create_destination_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build,
            target=build_target,
            cmake_generator=arguments.cmake_generator,
            build_variant=arguments.build_variant,
            version=arguments.anthem_version
        ),
        dependencies_root=create_dependencies_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build,
            target=build_target,
            build_variant=arguments.build_variant
        )
    )

    if arguments.skip_build:
        return 0

    install_running_copies(
        arguments=arguments,
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        destination_root=get_destination_directory(
            build_root=get_build_root(
                source_root=source_root,
                in_tree_build=arguments.in_tree_build
            ),
            target=build_target,
            cmake_generator=arguments.cmake_generator,
            build_variant=arguments.build_variant,
            version=arguments.anthem_version
        )
    )

    create_artefacts(
        arguments=arguments,
        host_system=current_platform(),
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        )
    )

    return 0
