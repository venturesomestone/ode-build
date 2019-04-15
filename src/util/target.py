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
This utility module works out the platform that the project
should be built for.
"""

import platform

from .mapping import Mapping


def _create_target(system, arch):
    """
    Create a dictionary representation of a target that Obliging
    Ode can run on.
    """
    result = Mapping(
        platform=system, arch=arch, name="{}-{}".format(system.name, arch))
    return result


def _create_platform(name, system, archs):
    """
    Create a dictionary representation of a platform that
    Obliging Ode can run on.
    """
    result = Mapping(name=name, system=system)
    result["targets"] = [_create_target(result, arch) for arch in archs]
    for target in result.targets:
        result[target.arch] = target
    return result


def host_target():
    """
    Return the host target for the build machine, if it is one of
    the recognized targets.
    """
    system = platform.system()
    machine = platform.machine()

    def _filter_armv(target):
        if system == "Linux":
            return (machine.startswith("armv6") and target == "armv6") \
                or (machine.startswith("armv7") and target == "armv7")
        return False
    macos = _create_platform(name="macos", system="Darwin", archs=["x86_64"])
    linux = _create_platform(
        name="linux", system="Linux", archs=[
            "x86_64", "armv6", "armv7", "aarch64", "powerpc64", "powerpc64le",
            "s390x"
        ])
    freebsd = _create_platform(
        name="freebsd", system="FreeBSD", archs=["x86_64"])
    cygwin = _create_platform(
        name="cygwin", system="CYGWIN_NT-10.0", archs=["x86_64"])
    windows = _create_platform(
        name="windows", system="Windows", archs=["x86_64", "AMD64"])
    known_platforms = [macos, linux, freebsd, cygwin, windows]
    found_platform = [p for p in known_platforms if p.system == system]
    if found_platform:
        found_target = [t for t in found_platform[0].targets
                        if t.arch == machine or _filter_armv(t)]
        if found_target:
            return found_target[0]
    raise NotImplementedError(
        "System '{}' with architecture '{}' is not supported".format(
            system, machine))
