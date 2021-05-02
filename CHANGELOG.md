# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com), and this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- Documentation for the usage options of Couplet Composer to its repository.
- Command line option `--repository` for specifying the name of the repository directory of the project that is being built.
- Type hints to every method of the script.
- Support for determining custom module for dependency by using the key `module` and custom class in the module by using the key `className`.
- Support for determining the files used to check whether a dependency is installed by using the key `files`.
- Support for specifying the files and directories to copy and check for in different directories by using the names of the dependency directories (`bin`, `include`, `lib`, `src`, etc.) as keys for files or file arrays in the value object in `files`.
- Support for specifying both the source file and destination file when the installation of the dependency requires copying files.
- Support for determining the asset file that should be downloaded for a dependency by using the key `asset`.
- Support for determining the [GitHub](https://github.com) repository of a dependency by using the key `repo`.
- Runner for each target and cross-compile target so that the script is run for every added target.
- Version and name CMake options automatically for each subproject.
- Colours to command line output that depends on the logging level of the message.
- More informative logging format to the command line output.
- Ability to add platform-dependant file configurations for the dependencies.
- Support for adding CMake commands in `product.json` with the key `cmakeOptions`.
- Command line option `--cmake-options` for adding CMake options.
- Support for passing the CMake option `COMPOSER_BUILD_TEST`.
- Support for passing the CMake option `COMPOSER_BUILD_BENCHMARK`.
- Support for passing the CMake option `COMPOSER_BUILD_DOCS`.
- Support for passing the CMake option `COMPOSER_CODE_COVERAGE`.
- Support for passing the CMake option `COMPOSER_CPP_STD`.
- Support for passing the CMake option `COMPOSER_LOCAL_PREFIX`.
- Support for passing the CMake option `COMPOSER_OPENGL_VERSION_MAJOR`.
- Support for passing the CMake option `COMPOSER_OPENGL_VERSION_MINOR`.
- Support for passing the CMake option `COMPOSER_name_VERSION` where `name` is the name of a supported project.
- Support for passing the CMake option `COMPOSER_name_NAME` where `name` is the name of a supported project.
- Support for passing option lists from the presets.
- Command line option `--verbose` and `-V` to print debugging output.

### Changed

- Internal application programming interface to use object based structure.
- Values for setting and checking the run mode into an enumeration.
- Values used in handling the operating system into an enumeration.
- Key for determining whether a dependency is built only when the tests are built to `testOnly`.
- Key for determining whether a dependency is built only when the benchmarks are built to `benchmarkOnly`.
- Name of the file containing the versions of the locally installed dependencies to start with a dot.
- Utility functions for modifying archives to a single methods that does different actions depending on arguments.
- Toolchain to install the tools in a ‘lazy’ manner so that a tool is installed only when it’s actually required.

### Removed

- Support for the file `util/values.json` as the file that contains the data of the project that is being built.
- Support for the file `util/dependencies.json` as the file that contains the data of the depdencies for the project that is being built.
- Support for the usage of value `default` in `project.json` as the way to tell the script to use the shared version number for Ode or Anthem.
- Support for the field `version` in `project.json` for holding the value of the shared version number.
- Command line options `--ode-version` and `--anthem-version`.
- Support for using the key `testonly` to determine whether a dependency is built only when the tests are built.
- Support for using the key `benchmarkonly` to determine whether a dependency is built only when the benchmarks are built.
- Dependency on `distro`.
- `ODE_BUILD_TEST` as it is replaced by `COMPOSER_BUILD_TEST`.
- `ODE_TEST_BENCHMARKING` as it is replaced by `COMPOSER_BUILD_BENCHMARK`.
- `ODE_BUILD_DOCS` as it is replaced by `COMPOSER_BUILD_DOCS`.
- `ODE_CODE_COVERAGE` as it is replaced by `COMPOSER_CODE_COVERAGE`.
- `ODE_CXX_VERSION` as it is replaced by `COMPOSER_CPP_STD`.
- `ODE_DEPENDENCY_PREFIX` as it is replaced by `COMPOSER_LOCAL_PREFIX`.
- `ODE_OPENGL_VERSION_MAJOR` as it is replaced by `COMPOSER_OPENGL_VERSION_MAJOR`.
- `ODE_OPENGL_VERSION_MINOR` as it is replaced by `COMPOSER_OPENGL_VERSION_MINOR`.
- `ODE_VERSION` as it is replaced by `COMPOSER_ODE_VERSION`.
- `ANTHEM_VERSION` as it is replaced by `COMPOSER_ANTHEM_VERSION`.
- `ODE_NAME` as it is replaced by `COMPOSER_ODE_NAME`.
- `ANTHEM_NAME` as it is replaced by `COMPOSER_ANTHEM_NAME`.
- `ODE_DEVELOPER` as it is removed.
- `ODE_BUILD_STATIC` as it is removed.
- `ODE_BUILD_SHARED` as it is removed.
- `ANTHEM_BUILD_STATIC` as it is removed.
- `ANTHEM_BUILD_SHARED` as it is removed.
- `ODE_TEST_USE_NULL_SINK` as it is removed.
- `ODE_DISABLE_GL_CALLS` as it is removed.
- `ODE_SCRIPTS_BASE_DIRECTORY` as it is removed.
- Command line option `--in-tree-build` as support for builds in tree is removed.
- Command line argument `--coverage` and support for creating code coverage reports.
- Command line argument `--print-debug`.
- Command line arguments `--github-auth-file`, `--github-user-agent`, and `--github-api-token`.
- Command line arguments `--compiler-toolchain`, `--clang`, `--gcc`, `--msvc`, `--compiler-version`, `--host-cc`, `--host-cxx`, `--host-compiler`, `--host-msbuild`, `--clang-tidy-binary`, `--clang-apply-replacements-binary`, and `--enable-xvfb`.
- Command line argument `--opengl-version`.
- Command line arguments `--ode-static-lib`, `--ode-shared-lib`, `--anthem-static-lib`, `--anthem-shared-lib`, and `--skip-build`.
- Command line argument `--export-linter-fixes`.
- Command line argument `--use-artefact-directory`.
- Command line arguments `--ode-binaries-name`, `--anthem-binaries-name`, `--anthem-artefacts-name`, and `--anthem-artifacts-name`.
- Command line arguments `--assertions` and `--no-assertions`.
- Command line argument `--developer-build`.
- Command line argument `--test-logging`.

## [1.9.0] - 2021-05-02

### Deprecated

- Command line argument `--coverage`.
- Python versions older than 3.6.

## [1.8.0] - 2021-04-12

### Deprecated

- Command line argument `--print-debug` as it will be replaced by `--verbose`.
- Command line argument `--in-tree-build` as it will be removed in the next major version.
- Command line arguments `--github-auth-file`, `--github-user-agent`, and `--github-api-token` as they’ll become obsolete in the next major version.
- Command line arguments `--compiler-toolchain`, `--clang`, `--gcc`, `--msvc`, `--compiler-version`, `--host-cc`, `--host-cxx`, `--host-compiler`, `--host-msbuild`, `--clang-tidy-binary`, `--clang-apply-replacements-binary`, and `--enable-xvfb` as they’ll become obsolete in the next major version.
- Command line argument `--opengl-version` as it will be replaced by a value in `product.json`.
- Command line arguments `--ode-static-lib`, `--ode-shared-lib`, `--anthem-static-lib`, `--anthem-shared-lib`, and `--skip-build` as they’ll become obsolete in the next major version.
- Command line argument `--export-linter-fixes` as it will be removed in the next major version.
- Command line argument `--use-artefact-directory` as it will be removed in the next major version.
- Command line arguments `--ode-binaries-name`, `--anthem-binaries-name`, `--anthem-artefacts-name`, and `--anthem-artifacts-name` as they’ll become obsolete in the next major version.
- Command line arguments `--assertions` and `--no-assertions` as they will be removed in the next major version.
- Command line argument `--developer-build` as it will be removed in the next major version.
- Command line argument `--test-logging` as it will be removed in the next major version.

## [1.7.6] - 2021-02-28

### Fixed

- Changelog links for `v1.7.5`.

## [1.7.5] - 2021-02-28

### Changed

- Google Test to use the out-of-tree sources on Windows.

## [1.7.4] - 2021-02-28

### Fixed

- Typo in the Google Test module return value.

## [1.7.3] - 2021-02-28

### Removed

- Google Test sources being added as a subdirectory.

## [1.7.2] - 2021-02-27

### Fixed

- Reading the SDL version when copying the library files after the build.

## [1.7.1] - 2021-02-27

### Added

- List of the requirements to the manifest file.

## [1.7.0] - 2021-02-27

### Fixed

- Command for uploading releases to the Python Package Index.

## [1.6.0] - 2021-02-27

### Fixed

- Command for uploading releases to the Python Package Index.

## [1.5.0] - 2021-02-26

### Added

- Version data to the `__version__.py` module.
- Support for installing the project from the Python Package Index.

### Changed

- Warning about the end of the Python 2.7 to tell the exact version of Couplet Composer.
- Arguments parser to parse only known arguments so that `pipenv` arguments don’t cause errors.

### Deprecated

- `ODE_BUILD_TEST` as it will be replaced by `COMPOSER_BUILD_TEST` in the next major version.
- `ODE_TEST_BENCHMARKING` as it will be replaced by `COMPOSER_BUILD_BENCHMARK` in the next major version.
- `ODE_BUILD_DOCS` as it will be replaced by `COMPOSER_BUILD_DOCS` in the next major version.
- `ODE_CODE_COVERAGE` as it will be replaced by `COMPOSER_CODE_COVERAGE` in the next major version.
- `ODE_DEVELOPER` as it will be replaced by `COMPOSER_DEVELOPER` in the next major version.
- `ODE_CXX_VERSION` as it will be replaced by `COMPOSER_CPP_STD` in the next major version.
- `ODE_DEPENDENCY_PREFIX` as it will be replaced by `COMPOSER_LOCAL_PREFIX` in the next major version.
- `ODE_OPENGL_VERSION_MAJOR` as it will be replaced by `COMPOSER_OPENGL_VERSION_MAJOR` in the next major version.
- `ODE_OPENGL_VERSION_MINOR` as it will be replaced by `COMPOSER_OPENGL_VERSION_MINOR` in the next major version.
- `ODE_VERSION` as it will be replaced by `COMPOSER_ODE_VERSION` in the next major version.
- `ANTHEM_VERSION` as it will be replaced by `COMPOSER_ANTHEM_VERSION` in the next major version.
- `ODE_NAME` as it will be replaced by `COMPOSER_ODE_NAME` in the next major version.
- `ANTHEM_NAME` as it will be replaced by `COMPOSER_ANTHEM_NAME` in the next major version.
- `ODE_DEVELOPER` as it will be removed in the next major version.
- `ODE_BUILD_STATIC` as it will be removed in the next major version.
- `ODE_BUILD_SHARED` as it will be removed in the next major version.
- `ANTHEM_BUILD_STATIC` as it will be removed in the next major version.
- `ANTHEM_BUILD_SHARED` as it will be removed in the next major version.
- `ODE_TEST_USE_NULL_SINK` as it will be removed in the next major version.
- `ODE_DISABLE_GL_CALLS` as it will be removed in the next major version.
- `ODE_SCRIPTS_BASE_DIRECTORY` as it will be removed in the next major version.

### Removed

- Text file where the script version was read from as it’s replaced by Python-only version resolving.

## [1.4.4] - 2021-01-29

### Fixed

- Link of the unreleased changes in the changelog.

## [1.4.3] - 2021-01-27

### Added

- Changelog entries for the older releases.

### Fixed

- Link of `v1.4.2` in the changelog.

## [1.4.2] - 2021-01-17

### Fixed

- Logical operator that caused error when checking the dependencies from `product.json`.

## [1.4.1] - 2021-01-17

### Fixed

- Wrong entries in `product.json` being read as dependencies.

## [1.4.0] - 2021-01-16

### Added

- Support for determining whether a dependency is built only when the tests are built by using the key `testOnly`.
- Support for determining whether a dependency is built only when the benchmarks are built by using the key `benchmarkOnly`.
- Support for providing both dependencies and project values in file `product.json`.

### Deprecated

- Usage of the key `testonly` for determining whether a dependency is built only when the tests are built.
- Usage of the key `benchmarkonly` for determining whether a dependency is built only when the benchmarks are built.
- Usage of the file `util/project.json` for providing information on the built project and its dependencies.

## [1.3.2] - 2020-12-18

### Fixed

- Missing argument when copying the SDL libraries.

## [1.3.1] - 2020-12-18

### Fixed

- Wrong call to dictionary's `items` function when creating the set of dependency data.

## [1.3.0] - 2020-12-18

### Added

- Support for providing both dependencies and project values in file `util/project.json`.
- Support for using value `shared` to indicate that either Ode or Anthem should use the shared version number from the project value file.
- Support for field `shared_version` to hold the value of the shared version number in the project value file.

### Deprecated

- Usage of value `default` in `values.json` and `project.json` as the way to tell the script to use the shared version number for Ode or Anthem.
- Field `version` in `values.json` and `project.json` for holding the value of the shared version number.
- Command line options `--ode-version` and `--anthem-version`.
- File `values.json` for providing information on the projects being built.
- File `dependencies.json` for providing information on the dependencies of the projects being built.

## [1.2.1] - 2020-09-12

### Fixed

- Import of missing function `get_project_version`.

## [1.2.0] - 2020-09-12

### Added

- Support for using one version number for both Obliging Ode and Unsung Anthem.

### Changed

- Version number from Python module to a text file.

### Deprecated

- Replacement of environment variables in the project versions.

## [1.1.5] - 2020-07-29

### Fixed

- Crash when environment variables contained entries with leading underscores.

## [1.1.4] - 2020-07-29

### Changed

- Replacement of the environment variables in the version strings to use named tuples to allow selecting the variable name with dot.

## [1.1.3] - 2020-07-29

### Added

- Logging to find out the name of the variable the script is trying to replace in the version string.

## [1.1.2] - 2020-07-29

### Fixed

- Missing links in the changelog.

## [1.1.1] - 2020-07-29

### Fixed

- Name of the environment variable missing from the default replacement dictionary for the versions of the projects.

## [1.1.0] - 2020-07-29

### Added

- Ability to use environment variables in the version of the project.

## [1.0.0] - 2020-07-27

### Added

- Helper module for the dependencies’ `should_install` functions.
- Note about ending supporting Python 2.7 at some point in the future.

### Changed

- Structure of the function used to perform actions common to different runs of the scripts.
- Structure of the composing mode module to be split up into more functions.
- Two functions for copying Windows libraries in SDL dependency module into one.

### Fixed

- Formatting of some entries in the changelog.

## [0.15.0] - 2020-05-13

### Added

- Support for generating code coverage data from the tests.
- Support for using X virtual frame buffer with the code coverage target.
- Installation of the Doxygen documentation to a directory for easier reading.

### Changed

- In-tree build to have all of the directories in tree.

### Fixed

- Lua trying to build for macOS on Linux when using Unix Makefiles build generator.

### Removed

- Command line options for setting the names of the loggers and windows of Obliging Ode and Unsung Anthem.
- Support for specifying the source root by using `$ODE_SOURCE_ROOT`.

## [0.14.7] - 2020-05-09

### Added

- Support for the CMake option for indicating that the compilation of the binaries is skipped.

## [0.14.6] - 2020-05-09

### Fixed

- Missing links in the changelog.

## [0.14.5] - 2020-05-09

### Fixed

- Script attempting to install binaries when the build is skipped.

## [0.14.4] - 2020-05-09

### Changed

- Printing of the Linux distribution at the beginning to be simpler.

## [0.14.3] - 2020-05-09

### Fixed

- Missing links in the changelog.

## [0.14.2] - 2020-05-09

### Fixed

- Host target option missing for printing the current system when running the script in preset mode.

## [0.14.1] - 2020-05-09

### Added

- Printing of the current platform at the beginning of the run.

### Fixed

- Check of the Linux distribution at the beginning of the LLVM installation.

## [0.14.0] - 2020-05-09

### Added

- Copying of launching scripts from the project directory to the destination directory.

## [0.13.4] - 2020-05-09

### Fixed

- Version [0.13.3] in the changelog.

## [0.13.3] - 2020-05-09

### Added

- Command line option to skip build.

### Changed

- Linter options’ location to the common options with other similar build options.

### Removed

- Option to only run the linter.

## [0.13.2] - 2020-05-09

### Changed

- Version of LLVM to 10.0.0.
- Downloads the LLVM to only support GitHub releases.
- Installation of clang-tidy to only happen when linter is actually needed.

## [0.13.1] - 2020-05-09

### Fixed

- Incorrect names and URLs of the LLVM assets.

## [0.13.0] - 2020-05-09

### Added

- Option to copy the build binaries to a directory instead of archiving them as it is useful on CI for example.
- Dependency on `distro` for resolving the Linux distribution for LLVM installation.
- Support installing the LLVM tools on macOS and Ubuntu if they are not found on the system.

### Changed

- Required parameters of the tool installation functions to one object instead of passing many different parameters.
- Required parameters of the dependency installation functions to one object instead of passing many different parameters.
- Version of Ninja to 1.10.0.
- All platform names to lower case.
- Build variant in the directory names to lower case.
- CMake generator in the directory names to lower case.

## [0.12.0] - 2020-04-25

### Added

- cxxotps as supported dependency.

### Removed

- Clara as supported dependency.

## [0.11.0] - 2020-04-19

### Added

- This changelog file for documenting changes to the project.
- Shell utility for changing file permissions.
- Support for linting Obliging Ode and Unsung Anthem with `clang-tidy`.
- Dependency on `PyYAML` for `clang-tidy` to be able to export diagnostics.
- Code of conduct and contributing guidelines.
- Templates for creating issues and pull requests and list of code owners for GitHub.

## [0.10.3] - 2020-04-13

### Changed

- File headers to match the new style.

## [0.10.2] - 2020-03-20

### Fixed

- Missing parameters from tool parameters.

## [0.10.1] - 2020-03-20

### Fixed

- Supposed tool data functions being values.

## [0.10.0] - 2020-03-20

### Added

- Support for building the documentation of the project if Doxygen is present.
- Command line option `--docs` for enabling the building of the documentation.

## [0.9.0] - 2020-03-18

### Changed

- To a simpler build directory structure.

## [0.8.0] - 2020-03-18

### Added

- Support for locally creating an installation of the project for running it.
- Support for creating archives of the project.
- Command line option `--anthem-artifacts-name` for specifying the name of the build artefact archives.
- Shell utilities for creating archives.

## [0.7.6] - 2020-03-15

### Fixed

- Incorrect set of choices for `--build-variant`.

## [0.7.5] - 2020-03-15

### Fixed

- Typo in the descriptions of `--github-user-agent` and `--github-api-token`.

## [0.7.4] - 2020-03-15

### Fixed

- Wrong variables used to check for GitHub API values.

## [0.7.3] - 2020-03-15

### Changed

- Value used for getting the GitHub API authorization file to a shorter variable.

## [0.7.2] - 2020-03-15

### Added

- Support for providing the command line option `--github-auth-file` in the preset mode.

## [0.7.1] - 2020-03-15

### Added

- Debug logging telling which version of the GitHub API is used.

## [0.7.0] - 2020-03-15

### Added

- Command line option `--github-auth-file` for specifying a file that contains GitHub access key.
- Support for building Google Benchamrks on Windows.
- Support for downloading the dependencies using the GitHub REST API when an access key isn’t provided.

## [0.6.0] - 2020-02-29

### Added

- Command line option `--test-logging` for enabling logging in the tests.
- Support for building runable Windows executables.
- Support for adding the Google Test sources to the main build for Windows.

## [0.5.4] - 2020-02-16

### Removed

- Unnecessary empty line.

## [0.5.3] - 2020-02-16

### Added

- Command line option `--host-msbuild` for manually defining the path to the MSBuild executable.

## [0.5.2] - 2020-02-16

### Fixed

- Capitalization of the searched MSBuild tool.

## [0.5.1] - 2020-02-16

### Added

- Support for creating tool data for MSVC.

## [0.5.0] - 2020-02-15

### Added

- Command line option for creating the project build in tree.
- Command line option `--msvc` for manually giving the path to the MSVC executable.
- Command line option `--host-compiler` for manually setting the path to a tool executable that should replace both `--host-cc` and `--host-cxx`.
- Command line option `--visual-studio-16` for using Visual Studio 16 as the CMake generator on Windows.

### Changed

- Warning about Python 2 to past tense.
- MSVC to be the default buildchain on Windows.
- Visual Studio 16 to be the default CMake generator on Windows.
- SDL build to use SDL’s own script and `make` to build it.
- Toolchain to be more easily extensible.

## [0.4.5] - 2019-12-26

### Added

- Utility for creating symbolic links.

### Fixed

- SDL symbolic links by creating them manually.

## [0.4.4] - 2019-12-26

### Fixed

- Erroneous index when copying SDL files on Linux.

## [0.4.3] - 2019-12-26

### Fixed

- SDL library files copied on Linux by copying all of the dynamic library files.

## [0.4.2] - 2019-12-26

### Fixed

- SDL library files copied on Linux by storing the SDL version and using it in the filename.

## [0.4.1] - 2019-12-26

### Fixed

- Name of the SDL dynamic library file on Linux.

## [0.4.0] - 2019-12-26

### Added

- Support for installing the project as a Python package.
- Commands `preset`, `configure`, and `compose` for selecting different steps of the build to run.
- Warning when using Python 2.
- Support for building Lua using a custom CMake script.
- stb_image as a dependency.
- Support for defining options only for configuring or composing mode in preset file.
- Unit tests.

### Changed

- Licence to MIT License.
- Project name to ‘Couplet Composer’.
- Project into three modes: preset, configure, and compose. Configuring mode sets up the build environment and builds and installs dependencies and composing mode builds the project. Preset mode can be used to run either configuring or composing mode with an options preset.
- Tools and dependencies into a new module format.

## [0.3.0] - 2018-04-08

### Added

- Command line options `--develop-script`, `--no-script-update`, and `--update-script` so they don’t cause errors as they are used by the helper script for running the build script.
- Command line option `--rpath` for setting the rpath.
- Command line option `--link-libc++` for manually forcing the linking of `libc++`.
- Command line option `--verbose-cmake` for enabling verbose CMake output.
- Command line option `--build-separate-benchmark-library` to force Google Benchmark be built separately from the rest of the project.
- Command line option `--log-tests` for enabling logger output from the tests of the project.
- Add a trace-level logging function that is always printed.
- Reflection for reading project values from a Python configuration of the project being built.
- Explicit support for copying symbolic links with the shell utility.
- Shell utility for listing all of the files in a directory.
- Support for building Google Test and Google Benchmark by copying the files to be added into the build by the CMake script of the project that is being built.
- Support for copying LLVM and SDL files to the correct directory according to the set rpath.
- Support for using environment variables in the projects’ version values.

### Changed

- SDL and LLVM library files to be copied one by one to avoid errors.

## [0.2.5] - 2018-03-25

### Fixed

- C++ standard library when using locally installed LLVM by manually linking `libc++`.

## [0.2.4] - 2018-03-25

### Changed

- CMake to be installed directory by directory to fix a copying error.

## [0.2.3] - 2018-03-25

### Added

- Support for downloading LLVM and using it instead of the LLVM on the system.
- Command line option `--build-llvm` for building LLVM.

## [0.2.2] - 2018-03-25

### Fixed

- Incorrect global script directory.

## [0.2.1] - 2018-03-25

### Fixed

- Incorrect script directory.

## [0.2.0] - 2018-03-25

### Removed

- Catch as the dependency for [Obliging Ode and Unsung Anthem](https://github.com/anttikivi/unsung-anthem).

## [0.1.0] - 2018-03-25

### Added

- Initial utility script for building [Obliging Ode and Unsung Anthem](https://github.com/anttikivi/unsung-anthem).

[unreleased]: https://github.com/anttikivi/couplet-composer/compare/v1.9.0...HEAD
[1.9.0]: https://github.com/anttikivi/couplet-composer/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/anttikivi/couplet-composer/compare/v1.7.6...v1.8.0
[1.7.6]: https://github.com/anttikivi/couplet-composer/compare/v1.7.5...v1.7.6
[1.7.5]: https://github.com/anttikivi/couplet-composer/compare/v1.7.4...v1.7.5
[1.7.4]: https://github.com/anttikivi/couplet-composer/compare/v1.7.3...v1.7.4
[1.7.3]: https://github.com/anttikivi/couplet-composer/compare/v1.7.2...v1.7.3
[1.7.2]: https://github.com/anttikivi/couplet-composer/compare/v1.7.1...v1.7.2
[1.7.1]: https://github.com/anttikivi/couplet-composer/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.com/anttikivi/couplet-composer/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/anttikivi/couplet-composer/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/anttikivi/couplet-composer/compare/v1.4.4...v1.5.0
[1.4.4]: https://github.com/anttikivi/couplet-composer/compare/v1.4.3...v1.4.4
[1.4.3]: https://github.com/anttikivi/couplet-composer/compare/v1.4.2...v1.4.3
[1.4.2]: https://github.com/anttikivi/couplet-composer/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/anttikivi/couplet-composer/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/anttikivi/couplet-composer/compare/v1.3.2...v1.4.0
[1.3.2]: https://github.com/anttikivi/couplet-composer/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/anttikivi/couplet-composer/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/anttikivi/couplet-composer/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/anttikivi/couplet-composer/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/anttikivi/couplet-composer/compare/v1.1.5...v1.2.0
[1.1.5]: https://github.com/anttikivi/couplet-composer/compare/v1.1.4...v1.1.5
[1.1.4]: https://github.com/anttikivi/couplet-composer/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/anttikivi/couplet-composer/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/anttikivi/couplet-composer/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/anttikivi/couplet-composer/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/anttikivi/couplet-composer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/anttikivi/couplet-composer/compare/v0.15.0...v1.0.0
[0.15.0]: https://github.com/anttikivi/couplet-composer/compare/v0.14.7...v0.15.0
[0.14.7]: https://github.com/anttikivi/couplet-composer/compare/v0.14.6...v0.14.7
[0.14.6]: https://github.com/anttikivi/couplet-composer/compare/v0.14.5...v0.14.6
[0.14.5]: https://github.com/anttikivi/couplet-composer/compare/v0.14.4...v0.14.5
[0.14.4]: https://github.com/anttikivi/couplet-composer/compare/v0.14.3...v0.14.4
[0.14.3]: https://github.com/anttikivi/couplet-composer/compare/v0.14.2...v0.14.3
[0.14.2]: https://github.com/anttikivi/couplet-composer/compare/v0.14.1...v0.14.2
[0.14.1]: https://github.com/anttikivi/couplet-composer/compare/v0.14.0...v0.14.1
[0.14.0]: https://github.com/anttikivi/couplet-composer/compare/v0.13.4...v0.14.0
[0.13.4]: https://github.com/anttikivi/couplet-composer/compare/v0.13.3...v0.13.4
[0.13.3]: https://github.com/anttikivi/couplet-composer/compare/v0.13.2...v0.13.3
[0.13.2]: https://github.com/anttikivi/couplet-composer/compare/v0.13.1...v0.13.2
[0.13.1]: https://github.com/anttikivi/couplet-composer/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/anttikivi/couplet-composer/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/anttikivi/couplet-composer/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/anttikivi/couplet-composer/compare/v0.10.3...v0.11.0
[0.10.3]: https://github.com/anttikivi/couplet-composer/compare/v0.10.2...v0.10.3
[0.10.2]: https://github.com/anttikivi/couplet-composer/compare/v0.10.1...v0.10.2
[0.10.1]: https://github.com/anttikivi/couplet-composer/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/anttikivi/couplet-composer/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/anttikivi/couplet-composer/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/anttikivi/couplet-composer/compare/v0.7.6...v0.8.0
[0.7.6]: https://github.com/anttikivi/couplet-composer/compare/v0.7.5...v0.7.6
[0.7.5]: https://github.com/anttikivi/couplet-composer/compare/v0.7.4...v0.7.5
[0.7.4]: https://github.com/anttikivi/couplet-composer/compare/v0.7.3...v0.7.4
[0.7.3]: https://github.com/anttikivi/couplet-composer/compare/v0.7.2...v0.7.3
[0.7.2]: https://github.com/anttikivi/couplet-composer/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/anttikivi/couplet-composer/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/anttikivi/couplet-composer/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/anttikivi/couplet-composer/compare/v0.5.4...v0.6.0
[0.5.4]: https://github.com/anttikivi/couplet-composer/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/anttikivi/couplet-composer/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/anttikivi/couplet-composer/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/anttikivi/couplet-composer/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/anttikivi/couplet-composer/compare/0.4.5...v0.5.0
[0.4.5]: https://github.com/anttikivi/couplet-composer/compare/0.4.4...0.4.5
[0.4.4]: https://github.com/anttikivi/couplet-composer/compare/0.4.3...0.4.4
[0.4.3]: https://github.com/anttikivi/couplet-composer/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/anttikivi/couplet-composer/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/anttikivi/couplet-composer/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/anttikivi/couplet-composer/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/anttikivi/couplet-composer/compare/0.2.5...0.3.0
[0.2.5]: https://github.com/anttikivi/couplet-composer/compare/0.2.4...0.2.5
[0.2.4]: https://github.com/anttikivi/couplet-composer/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/anttikivi/couplet-composer/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/anttikivi/couplet-composer/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/anttikivi/couplet-composer/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/anttikivi/couplet-composer/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/anttikivi/couplet-composer/releases/tag/0.1.0
