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

"""This support module has common binary related utilities."""

import os
import platform

from support import data

from . import diagnostics, shell


def exist(component, path):
    """Check if the binary for the product exists."""
    if os.path.exists(os.path.join(data.session.shared_build_dir, path)):
        diagnostics.debug_note(
            "{} is already built and should not be re-built".format(
                component.repr
            )
        )
        return True
    return False


def ninja(target=None, env=None):
    """Call Ninja."""
    if target:
        if isinstance(target, list):
            ninja_call = [data.session.toolchain.ninja]
            ninja_call += target
            ninja_call += ["-j"]
            ninja_call += [str(data.session.args.build_jobs)]
            shell.call(ninja_call, env=env)
        else:
            shell.call([
                data.session.toolchain.ninja,
                target,
                "-j",
                str(data.session.args.build_jobs)
            ], env=env)
    else:
        shell.call([
            data.session.toolchain.ninja,
            "-j",
            str(data.session.args.build_jobs)
        ], env=env)


def make(target=None, build_args=None, env=None, xvfb=False):
    """Call Make."""
    if xvfb and data.session.args.enable_xvfb:
        call = [data.session.toolchain.xvfb_run]
        call += ["--server-args"]
        call += ["-screen 0 1920x1080x24"]
        call += ["-e"]
        call += ["/dev/stdout"]
        call += ["-a"]
        call += [data.session.toolchain.make]
    else:
        call = [data.session.toolchain.make]
    if target:
        if isinstance(target, list):
            call += target
        else:
            call += [target]
    if build_args:
        if isinstance(build_args, list):
            call += build_args
        else:
            call += [build_args]
    # call += ["-j"]
    # call += [str(data.session.args.build_jobs)]
    shell.call(call, env=env)


def msbuild(args, target=None, env=None, dry_run=None, echo=False):
    """Call MSBuild."""
    call_command = [data.session.toolchain.msbuild]
    call_command += args
    if target:
        call_command += ["/target:{}".format(target)]
    shell.call(call_command, env=env, dry_run=dry_run, echo=echo)


def compile(
    component,
    build_directory,
    make_targets=None,
    install_targets=None,
    solution_name=None
):
    """
    Compiles the binary from source code with CMake-generated
    build scripts.
    """
    args = data.session.args
    use_ninja = \
        args.cmake_generator == "Ninja" or args.cmake_generator == "Xcode"

    with shell.pushd(build_directory):
        # TODO MSBuild
        if use_ninja:
            if make_targets:
                ninja(make_targets)
            else:
                ninja()
            if install_targets:
                ninja(install_targets)
            else:
                ninja("install")
        elif args.cmake_generator == "Unix Makefiles":
            if make_targets:
                make(make_targets)
            else:
                make()
            if install_targets:
                make(install_targets)
            else:
                make(target="install")
        elif data.session.visual_studio:
            if solution_name is None:
                msbuild_args = ["{}.sln".format(component.key)]
            else:
                msbuild_args = ["{}.sln".format(solution_name)]

            if args.msbuild_logger is not None:
                msbuild_args += ["/logger:{}".format(args.msbuild_logger)]

            # msbuild_args += ["/property:Configuration={}".format(
            #     args.ode_build_variant if not build_type else build_type)]
            msbuild_args += [
                "/property:Configuration={}".format(args.ode_build_variant)
            ]

            if platform.system() == "Windows":
                msbuild_args += ["/property:Platform=Win32"]

            msbuild(msbuild_args)
