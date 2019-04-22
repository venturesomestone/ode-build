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
This support module has the functions for downloading the
dependencies.
"""

import json
import os

from support import data

from util import diagnostics


__all__ = ["run"]


_SOURCE_TARGET = "source"


def _write_version_file(versions, final_write=False):
    with open(data.session.shared_status_file, "w") as outfile:
        json.dump(versions, outfile)

    if final_write:
        log_function = diagnostics.debug_ok
    else:
        log_function = diagnostics.debug
    log_function("Wrote the dependency version information to {}".format(
        data.session.shared_status_file))


def _get_component(component, versions):
    getattr(component.clone_module, "get_dependency")(component)

    if component.is_source:
        target = _SOURCE_TARGET
    else:
        target = data.session.host_target
    # info = {"version": component.version, "targets": [target]}
    info = {"version": "0", "targets": [target]}
    versions[component.key] = info


def run(bootstrap):
    """
    Run the download script.

    bootstrap -- whether or not this is called from the bootstrap
    script and not the build script
    """
    if not bootstrap:
        diagnostics.fatal(
            "The download of the dependencies cannot be run from the build "
            "script")

    diagnostics.debug_head("Starting the download of the dependencies")

    args = data.session.args

    if os.path.isfile(data.session.shared_status_file):
        with open(data.session.shared_status_file) as json_file:
            versions = json.load(json_file)
    else:
        versions = {}

    def _skip_repositories():
        toolchain = data.session.toolchain
        skip_list = []
        if toolchain.cmake is not None:
            skip_list += ["cmake"]
        if toolchain.ninja is not None:
            pass
            # skip_list += ["ninja"]
        # if not args.build_test:
        #     skip_list += ["catch"]
        return skip_list

    skip_repository_list = _skip_repositories()

    diagnostics.debug("Using {} to make the hypertext calls".format(
        data.session.connection_protocol.upper()))
    diagnostics.trace("The dependencies to be skipped are {}".format(
        skip_repository_list))

    for key, component in data.session.dependencies.items():
        name = component.repr

        diagnostics.debug("Beginning to update {}".format(name))

        if key in skip_repository_list:
            diagnostics.debug(
                "{} is on the list of repositories to be skipped".format(name))
            continue

        if not args.clean:
            if component.is_source:
                target = _SOURCE_TARGET
            else:
                target = data.session.host_target
            # TODO Cross-compile targets
            if key in versions \
                    and component.version == versions[key]["version"] \
                    and target in versions[key]["targets"]:
                diagnostics.trace(
                    "{} should not be re-downloaded, skipping".format(name))
                continue
        _get_component(component, versions)
        diagnostics.debug_ok("Updating {} is complete".format(name))
        _write_version_file(versions)

    _write_version_file(versions)

    diagnostics.debug_head("The download of the dependencies is done")
