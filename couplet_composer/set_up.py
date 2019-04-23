# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""
This support module has the set up functions used by both the
build script and the bootstrap script.
"""

from __future__ import print_function

import os
import platform
import sys
import time

from support import data, defaults

from support.variables import ODE_BUILD_ROOT, ODE_SCRIPT_ROOT, ODE_SOURCE_ROOT

from util import diagnostics, shell, workspace

from util.mapping import Mapping

from util.toolchain import host_toolchain

from . import component_set_up


__all__ = ["run"]


def _exit_rejecting_arguments(message, parser=None):
    print(message, file=sys.stderr)
    if parser:
        parser.print_usage(sys.stderr)
    sys.exit(2)  # 2 is the same as 'argparse' error exit code.


def _validate_arguments(args, bootstrap):
    # if not args.build_ode and not args.build_anthem:
    #     _exit_rejecting_arguments(
    #         "Both the build of Obliging Ode and the build of Unsung Anthem "
    #         "cannot be skipped")
    # if not args.std == "c++2a" and not args.std == "c++17":
    #     _exit_rejecting_arguments(
    #         "C++ standard version is set to an invalid value: "
    #         "{}".format(args.std))
    # if args.stdlib:
    #     if not args.stdlib == "libc++" and not args.stdlib == "libstdc++":
    #         _exit_rejecting_arguments(
    #             "C++ standard library implementation is set to an invalid "
    #             "value: {}".format(args.stdlib))
    if not bootstrap:
        if not args.cmake_generator == "Ninja" \
                and not args.cmake_generator == "Unix Makefiles" \
                and not args.cmake_generator == "Xcode" \
                and not args.cmake_generator == "Visual Studio 14 2015" \
                and not args.cmake_generator == "Visual Studio 15 2017" \
                and not args.cmake_generator == "Eclipse CDT4 - Ninja":
            _exit_rejecting_arguments(
                "CMake generator is set to an invalid value: "
                "{}".format(args.cmake_generator))


def _clean_delay():
    def _impl_write(index):
        sys.stdout.write(
            diagnostics.RED + "\b{!s}".format(index) + diagnostics.ENDC)
        sys.stdout.flush()
        time.sleep(1)
        return index
    sys.stdout.write(
        diagnostics.RED + "Starting a clean build in  " + diagnostics.ENDC)
    index_list = [_impl_write(i) for i in reversed(range(0, 4))]
    print(diagnostics.RED + "\b\b\b\bnow." + diagnostics.ENDC)
    return index_list


def run(args):
    """Run the common set up phase of the scripts."""
    shell.DRY_RUN = args.dry_run
    shell.ECHO = args.verbosity >= 1

    diagnostics.DEBUG = args.verbosity >= 1
    diagnostics.VERBOSE = args.verbosity >= 2

    diagnostics.debug(
        "Setting up version {} of {} and version {} of {}".format(
            defaults.ANTHEM_VERSION,
            defaults.ANTHEM_NAME,
            defaults.ODE_VERSION,
            defaults.ODE_NAME
        )
    )

    diagnostics.debug_head("Starting the setup phase")

    if args.build_subdir is None:
        args.build_subdir = workspace.compute_build_subdir_name(args)

    diagnostics.trace(
        "The build subdirectory is set to {}".format(args.build_subdir)
    )

    data.session = Mapping(
        args=args,
        # The source root is the directory that the repository
        # directory and the other related projects are for
        # development.
        source_root=ODE_SOURCE_ROOT,
        # The build root is the directory, usually under the
        # source root, that contains the files downloaded and
        # created by the bootstrap script or the build script.
        # Most often it is $ODE_SOURCE_ROOT/build.
        build_root=ODE_BUILD_ROOT,
        # The shared directory in the build root is the directory
        # that the projects needed to build the project are
        # downloaded to.
        shared_dir=os.path.join(ODE_BUILD_ROOT, "shared"),
        # The build directory in the build root is the
        # directory that the build files are created in.
        build_dir=os.path.join(
            ODE_BUILD_ROOT,
            "build",
            args.ode_version,
            args.build_subdir
        ),
        # The script directory in the build root is the
        # directory that the build script files are copied in.
        script_dir=ODE_SCRIPT_ROOT,
        # The dependencies are the projects that are needed to
        # build the project. The dependencies are built by the
        # bootstrap script.
        dependencies=Mapping(),
        # This is the mapping that contains the data for building
        # Obliging Ode.
        ode=Mapping(version=args.ode_version),
        # This is the mapping that contains the data for building
        # Unsung Anthem.
        anthem=Mapping(version=args.anthem_version),
        host_target=args.host_target,
        # TODO The C++ standard
        # std=args.std,
        # TODO The C++ standard library implementation
        # stdlib=args.stdlib,
        # TODO This will be removed
        build_lua_with_cmake=platform.system() == "Windows"
    )

    # The shared build directory in the build directory is the
    # directory that the dependency binaries are created in.
    data.session.shared_build_dir = os.path.join(
        ODE_BUILD_ROOT,
        "build",
        "shared",
        args.build_subdir,
        data.session.host_target,
        "local"
    )

    data.session.visual_studio = \
        args.cmake_generator == "Visual Studio 14 2015" \
        or args.cmake_generator == "Visual Studio 15 2017"

    diagnostics.trace("The mapping of the session data is created")

    diagnostics.debug("The source root is set to {}".format(
        data.session.source_root
    ))
    diagnostics.debug("The build root is set to {}".format(
        data.session.build_root
    ))
    diagnostics.debug("The shared directory is set to {}".format(
        data.session.shared_dir
    ))
    diagnostics.debug("The build directory is set to {}".format(
        data.session.build_dir
    ))
    diagnostics.debug("The script directory is set to {}".format(
        data.session.script_dir
    ))
    diagnostics.debug("The shared build directory is set to {}".format(
        data.session.shared_build_dir
    ))

    if args.clean:
        _clean_delay()
        shell.rmtree(path=data.session.shared_dir)
        shell.rmtree(path=data.session.build_dir)
        shell.rmtree(path=data.session.shared_build_dir)

    shell.makedirs(data.session.shared_dir)
    shell.makedirs(data.session.build_dir)
    shell.makedirs(data.session.shared_build_dir)

    diagnostics.trace("Created the build directories")

    os.environ["TOOLCHAINS"] = "default"
    data.session.toolchain = host_toolchain(args=args)

    data.session.ci = "CI" in os.environ and os.environ["CI"]

    if args.auth_token:
        data.session.github_token = args.auth_token
    elif "ODE_OAUTH" in os.environ:
        data.session.github_token = str(os.environ["ODE_OAUTH"])
    elif "ANTHEM_OAUTH" in os.environ:
        data.session.github_token = str(os.environ["ANTHEM_OAUTH"])

    if not data.session.github_token:
        with open(args.auth_token_file) as file:
            # TODO This isn't not all that elegant solution
            data.session.github_token = file.readline().replace("\n", "")

    data.session.connection_protocol = defaults.PROTOCOL

    # The shared status file is a JSON file containing the
    # versions of the dependencies in order to determine whether
    # to download new versions of them.
    data.session.shared_status_file = os.path.join(
        data.session.shared_dir,
        "status"
    )

    component_set_up.run()

    diagnostics.debug_head("Setup phase is done")
