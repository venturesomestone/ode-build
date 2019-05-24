# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""
This support module has build values that are set at the
beginning of the run.
"""

import json
import os
import re

from absl import logging

from couplet_composer.flags import FLAGS

from util import toolchain

from util.mapping import Mapping

from util.target import host_target

from . import defaults

from .defaults import GITHUB_OAUTH_ENV_VARIABLES, SCRIPT_NAME

from .variables import \
    HOME, \
    ODE_BUILD_ROOT, \
    ODE_GRAPHQL_ROOT, \
    ODE_REPO_NAME, \
    ODE_SOURCE_ROOT


__all__ = [
    "ODE",
    "ANTHEM",
    "DEPENDENCIES",
    "CI",
    "HOST_TARGET",
    "CMAKE_GENERATOR",
    "BUILD_VARIANTS",
    "ASSERTIONS",
    "BUILD_SUBDIR",
    "BUILD_DIR",
    "DOWNLOAD_DIR",
    "DOWNLOAD_STATUS_FILE",
    "TOOLCHAIN_STATUS_FILE",
    "TOOLCHAIN",
    "GITHUB_API_V4_ENDPOINT",
    "GITHUB_OAUTH_TOKEN",
    "GITHUB_TAG_QUERY_FILE",
    "GITHUB_REPOSITORY_QUERY_FILE",
    "GITHUB_ASSET_QUERY_FILE",
    "CONNECTION_PROTOCOL",
    "SOURCE_TARGET"
]

# A mapping that contains the build data for Obliging Ode.
ODE = Mapping()

# A mapping that contains the build data for Unsung Anthem.
ANTHEM = Mapping()

# A mapping that contains the build data for the dependencies.
DEPENDENCIES = Mapping()

# Whether or not Composer is run in a CI environment.
CI = "CI" in os.environ and os.environ["CI"]

# The target that represents the host machine and that the
# project is primarily built for.
HOST_TARGET = None

# The program that CMake generates the build files for.
CMAKE_GENERATOR = None

# The dictionary of build variants has the build variant for each
# project propagated from the command line flags.
BUILD_VARIANTS = Mapping()

# The dictionary of assertions has the assertion status for each
# project propagated from the command line flags.
ASSERTIONS = Mapping()

# The build subdirectory is the directory in the build directory
# where the build files are created.
BUILD_SUBDIR = None

# The build directory in the build root is the directory that the
# build files are created in.
BUILD_DIR = os.path.join(ODE_BUILD_ROOT, "build")

# The script directory in the build root is the directory that
# the build script files are copied in.
SCRIPT_DIR = os.path.join(ODE_BUILD_ROOT, "script")

# The download directory in the build root is the directory that
# the dependencies needed to build the project are downloaded to.
DOWNLOAD_DIR = os.path.join(ODE_BUILD_ROOT, "shared")

# The download status file is a JSON file containing the versions
# of the dependencies in order to determine whether to download
# new versions of them.
DOWNLOAD_STATUS_FILE = os.path.join(DOWNLOAD_DIR, "status")

# The build status file is a JSON file containing the versions of
# the built components in order to determine whether to build
# them.
TOOLCHAIN_STATUS_FILE = None

# The toolchain of the build. Please note that some of the
# toolchain's tools may change as they are built by Couplet
# Composer.
TOOLCHAIN = None

# The endpoint of the GitHub GraphQL API.
GITHUB_API_V4_ENDPOINT = "https://api.github.com/graphql"

# The GitHub OAuth token is used to connect to the GitHub GraphQL
# API. If Composer can't set the token, the GitHub REST API is
# used instead.
GITHUB_OAUTH_TOKEN = None

# The GitHub tag query file has the base for the GraphQL queries
# for downloading a tag from GitHub.
GITHUB_TAG_QUERY_FILE = os.path.join(ODE_GRAPHQL_ROOT, "github_tag.graphql")

# The GitHub repository query file has the base for the GraphQL
# queries for downloading a repository from GitHub.
GITHUB_REPOSITORY_QUERY_FILE = os.path.join(
    ODE_GRAPHQL_ROOT,
    "github_repository.graphql"
)

# The GitHub asset query file has the base for the GraphQL
# queries for downloading a release asset from GitHub.
GITHUB_ASSET_QUERY_FILE = os.path.join(
    ODE_GRAPHQL_ROOT,
    "github_asset.graphql"
)

# The connection protocol is the hypertext transfer protocol that
# the script uses.
CONNECTION_PROTOCOL = defaults.PROTOCOL

# The source target is the name of the target of a project when
# it's downloaded as source code.
SOURCE_TARGET = "source"


def set_values():
    """Sets the values."""
    logging.debug("Setting the constant values for the run")

    global HOST_TARGET
    HOST_TARGET = FLAGS["host-target"].value

    # The version number set via a command line flag may have the
    # symbol '[v]' that is replaced by the default version.
    ode_version = FLAGS["ode-version"].value
    if "[v]" in FLAGS["ode-version"].value:
        ode_version = ode_version.replace("[v]", defaults.ODE_VERSION)
    anthem_version = FLAGS["anthem-version"].value
    if "[v]" in FLAGS["anthem-version"].value:
        anthem_version = anthem_version.replace("[v]", defaults.ANTHEM_VERSION)

    # The version number of the project may have environment
    # variables and thus the regular expression finds them and
    # they're replaced by the value of the environment variable.
    env_var = re.compile(r"env\(\w+\)")
    if env_var.search(ode_version):
        for var in env_var.findall(ode_version):
            var_name = var[4:-1]
            ode_version = ode_version.replace(var, os.environ[var_name])
    if env_var.search(anthem_version):
        for var in env_var.findall(anthem_version):
            var_name = var[4:-1]
            anthem_version = anthem_version.replace(var, os.environ[var_name])

    ODE.version = ode_version
    ANTHEM.version = anthem_version

    # Deduce the CMake generator
    if FLAGS["cmake-generator"].value == "ninja":
        cmake_generator = "Ninja"
    elif FLAGS["cmake-generator"].value == "eclipse":
        cmake_generator = "clipse CDT4 - Ninja"
    elif FLAGS["cmake-generator"].value == "make":
        cmake_generator = "Unix Makefiles"
    elif FLAGS["cmake-generator"].value == "xcode":
        cmake_generator = "Xcode"
    elif FLAGS["cmake-generator"].value == "visual-studio-14":
        cmake_generator = "Visual Studio 14 2015"
    elif FLAGS["cmake-generator"].value == "visual-studio-15":
        cmake_generator = "Visual Studio 15 2017"
    else:
        cmake_generator = FLAGS["cmake-generator"].value
    if FLAGS.ninja:
        cmake_generator = "Ninja"
    elif FLAGS.eclipse:
        cmake_generator = "clipse CDT4 - Ninja"
    elif FLAGS.make:
        cmake_generator = "Unix Makefiles"
    elif FLAGS.xcode:
        cmake_generator = "Xcode"
    elif FLAGS["visual-studio-14"].value:
        cmake_generator = "Visual Studio 14 2015"
    elif FLAGS["visual-studio-15"].value:
        cmake_generator = "Visual Studio 15 2017"
    global CMAKE_GENERATOR
    CMAKE_GENERATOR = cmake_generator
    logging.debug("The CMake generator is set to %s", CMAKE_GENERATOR)

    # Deduce and propagate the build variant
    if FLAGS["build-variant"].value == "debug":
        build_variant = "Debug"
    elif FLAGS["build-variant"].value == "release-debuginfo":
        build_variant = "RelWithDebInfo"
    elif FLAGS["build-variant"].value == "release":
        build_variant = "Release"
    else:
        build_variant = FLAGS["build-variant"].value
    if FLAGS.debug:
        build_variant = "Debug"
    elif FLAGS["release-debuginfo"].value:
        build_variant = "RelWithDebInfo"
    elif FLAGS.release:
        build_variant = "Release"
    BUILD_VARIANTS.all = build_variant
    logging.debug("Build variant is %s", BUILD_VARIANTS.all)
    if FLAGS["debug-ode"].value:
        BUILD_VARIANTS.ode = "Debug"
    else:
        BUILD_VARIANTS.ode = build_variant
    logging.debug(
        "The build variant of %s is %s",
        defaults.ODE_NAME,
        BUILD_VARIANTS.ode
    )
    if FLAGS["debug-anthem"].value:
        BUILD_VARIANTS.anthem = "Debug"
    else:
        BUILD_VARIANTS.anthem = build_variant
    logging.debug(
        "The build variant of %s is %s",
        defaults.ANTHEM_NAME,
        BUILD_VARIANTS.anthem
    )
    if FLAGS["debug-sdl"].value:
        BUILD_VARIANTS.sdl = "Debug"
    else:
        BUILD_VARIANTS.sdl = build_variant
    logging.debug(
        "The build variant of %s is %s",
        defaults.SDL_NAME,
        BUILD_VARIANTS.sdl
    )

    # Propagate the assertions
    ASSERTIONS.all = FLAGS.assertions
    if FLAGS["ode-assertions"].value:
        ASSERTIONS.ode = True
    else:
        ASSERTIONS.ode = FLAGS.assertions
    if FLAGS["anthem-assertions"].value:
        ASSERTIONS.anthem = True
    else:
        ASSERTIONS.anthem = FLAGS.assertions

    def _build_subdir_name():
        build_subdir = FLAGS["cmake-generator"].value.replace(" ", "_")
        # NOTE: It is not possible to set assertions to SDL at least
        # for now.
        # sdl_build_dir_label = args.sdl_build_variant
        ode_build_dir_label = BUILD_VARIANTS.ode
        if ASSERTIONS.ode:
            ode_build_dir_label += "Assert"
        anthem_build_dir_label = BUILD_VARIANTS.anthem
        if ASSERTIONS.anthem:
            anthem_build_dir_label += "Assert"
        # TODO It's currently impossible to use assertions in SDL
        sdl_build_dir_label = BUILD_VARIANTS.sdl
        if ode_build_dir_label == anthem_build_dir_label \
                and ode_build_dir_label == sdl_build_dir_label:
            build_subdir += "-" + ode_build_dir_label
        elif ode_build_dir_label != anthem_build_dir_label \
                and ode_build_dir_label == sdl_build_dir_label:
            build_subdir += "-" + ode_build_dir_label
            build_subdir += "+anthem-" + anthem_build_dir_label
        elif ode_build_dir_label == anthem_build_dir_label \
                and ode_build_dir_label != sdl_build_dir_label:
            build_subdir += "-" + ode_build_dir_label
            build_subdir += "+sdl-" + sdl_build_dir_label
        elif sdl_build_dir_label == anthem_build_dir_label \
                and ode_build_dir_label != sdl_build_dir_label:
            build_subdir += "-" + anthem_build_dir_label
            build_subdir += "+ode-" + ode_build_dir_label
        else:
            build_subdir += "+ode-" + ode_build_dir_label
            build_subdir += "+anthem-" + anthem_build_dir_label
            build_subdir += "+sdl-" + sdl_build_dir_label
        return build_subdir

    global BUILD_SUBDIR
    BUILD_SUBDIR = _build_subdir_name()

    logging.debug(
        "Building the project files in %s",
        os.path.join(BUILD_DIR, BUILD_SUBDIR)
    )

    # Create the paths of certain files and directories
    global TOOLCHAIN_STATUS_FILE
    TOOLCHAIN_STATUS_FILE = os.path.join(
        BUILD_DIR,
        "toolchain-{}-{}".format(ANTHEM.version, HOST_TARGET)
    )

    # Create the toolchain
    toolchain_data = None
    if os.path.exists(TOOLCHAIN_STATUS_FILE):
        with open(TOOLCHAIN_STATUS_FILE) as json_file:
            toolchain_data = json.load(json_file)
    global TOOLCHAIN
    TOOLCHAIN = toolchain.host_toolchain(
        HOST_TARGET,
        toolchain_data
    )

    logging.debug("The toolchain is %s", TOOLCHAIN)

    # Set the GitHub OAuth token if possible
    global GITHUB_OAUTH_TOKEN
    if FLAGS["auth-token-file"].value:
        if os.path.exists(FLAGS["auth-token-file"].value):
            with open(FLAGS["auth-token-file"].value) as token_file:
                # TODO This isn't not all that elegant solution
                GITHUB_OAUTH_TOKEN = token_file.readline().replace(
                    "\n",
                    ""
                )
        else:
            logging.error(
                "The GitHub OAuth token file '%s' set in command line flags "
                "isn't a file",
                FLAGS["auth-token-file"].value
            )
    elif FLAGS["auth-token"].value:
        GITHUB_OAUTH_TOKEN = FLAGS["auth-token"].value
    else:
        for var in GITHUB_OAUTH_ENV_VARIABLES:
            if var in os.environ:
                GITHUB_OAUTH_TOKEN = os.environ[var]
                break

    # Create the dependencies' build information
    with open(os.path.join(
        ODE_SOURCE_ROOT,
        ODE_REPO_NAME,
        "util",
        "composer",
        "dependencies.json"
    )) as f:
        components = json.load(f)
    for key, component in components.items():
        logging.debug(
            "Creating a mapping for '%s' (%s)",
            component["name"],
            key
        )
        DEPENDENCIES[key] = Mapping(repr=component["name"], key=key)
        dependency = DEPENDENCIES[key]
        if isinstance(component["version"], dict):
            dependency.version_data = Mapping()
            if "major" in component["version"]:
                for v_key, value in component["version"].items():
                    dependency.version_data[v_key] = value
                    logging.debug(
                        "The value of '%s' in the version of %s is %d",
                        v_key,
                        dependency.repr,
                        value
                    )
                dependency.version = "{}.{}.{}".format(
                    dependency.version_data.major,
                    dependency.version_data.minor,
                    dependency.version_data.patch
                )
            else:
                for v_key, value in component["version"].items():
                    dependency.version_data[v_key] = value
                    logging.debug(
                        "The value of '%s' in the version of %s is %s",
                        v_key,
                        dependency.repr,
                        value
                    )
                dependency.version = dependency.version_data.version
        else:
            dependency.version = component["version"]
        logging.debug(
            "The version of %s is %s",
            dependency.repr,
            dependency.version
        )
