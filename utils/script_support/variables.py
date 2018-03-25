#===----------------------------- variables.py ---------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (c) 2018 Venturesome Stone
# Licensed under GNU Affero General Public License v3.0

"""The support module containing build variables."""


import os


# $HOME is got as an environment variable so it is set to the value it is
# expected to have.
HOME = os.environ.get("HOME", "/")


def _script_path():
    # Get the parent directory of this file for checking if this file is
    # located in an Unsung Anthem checkout.
    #
    # $ANTHEM_SOURCE_ROOT/script/script_support/variables.py
    script_path = os.path.dirname(os.path.dirname(__file__))
    # Split the path as the first part of the 'utils_path' is presumably the
    # script checkout.
    root_path, parent_dirname = os.path.split(script_path)
    if parent_dirname != "script":
        return ""
    # The checkout has to have CMake Listfile.
    if not os.path.exists(os.path.join(
            root_path, "unsung-anthem", "CMakeLists.txt")):
        return ""
    return script_path


def _get_default_source_root():
    return os.path.dirname(_script_path())


# $ANTHEM_SOURCE_ROOT is resolved from the path of this file if the environment
# variable is not set.
ANTHEM_SOURCE_ROOT = os.environ.get(
    "ANTHEM_SOURCE_ROOT", _get_default_source_root())


# $ANTHEM_CHECKOUT_ROOT is resolved from $ANTHEM_SOURCE_ROOT if the environment
# variable is not set.
ANTHEM_CHECKOUT_ROOT = os.environ.get(
    "ANTHEM_CHECKOUT_ROOT", os.path.join(ANTHEM_SOURCE_ROOT, "checkout"))


# $ANTHEM_BUILD_ROOT is resolved from $ANTHEM_SOURCE_ROOT if the environment
# variable is not set.
ANTHEM_BUILD_ROOT = os.environ.get(
    "ANTHEM_BUILD_ROOT", os.path.join(ANTHEM_SOURCE_ROOT, "build"))


# TODO
# def _get_default_anthem_repo_name():
#     # Split the path of the checkout directory as the latter part of it is the
#     # filename of the checkout directory.
#     _, anthem_repo_name = os.path.split(_anthem_path())
#     return anthem_repo_name


# $ANTHEM_REPO_NAME is resolved from the path of this file if the environment
# variable is not set.
ANTHEM_REPO_NAME = os.environ.get("ANTHEM_REPO_NAME", "unsung-anthem")


SCRIPT_DIR = os.path.join(ANTHEM_SOURCE_ROOT, "script")  # TODO _script_path()


ANTHEM_SCRIPT_DIR = os.path.join(ANTHEM_SOURCE_ROOT, ANTHEM_REPO_NAME, "utils")


CHECKOUT_FILE = os.path.join(ANTHEM_CHECKOUT_ROOT, "data")


SOURCE_TARGET = "src"
