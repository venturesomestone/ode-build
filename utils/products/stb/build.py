#===------------------------------- build.py -----------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (c) 2018 Venturesome Stone
# Licensed under GNU Affero General Public License v3.0

"""The support module containing the utilities for stb_image build."""


import os
import platform

from build_utils import shell, workspace

from products import common

from script_support import data

from script_support.variables import ANTHEM_REPO_NAME, ANTHEM_SOURCE_ROOT


def _create_cxx_header():
    cxx_header = os.path.join(data.build.local_root, "include", "lua.hpp")
    if not os.path.exists(cxx_header):
        with open(cxx_header, "w+") as outfile:
            outfile.write("// lua.hpp\n")
            outfile.write("// Lua header files for C++\n")
            outfile.write(
                "// <<extern \"C\">> not supplied automatically because Lua "
                "also compiles as C++\n")
            outfile.write("\n")
            outfile.write("extern \"C\" {\n")
            outfile.write("#include \"lua.h\"\n")
            outfile.write("#include \"lualib.h\"\n")
            outfile.write("#include \"lauxlib.h\"\n")
            outfile.write("}\n")
            outfile.write("")


def _build():
    """Do the build of stb_image."""
    product = data.build.products.stb
    bin_path = workspace.include_file(path="stb_image.h")
    if common.build.binary_exists(product=product, path=bin_path):
        return
    source_dir = workspace.source_dir(product)
    include = workspace.include_file(path="stb_image.h")
    if not workspace.is_include_dir_made() and workspace.include_file_exists(
            path="stb_image.h"):
        shell.rm(include)
    shell.copytree(os.path.join(source_dir, "stb_image.h"), include)


def do_build():
    """Build stb_image."""
    product = data.build.products.stb
    common.build.check_source(product)
    _build()


def should_build():
    """Check whether this product should be built."""
    return True
