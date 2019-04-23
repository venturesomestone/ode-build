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

import argparse


def create_parser():
    """
    Makes the parser containing the arguments for the preset
    mode.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Builds Obliging Ode and Unsung Anthem using a preset.")
    parser.add_argument(
        "-n", "--dry-run",
        help="print the commands that would be run, but don't run them",
        action="store_true",
        default=False)
    parser.add_argument(
        "-c", "--clean",
        help="do a clean build",
        action="store_true",
        default=False)
    parser.add_argument(
        "--preset-file",
        help="load presets from the given file",
        metavar="PATH",
        action="append",
        dest="preset_file_names",
        default=[])
    parser.add_argument(
        "--preset",
        help="use the given option preset",
        metavar="NAME")
    parser.add_argument(
        "--show-presets",
        help="list all presets and exit",
        action="store_true")
    parser.add_argument(
        "-j", "--jobs",
        help="the number of parallel build jobs to use",
        type=int,
        dest="build_jobs")
    parser.add_argument(
        "preset_substitutions_raw",
        help="'name=value' pairs that are substituted in the preset",
        nargs="*",
        metavar="SUBSTITUTION")
    parser.add_argument(
        "--expand-build-script-invocation",
        help="Print the build-script invocation made by the preset, but "
             "don't run it",
        action="store_true")
    parser.add_argument(
        "-v", "--verbose",
        help="print the commands executed during the build",
        action="store",
        type=int,
        default=0)
    parser.add_argument(
        "--develop-stack",
        help="Use the local, development version of the build script",
        action="store_true")

    return parser
