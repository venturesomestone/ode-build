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

"""This module downloads the dependecies of the project."""

import json
import os

from absl import logging

from couplet_composer.flags import FLAGS

from util import reflection

from support.values import \
    CONNECTION_PROTOCOL, \
    DEPENDENCIES, \
    DOWNLOAD_STATUS_FILE, \
    HOST_TARGET, \
    SOURCE_TARGET, \
    TOOLCHAIN

from support import values


def _write_version_file(versions):
    with open(DOWNLOAD_STATUS_FILE, "w") as outfile:
        json.dump(versions, outfile, indent=2, sort_keys=True)
    logging.debug(
        "Wrote the dependency version information to %s",
        DOWNLOAD_STATUS_FILE
    )


def _download_component(component, versions):
    clone_module = reflection.import_clone_component(component.key)
    getattr(clone_module, "get_dependency")(component)
    if getattr(reflection.import_clone_component(component.key), "SOURCE"):
        target = SOURCE_TARGET
    else:
        target = HOST_TARGET
    info = {"version": component.version, "targets": [target]}
    extra_data = reflection.get_custom_version_data(component)
    if extra_data is not None:
        for key, value in extra_data.items():
            logging.debug(
                "Adding the extra data item '%s' for key %s to the verson "
                "JSON",
                value,
                key
            )
            info[key] = value
    versions[component.key] = info


def _has_correct_version(component, versions, target):
    key = component.key
    added = key in versions
    if not added:
        return False
    version_equals = component.version == versions[key]["version"]
    same_target = target in versions[key]["targets"]
    extra_data = reflection.get_custom_version_data(component)
    if extra_data is not None:
        record = versions[key]
        for key, value in extra_data.items():
            if record[key] is None:
                logging.debug(
                    "The key %s isn't in the downloaded version data",
                    key
                )
                return False
            logging.debug(
                "The value of %s in the downloaded version data is %s",
                key,
                record[key]
            )
            if record[key] != value:
                return False
    return version_equals and same_target


def download_dependencies():
    """Downloads the dependecies of the project."""
    logging.info("Downloading the dependencies")
    if os.path.isfile(DOWNLOAD_STATUS_FILE):
        with open(DOWNLOAD_STATUS_FILE) as json_file:
            versions = json.load(json_file)
    else:
        versions = {}

    # The download of some dependencies is skipped if they're not
    # needed.
    def _skip_repositories():
        logging.debug("The toolchain in clone is %s", values.TOOLCHAIN)
        skip_list = []
        if values.TOOLCHAIN.cmake is not None:
            skip_list += ["cmake"]
        if values.TOOLCHAIN.ninja is not None:
            skip_list += ["ninja"]
        return skip_list

    skip_repository_list = _skip_repositories()

    logging.debug(
        "Using %s to make the hypertext transfer calls",
        CONNECTION_PROTOCOL.upper()
    )
    logging.debug(
        "The dependencies to be skipped are %s",
        ", ".join(skip_repository_list)
    )
    for key, component in DEPENDENCIES.items():
        name = component.repr
        logging.debug("Starting the download iteration of %s", name)

        if key in skip_repository_list:
            logging.debug(
                "The download of %s is skipped as it's on the list of the "
                "repositories to be skipped",
                name
            )
            continue

        if not FLAGS.clean:
            # The target of the dependency here isn't the source
            # that the dependency is built for but the target
            # that the dependency's distribution is for. If the
            # target is 'SOURCE_TARGET', it means the dependency
            # distribution is in source code.
            if component.is_source:
                target = SOURCE_TARGET
            else:
                target = HOST_TARGET
            # TODO Cross-compile targets
            if _has_correct_version(component, versions, target):
                logging.debug(
                    "The version %s of %s is already downloaded",
                    component.version,
                    name
                )
                continue
        _download_component(component, versions)
        logging.debug("Downloading %s is complete", name)

    _write_version_file(versions)

    logging.info("The download of the dependencies is done")
