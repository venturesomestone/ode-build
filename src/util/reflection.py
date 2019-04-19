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
    diagnostics.trace("Importing component '{}'".format(name))
    path = os.path.join(
        data.session.script_dir, "components", name, "clone.py")
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
