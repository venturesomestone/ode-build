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

"""This module contains miscellaneous GitHub helpers."""


def create_github_version(component, github_data):
    """Concatenate the full version for GitHub."""
    if github_data.version_prefix:
        ret = "{}{}".format(github_data.version_prefix, component.version)
    else:
        ret = component.version
    return ret
