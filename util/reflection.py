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
This support module has functions for reflection.
"""

import os
import sys

from support import data

from . import diagnostics


def import_clone_component(name):
    """
    Imports the clone module of a dependency component module.

    name -- the name of the component
    """
    path = os.path.join(
        data.session.script_dir, "components", name, "clone.py")
    diagnostics.trace("Importing component '{}' from path '{}'".format(
        name, path))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            diagnostics.trace(
                "Got the module components.{}.clone".format(name))
            return module
        else:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(name, path).load_module()
            diagnostics.trace(
                "Got the module components.{}.clone".format(name))
            return module
    else:
        import imp
        module = imp.load_source(name, path)
        diagnostics.trace("Got the module components.{}.clone".format(name))
        return module


def get_custom_version_data(component):
    """
    Gives the possible optional extra version data of a
    dependency component module as a dictionary.

    component -- the component
    """
    name = component.key
    path = os.path.join(
        data.session.script_dir, "components", name, "clone.py")
    diagnostics.trace("Importing component '{}' from path '{}'".format(
        name, path))
    module = None
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            diagnostics.trace(
                "Got the module components.{}.clone".format(name))
        else:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(name, path).load_module()
            diagnostics.trace(
                "Got the module components.{}.clone".format(name))
    else:
        import imp
        module = imp.load_source(name, path)
        diagnostics.trace("Got the module components.{}.clone".format(name))

    if hasattr(module, "version_data"):
        v_data = getattr(module, "version_data")()
        for key, value in v_data.items():
            diagnostics.trace("{} has custom version data: '{}': '{}'".format(
                component.repr,
                key,
                value
            ))
    else:
        v_data = None
    return v_data


def import_build_component(name):
    """
    Imports the build module of a dependency component module.

    name -- the name of the component
    """
    path = os.path.join(
        data.session.script_dir, "components", name, "build.py")
    diagnostics.trace("Importing component '{}' from path '{}'".format(
        name, path))
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            diagnostics.trace(
                "Got the module components.{}.build".format(name))
            return module
        else:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(name, path).load_module()
            diagnostics.trace(
                "Got the module components.{}.build".format(name))
            return module
    else:
        import imp
        module = imp.load_source(name, path)
        diagnostics.trace("Got the module components.{}.build".format(name))
        return module
