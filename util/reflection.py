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
This support module has functions for reflection.
"""

import os
import sys

from absl import logging

from support.values import SCRIPT_DIR


def _component_module(name, module):
    """
    Imports the clone module of a dependency component module.

    name -- the name of the component
    module -- the name of the module
    """
    path = os.path.join(SCRIPT_DIR, "components", name, "{}.py".format(module))
    logging.debug(
        "Importing module %s of component %s from %s",
        module,
        name,
        path
    )
    if sys.version_info.major >= 3:
        if sys.version_info.minor >= 4:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logging.debug("Got the module components.%s.%s", name, module)
            return module
        else:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(name, path).load_module()
            logging.debug("Got the module components.%s.%s", name, module)
            return module
    else:
        import imp
        module = imp.load_source(name, path)
        logging.debug("Got the module components.%s.%s", name, module)
        return module


def import_clone_component(name):
    """
    Imports the clone module of a dependency component module.

    name -- the name of the component
    """
    return _component_module(name, "clone")


def get_custom_version_data(component):
    """
    Gives the possible optional extra version data of a
    dependency component module as a dictionary.

    component -- the component
    """
    module = _component_module(component.key, "clone")
    if hasattr(module, "version_data"):
        v_data = getattr(module, "version_data")()
        for key, value in v_data.items():
            logging.debug(
                "%s has custom version data: '%s': '%s'",
                component.repr,
                key,
                value
            )
    else:
        v_data = None
    return v_data
