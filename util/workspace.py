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
This utility module works out the directories to be used in the
project workspace.
"""

import os

from contextlib import contextmanager

from couplet_composer.flags import FLAGS

from support.values import \
    ASSERTIONS, \
    BUILD_VARIANTS, \
    DOWNLOAD_DIR, \
    HOST_TARGET

from util import shell


def source_dir(component):
    """
    Create an absolute path to the source directory of a
    dependency.
    """
    if component.is_source:
        target = "source"
    else:
        target = HOST_TARGET
    return os.path.join(DOWNLOAD_DIR, component.key, component.version, target)


def temporary_dir(component):
    """
    Create an absolute path to the temporary directory of a
    dependency.
    """
    return os.path.join(DOWNLOAD_DIR, component.key, "tmp")


@contextmanager
def clone_dir_context(component):
    """Creates the directories for cloning a dependency."""
    shell.rmtree(source_dir(component))
    shell.rmtree(temporary_dir(component))
    shell.makedirs(source_dir(component))
    shell.makedirs(temporary_dir(component))
    yield
    shell.rmtree(temporary_dir(component))
