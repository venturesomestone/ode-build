# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the class for the objects that run the
composing run mode of the build script.
"""

import os

from .runner_proper import RunnerProper


class ComposingRunner(RunnerProper):
    """A class for creating callable objects that represent the
    composing mode runners of the build script.
    """

    def __call__(self) -> int:
        """Runs the run mode of this runner.

        Returns:
            An 'int' that is equal to the exit code of the run.
        """
        super().__call__()

        cmake_call = [
            self.toolchain.cmake,
            os.path.join(
                self.invocation.source_root,
                self.invocation.args.repository
            ),
            "-G",
            self.invocation.cmake_generator.value,
            "-DCMAKE_BUILD_TYPE={}".format(
                self.invocation.build_variant.value
            ),
            "-DCMAKE_INSTALL_PREFIX={}".format(
                self.build_dir.destination.replace(os.path.sep, "/")
            ),
            "-DCOMPOSER_BUILD_TEST={}".format(
                "ON" if self.invocation.args.build_test else "OFF"
            ),
            "-DCOMPOSER_BUILD_BENCHMARK={}".format(
                "ON" if self.invocation.args.build_benchmark else "OFF"
            ),
            "-DCOMPOSER_BUILD_DOCS={}".format(
                "ON" if self.invocation.args.build_docs else "OFF"  # TODO Also check that Doxygen is found
            ),
            "-DCOMPOSER_CODE_COVERAGE={}".format(
                "ON" if self.invocation.args.coverage else "OFF"
            ),
            "-DCOMPOSER_DEVELOPER={}".format(
                "ON" if self.invocation.args.developer_build else "OFF"
            ),
            "-DCOMPOSER_CXX_STD={}".format(self.invocation.args.std.value),
            "-DCOMPOSER_LOCAL_PREFIX={}".format(
                self.build_dir.dependencies.replace(os.path.sep, "/")
            ),
            "-DCOMPOSER_OPENGL_VERSION_MAJOR={}".format(
                self.invocation.project.gl_version.split(".")[0]
            ),
            "-DCOMPOSER_OPENGL_VERSION_MINOR={}".format(
                self.invocation.project.gl_version.split(".")[1]
            )
        ]

        for key in self.invocation.project.project_keys:
            cmake_call.append("-DCOMPOSER_{}_VERSION={}".format(
                key.upper(),
                getattr(self.invocation.project, "{}_version".format(key))
            ))
            cmake_call.append("-DCOMPOSER_{}_NAME={}".format(
                key.upper(),
                getattr(self.invocation.project, "{}_name".format(key))
            ))

        return 0
