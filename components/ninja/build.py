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
This support module has the info necessary for building Ninja.
"""

import os
import platform
import sys

from support import data

from util import binaries, shell, workspace


def skip_build(component, has_correct_version):
    """Whether the build is skippped."""
    bin_name = os.path.join("bin", "ninja.exe") \
        if platform.system() == "Windows" else os.path.join("bin", "ninja")
    return data.session.toolchain.ninja is not None or (
        binaries.exist(component, bin_name) and has_correct_version
    )
    # and not data.session.args.build_ninja


def build(component):
    """Builds the dependency."""
    bin_name = os.path.join("bin", "ninja.exe") \
        if platform.system() == "Windows" else os.path.join("bin", "ninja")

    src_dir = workspace.source_dir(component)
    src_bin = os.path.join(src_dir, "ninja.exe") \
        if platform.system() == "Windows" else os.path.join(src_dir, "ninja")
    bin_file = os.path.join(data.session.shared_build_dir, bin_name)

    if os.path.exists(src_bin):
        if os.path.exists(bin_file):
            shell.rm(bin_file)
        if not os.path.isdir(
            os.path.join(data.session.shared_build_dir, "bin")
        ):
            shell.makedirs(os.path.join(data.session.shared_build_dir, "bin"))
        shell.copy(src_bin, bin_file)
        data.session.toolchain.ninja = bin_file
        shell.call(["chmod", "+x", str(bin_file)])
        return

    with workspace.build_directory(component) as build_dir:
        # Ninja can only be built in-tree.
        shell.copytree(src_dir, build_dir)
        toolchain = data.session.toolchain
        env = None
        if platform.system() == "Darwin":
            from util import xcrun
            sysroot = xcrun.sdk_path("macosx")
            osx_version_min = data.session.args.darwin_deployment_version
            assert sysroot is not None
            env = {
                "CC": toolchain.cc,
                "CXX": toolchain.cxx,
                "CFLAGS": (
                    "-isysroot {sysroot} "
                    "-mmacosx-version-min={osx_version}"
                ).format(sysroot=sysroot, osx_version=osx_version_min),
                "LDFLAGS": "-mmacosx-version-min={osx_version}".format(
                    osx_version=osx_version_min
                )
            }
        elif toolchain.cxx:
            env = {"CC": toolchain.cc, "CXX": toolchain.cxx}
        with shell.pushd(build_dir):
            shell.call(
                [sys.executable, "configure.py", "--bootstrap"],
                env=env
            )
        shell.rm(bin_file)
        shell.copy(os.path.join(build_dir, bin_name), bin_file)
        data.session.toolchain.ninja = bin_file
        shell.call(["chmod", "+x", str(bin_file)])
