# ------------------------------------------------------------- #
#                 Obliging Ode & Unsung Anthem
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
This support module has the set up functions used to create the
mapping of the build components.
"""

import json
import os

from support import data

from support.variables import ODE_SOURCE_ROOT, ODE_REPO_NAME

from util import diagnostics

from util.mapping import Mapping

from util.reflection import import_clone_component


__all__ = ["run"]


def run(bootstrap):
    """
    Create the mappings of the dependencies and components of the
    build.

    bootstrap -- whether or not this is called from the bootstrap
    script and not the build script
    """
    with open(os.path.join(
            ODE_SOURCE_ROOT, ODE_REPO_NAME, "util", "build",
            "dependencies.json")) as f:
        components = json.load(f)

    for key, component in components.items():
        diagnostics.trace(
            "Creating a mapping for the component '{}' ({})".format(
                component["name"], key))

        data.session.dependencies[key] = Mapping(
            repr=component["name"], key=key)

        dependency = data.session.dependencies[key]

        if isinstance(component["version"], dict):
            dependency.version_data = Mapping()
            for v_key, value in component["version"].items():
                dependency.version_data[v_key] = value
                diagnostics.trace(
                    "The value of '{}' in the version of {} is {}".format(
                        v_key, dependency.repr, value))
            dependency.version = "{}.{}.{}".format(
                dependency.version_data.major, dependency.version_data.minor,
                dependency.version_data.patch)
            diagnostics.trace("The version of {} is {}".format(
                dependency.repr, dependency.version))
        else:
            dependency.version = component["version"]
            diagnostics.trace("The version of {} is {}".format(
                dependency.repr, dependency.version))

        dependency.clone_module = import_clone_component(key)

        dependency.is_source = getattr(dependency.clone_module, "SOURCE")

        if dependency.is_source:
            diagnostics.trace(
                "{} is going to be downloaded as source code".format(
                    dependency.repr))
        else:
            diagnostics.trace(
                "{} is going to be downloaded as a binary".format(
                    dependency.repr))

        dependency.github = getattr(dependency.clone_module, "GITHUB")

        if dependency.github:
            diagnostics.trace(
                "{} is going to be downloaded from GitHub".format(
                    dependency.repr))
            dependency.github_data = getattr(
                dependency.clone_module, "GITHUB_DATA")
        else:
            diagnostics.trace(
                "{} isn't going to be downloaded from GitHub".format(
                    dependency.repr))
