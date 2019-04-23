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
This support module has the info necessary for building Lua.
"""

import os
import platform

from support import data

from support.variables import ODE_REPO_NAME, ODE_SOURCE_ROOT

from util import binaries, cmake, shell, workspace


def _create_cxx_header():
    if not os.path.isdir(
        os.path.join(data.session.shared_build_dir, "include")
    ):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "include"))
    cxx_header = os.path.join(
        data.session.shared_build_dir,
        "include",
        "lua.hpp"
    )
    if os.path.exists(cxx_header):
        shell.rm(cxx_header)
    with open(cxx_header, "w+") as outfile:
        outfile.write("// lua.hpp\n")
        outfile.write("// Lua header files for C++\n")
        outfile.write(
            "// <<extern \"C\">> not supplied automatically because Lua also "
            "compiles as C++\n"
        )
        outfile.write("\n")
        outfile.write("extern \"C\" {\n")
        outfile.write("#include \"lua.h\"\n")
        outfile.write("#include \"lualib.h\"\n")
        outfile.write("#include \"lauxlib.h\"\n")
        outfile.write("}\n")
        outfile.write("")


def _build_cmake(component, build_dir):
    src_dir = workspace.source_dir(component)
    tmp_dir = os.path.join(os.path.dirname(src_dir), "tmp")
    shell.makedirs(tmp_dir)
    shell.copytree(src_dir, tmp_dir)
    shell.copy(
        os.path.join(
            ODE_SOURCE_ROOT,
            ODE_REPO_NAME,
            "cmake",
            "lua",
            "CMakeLists.txt"
        ),
        os.path.join(tmp_dir, "CMakeLists.txt")
    )
    cmake.call(component, tmp_dir, build_dir)
    binaries.compile(component, build_dir, install=False)
    _create_cxx_header()
    if not os.path.isdir(os.path.join(data.session.shared_build_dir, "lib")):
        shell.makedirs(os.path.join(data.session.shared_build_dir, "lib"))
    lib_file = os.path.join(data.session.shared_build_dir, "lib", "lua.lib")
    if os.path.exists(lib_file):
        shell.rm(lib_file)
    shell.copy(os.path.join(build_dir, "Debug", "lua.lib"), lib_file)
    shell.rm(os.path.join(data.session.shared_build_dir, "include", "lua.h"))
    shell.rm(
        os.path.join(data.session.shared_build_dir, "include", "lualib.h")
    )
    shell.rm(
        os.path.join(data.session.shared_build_dir, "include", "lauxlib.h")
    )
    shell.rm(
        os.path.join(data.session.shared_build_dir, "include", "luaconf.h")
    )
    shell.copy(
        os.path.join(tmp_dir, "src", "lua.h"),
        os.path.join(data.session.shared_build_dir, "include", "lua.h")
    )
    shell.copy(
        os.path.join(tmp_dir, "src", "lualib.h"),
        os.path.join(data.session.shared_build_dir, "include", "lualib.h")
    )
    shell.copy(
        os.path.join(tmp_dir, "src", "lauxlib.h"),
        os.path.join(data.session.shared_build_dir, "include", "lauxlib.h")
    )
    shell.copy(
        os.path.join(tmp_dir, "src", "luaconf.h"),
        os.path.join(data.session.shared_build_dir, "include", "luaconf.h")
    )
    shell.rmtree(tmp_dir)


def _build(component, build_dir):
    src_dir = workspace.source_dir(component)
    shell.copytree(src_dir, build_dir)
    with shell.pushd(build_dir):
        if platform.system() == "Darwin":
            binaries.make(target="macosx")
        elif platform.system() == "Linux":
            binaries.make(target="linux")
        binaries.make(target="install", build_args="INSTALL_TOP={}".format(
            data.session.shared_build_dir
        ))


def build(component):
    """Builds the dependency."""
    bin_name = os.path.join("lib", "lua.lib") \
        if platform.system() == "Windows" \
        else os.path.join("lib", "liblua.a")
    if binaries.exist(component, bin_name):
        return
    with workspace.build_directory(component) as build_dir:
        if platform.system() == "Windows":
            _build_cmake(component, build_dir)
        else:
            _build(component, build_dir)
