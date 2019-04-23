# ------------------------------------------------------------- #
#                         Ode Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

from __future__ import print_function

import argparse
import os
import sys

from support import arguments, data

from support.presets import get_all_preset_names, get_preset_options

from support.variables import HOME, ODE_REPO_NAME, ODE_SOURCE_ROOT

from util import diagnostics, reflection, shell

from . import clone, preset, set_up


def _build_dependencies():
    diagnostics.debug_head("Starting to build the dependencies")
    shell.makedirs(os.path.join(data.session.shared_build_dir))
    shell.makedirs(os.path.join(
        ODE_SOURCE_ROOT,
        data.session.build_dir,
        data.session.host_target,
        "local"
    ))
    for key, value in data.session.dependencies.items():
        if value.repr == key:
            diagnostics.debug("Building {}".format(value.repr))
        else:
            diagnostics.debug("Building {} ({})".format(value.repr, key))
        getattr(reflection.import_build_component(key), "build")(
            data.session.dependencies[key]
        )


def run_preset():
    """
    Works out the preset of the bootstrap mode and runs the
    script with the arguments.
    """
    parser = preset.create_parser(True)
    args = parser.parse_args()

    shell.DRY_RUN = args.dry_run
    shell.ECHO = args.verbose >= 1

    diagnostics.DEBUG = args.verbose >= 1
    diagnostics.VERBOSE = args.verbose >= 2

    if not args.preset_file_names:
        args.preset_file_names = [
            os.path.join(HOME, ".anthem-build-presets"),
            os.path.join(HOME, ".ode-build-presets"),
            os.path.join(
                ODE_SOURCE_ROOT, ODE_REPO_NAME, "util", "build-presets.ini")
        ]

    if args.show_presets:
        for name in sorted(
                get_all_preset_names(args.preset_file_names), key=str.lower):
            print(name)
        return 0

    if not args.preset:
        diagnostics.fatal("Missing the '--preset' option")

    args.preset_substitutions = {}

    for arg in args.preset_substitutions_raw:
        name, value = arg.split("=", 1)
        args.preset_substitutions[name] = value

    preset_args = get_preset_options(
        args.preset_substitutions, args.preset_file_names, args.preset)

    build_script_args = [sys.argv[0]]
    build_script_args += ["bootstrap"]

    if args.dry_run:
        build_script_args += ["--dry-run"]
    if args.clean:
        build_script_args += ["--clean"]
    if args.verbose:
        build_script_args += ["--verbose", args.verbose]
    if args.develop_stack:
        build_script_args += ["--develop-stack"]
    build_script_args += preset_args
    if args.build_jobs:
        build_script_args += ["--jobs", str(args.build_jobs)]

    diagnostics.note("Using preset '{}', which expands to \n\n{}\n".format(
        args.preset, shell.quote_command(build_script_args)))
    diagnostics.debug(
        "The script will run with '{}' as the Python executable\n".format(
            sys.executable))

    if args.expand_build_script_invocation:
        return 0

    command_to_run = [sys.executable] + build_script_args

    shell.caffeinate(command_to_run)

    return 0


def run():
    parser = arguments.create_argument_parser()
    # TODO Unknown args
    args, unknown_args = parser.parse_known_args(
        list(arg for arg in sys.argv[1:] if arg != '--'))
    set_up.run(args, True)
    clone.run(True)
    _build_dependencies()
    return 0
