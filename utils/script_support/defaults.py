#===----------------------------- defaults.py ----------------*- python -*-===#
#
#                         Obliging Ode & Unsung Anthem
#
# This source file is part of the Obliging Ode and Unsung Anthem open source
# projects.
#
# Copyright (c) 2018 Venturesome Stone
# Licensed under GNU Affero General Public License v3.0

"""Default option value definitions."""


import os
import platform

from build_utils.mapping import Mapping

from build_utils.reflection import anthem_config_value

from .product_config import product_config, version_config, github_config, \
    asset, SOURCE_ASSET, platform_specific_asset, platform_file_config, \
    ode_anthem_config


__all__ = [
    # Command line configurable
    "BUILD_VARIANT", "CMAKE_GENERATOR", "CXX_STANDARD", "ANTHEM_VERSION",
    "ODE_VERSION", "DARWIN_DEPLOYMENT_VERSION", "UNIX_INSTALL_PREFIX",
    "DARWIN_INSTALL_PREFIX",

    # Constants
    "PRODUCT_CONFIG", "PROTOCOL", "GITHUB_API_V4_ENDPOINT"
]


# Options that can be "configured" by command line options

BUILD_VARIANT = "Debug"
CMAKE_GENERATOR = "Ninja"

CXX_STANDARD = "c++17"

ANTHEM_VERSION = anthem_config_value("ANTHEM_VERSION")
ODE_VERSION = anthem_config_value("ODE_VERSION")

DARWIN_DEPLOYMENT_VERSION = "10.9"

UNIX_INSTALL_PREFIX = "/usr"
DARWIN_INSTALL_PREFIX = "/Applications/Xcode.app/Contents/Developer" \
                        "/Toolchains/XcodeDefault.xctoolchain/usr"

# Options that can only be "configured" by editing this file.
#
# These options are not exposed as command line options on purpose. If you
# need to change any of these, you should do so on trunk or in a branch.

SCRIPT_VERSION = "0.3.0"

PROTOCOL = "https"
GITHUB_API_V4_ENDPOINT = "https://api.github.com/graphql"


COVERAGE_TARGET_MARK = "c"


PRODUCT_CONFIG = Mapping(
    anthem=ode_anthem_config(
        version=anthem_config_value("ANTHEM_VERSION"),
        name=anthem_config_value("ANTHEM_NAME"),
        key=anthem_config_value("ANTHEM_KEY"),
        window_name=anthem_config_value("ANTHEM_WINDOW_NAME"),
        logger_name=anthem_config_value("ANTHEM_LOGGER_NAME"),
        is_tool=False,
        is_source=True
    ),

    benchmark=product_config(
        version=anthem_config_value("BENCHMARK_VERSION"),
        name="benchmark",
        key="benchmark",
        is_tool=False,
        is_source=True,
        github_data=github_config(
            owner="google",
            name="benchmark",
            asset_data=SOURCE_ASSET,
            version_prefix="v"
        )
    ),

    clara=product_config(
        version=anthem_config_value("CLARA_VERSION"),
        name="Clara",
        key="clara",
        is_tool=False,
        is_source=True,
        github_data=github_config(
            owner="catchorg",
            name="Clara",
            asset_data=asset("clara.hpp"),
            version_prefix="v"
        )
    ),

    cmake=product_config(
        version=version_config(
            major=anthem_config_value("CMAKE_MAJOR_VERSION"),
            minor=anthem_config_value("CMAKE_MINOR_VERSION"),
            patch=anthem_config_value("CMAKE_PATCH_VERSION")
        ),
        name="CMake",
        key="cmake",
        is_tool=True,
        is_source=False,
        url_format="{protocol}://cmake.org/files/v{major_minor}/cmake-"
                   "{version}-{platform}.{extension}"
    ),

    glad=product_config(
        version=anthem_config_value("GLAD_VERSION"),
        name="glad",
        key="glad",
        is_tool=False,
        is_source=True,
        github_data=github_config(
            owner="Dav1dde",
            name="glad",
            asset_data=SOURCE_ASSET,
            version_prefix="v"
        )
    ),

    googletest=product_config(
        version=anthem_config_value("GOOGLETEST_VERSION"),
        name="Google Test",
        key="googletest",
        is_tool=False,
        is_source=True,
        github_data=github_config(
            owner="google",
            name="googletest",
            asset_data=SOURCE_ASSET,
            version_prefix="release-"
        )
    ),

    llvm=product_config(
        version=anthem_config_value("LLVM_VERSION"),
        name="Low Level Virtual Machine",
        key="llvm",
        is_tool=True,
        is_source=False,
        url_format="{protocol}://releases.llvm.org/{version}/"
                   "clang+llvm-{version}-{platform}.{extension}"
    ),

    lua=product_config(
        version=anthem_config_value("LUA_VERSION"),
        name="Lua",
        key="lua",
        is_tool=False,
        is_source=True,
        url_format="{protocol}://www.lua.org/ftp/lua-{version}.tar.gz"
    ),

    ninja=product_config(
        version=anthem_config_value("NINJA_VERSION"),
        name="Ninja",
        key="ninja",
        is_tool=True,
        is_source=False,
        github_data=github_config(
            owner="ninja-build",
            name="ninja",
            version_prefix="v",
            asset_data=platform_specific_asset(
                asset_file="ninja.zip",
                platform_files=platform_file_config(
                    darwin="ninja-mac.zip",
                    windows="ninja-win.zip",
                    linux="ninja-linux.zip"
                )
            )
        )
    ),

    ode=ode_anthem_config(
        version=anthem_config_value("ODE_VERSION"),
        name=anthem_config_value("ODE_NAME"),
        key=anthem_config_value("ODE_KEY"),
        opengl=Mapping(version=Mapping(
            major=anthem_config_value("ODE_OPENGL_MAJOR_VERSION"),
            minor=anthem_config_value("ODE_OPENGL_MINOR_VERSION"))),
        logger_name=anthem_config_value("ODE_LOGGER_NAME"),
        is_tool=False,
        is_source=True
    ),

    sdl=product_config(
        version=anthem_config_value("SDL_VERSION"),
        name="Simple DirectMedia Layer",
        key="sdl",
        is_tool=False,
        is_source=not platform.system() == "Windows",
        url_format="{protocol}://www.libsdl.org/release/"
                   "SDL2-{version}.{extension}",
        windows_format="{protocol}://www.libsdl.org/release/"
                       "SDL2-devel-{version}-{type}.{extension}"
    ),

    spdlog=product_config(
        version=anthem_config_value("SPDLOG_VERSION"),
        name="spdlog",
        key="spdlog",
        is_tool=False,
        is_source=True,
        build_subdir=os.path.join("include", "spdlog"),
        github_data=github_config(
            owner="gabime",
            name="spdlog",
            asset_data=SOURCE_ASSET,
            version_prefix="Version "
        )
    ),

    stb=product_config(
        version=anthem_config_value("STB_IMAGE_VERSION"),
        name="stb_image",
        key="stb_image",
        is_tool=False,
        is_source=True,
        master=True,
        github_data=github_config(
            owner="nothings",
            name="stb",
            asset_data=SOURCE_ASSET
        )
    )
)
