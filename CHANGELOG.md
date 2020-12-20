# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com), and this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- Documentation for the usage options of Couplet Composer to its repository.
- Command line option `--repository` for specifying the name of the repository directory of the project that is being built.
- Type hints to every method of the script.
- Support for determining custom module for dependency by using the key `module` and custom class in the module by using the key `class`.
- Support for determining the file used to check whether a dependency is installed by using the key `libraryFile`.

### Changed

- Internal application programming interface to use object based structure.
- Values for setting and checking the run mode into an enumeration.
- Values used in handling the operating system into an enumeration.
- Key for determining whether a dependency is built only when the tests are built to `testOnly`.
- Key for determining whether a dependency is built only when the benchmarks are built to `benchmarkOnly`.
- Name of the file containing the versions of the locally installed dependencies to start with a dot.

### Removed

- Support for the file `util/values.json` as the file that contains the data of the project that is being built.
- Support for the file `util/dependencies.json` as the file that contains the data of the depdencies for the project that is being built.
- Support for the usage of value `default` in `project.json` as the way to tell the script to use the shared version number for Ode or Anthem.
- Support for the field `version` in `project.json` for holding the value of the shared version number.
- Command line options `--ode-version` and `--anthem-version`.
- Support for using the key `testonly` to determine whether a dependency is built only when the tests are built.
- Support for using the key `benchmarkonly` to determine whether a dependency is built only when the benchmarks are built.

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

- Note about ending supporting Python 2.7 at some point in the future.

### Fixed

- Formatting of some entries in the changelog.

## [1.0.0-rc.1] - 2020-05-17

### Added

- Helper module for the dependencies’ `should_install` functions.

### Changed

- Structure of the function used to perform actions common to different runs of the scripts.
- Structure of the composing mode module to be split up into more functions.
- Two functions for copying Windows libraries in SDL dependency module into one.

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

- Support for the CMake option for indicating that the compilation of the binaries will be skipped.

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

- No changelog available.

## [0.10.2] - 2020-03-20

- No changelog available.

## [0.10.1] - 2020-03-20

- No changelog available.

## [0.10.0] - 2020-03-20

- No changelog available.

## [0.9.0] - 2020-03-18

- No changelog available.

## [0.8.0] - 2020-03-18

- No changelog available.

## [0.7.6] - 2020-03-15

- No changelog available.

## [0.7.5] - 2020-03-15

- No changelog available.

## [0.7.4] - 2020-03-15

- No changelog available.

## [0.7.3] - 2020-03-15

- No changelog available.

## [0.7.2] - 2020-03-15

- No changelog available.

## [0.7.1] - 2020-03-15

- No changelog available.

## [0.7.0] - 2020-03-15

- No changelog available.

## [0.6.0] - 2020-02-29

- No changelog available.

## [0.5.4] - 2020-02-16

- No changelog available.

## [0.5.3] - 2020-02-16

- No changelog available.

## [0.5.2] - 2020-02-16

- No changelog available.

## [0.5.1] - 2020-02-16

- No changelog available.

## [0.5.0] - 2020-02-15

- No changelog available.

## [0.4.5] - 2019-12-26

- No changelog available.

## [0.4.4] - 2019-12-26

- No changelog available.

## [0.4.3] - 2019-12-26

- No changelog available.

## [0.4.2] - 2019-12-26

- No changelog available.

## [0.4.1] - 2019-12-26

- No changelog available.

## [0.4.0] - 2019-12-26

- No changelog available.

## [0.4.0-rc.6] - 2019-12-26

- No changelog available.

## [0.4.0-rc.5] - 2019-12-26

- No changelog available.

## [0.4.0-rc.4] - 2019-12-26

- No changelog available.

## [0.4.0-rc.3] - 2019-12-26

- No changelog available.

## [0.4.0-rc.2] - 2019-12-25

- No changelog available.

## [0.4.0-rc.1] - 2019-12-25

- No changelog available.

## [0.3.0] - 2018-04-08

- No changelog available.

## [0.3.0-dev.16] - 2018-03-27

- No changelog available.

## [0.3.0-dev.15] - 2018-03-27

- No changelog available.

## [0.3.0-dev.14] - 2018-03-27

- No changelog available.

## [0.3.0-dev.13] - 2018-03-27

- No changelog available.

## [0.3.0-dev.12] - 2018-03-27

- No changelog available.

## [0.3.0-dev.11] - 2018-03-27

- No changelog available.

## [0.3.0-dev.10] - 2018-03-27

- No changelog available.

## [0.3.0-dev.9] - 2018-03-27

- No changelog available.

## [0.3.0-alpha.3] - 2018-03-27

- No changelog available.

## [0.3.0-alpha.2] - 2018-03-27

- No changelog available.

## [0.3.0-alpha.1] - 2018-03-27

- No changelog available.

## [0.3.0-dev.8] - 2018-03-27

- No changelog available.

## [0.3.0-dev.7] - 2018-03-27

- No changelog available.

## [0.3.0-dev.6] - 2018-03-26

- No changelog available.

## [0.3.0-dev.5] - 2018-03-26

- No changelog available.

## [0.3.0-dev.4] - 2018-03-26

- No changelog available.

## [0.3.0-dev.3] - 2018-03-26

- No changelog available.

## [0.3.0-dev.2] - 2018-03-26

- No changelog available.

## [0.3.0-dev.1] - 2018-03-26

- No changelog available.

## [0.2.5] - 2018-03-25

- No changelog available.

## [0.2.4] - 2018-03-25

- No changelog available.

## [0.2.3] - 2018-03-25

- No changelog available.

## [0.2.2] - 2018-03-25

- No changelog available.

## [0.2.1] - 2018-03-25

- No changelog available.

## [0.2.0] - 2018-03-25

- No changelog available.

## [0.1.0] - 2018-03-25

- No changelog available.

[unreleased]: https://github.com/anttikivi/couplet-composer/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/anttikivi/couplet-composer/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/anttikivi/couplet-composer/compare/v1.1.5...v1.2.0
[1.1.5]: https://github.com/anttikivi/couplet-composer/compare/v1.1.4...v1.1.5
[1.1.4]: https://github.com/anttikivi/couplet-composer/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/anttikivi/couplet-composer/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/anttikivi/couplet-composer/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/anttikivi/couplet-composer/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/anttikivi/couplet-composer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/anttikivi/couplet-composer/compare/v1.0.0-rc.1...v1.0.0
[1.0.0-rc.1]: https://github.com/anttikivi/couplet-composer/compare/v0.15.0...v1.0.0-rc.1
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
[0.5.0]: https://github.com/anttikivi/couplet-composer/compare/0.4.5...0.5.0
[0.4.5]: https://github.com/anttikivi/couplet-composer/compare/0.4.4...0.4.5
[0.4.4]: https://github.com/anttikivi/couplet-composer/compare/0.4.3...0.4.4
[0.4.3]: https://github.com/anttikivi/couplet-composer/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/anttikivi/couplet-composer/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/anttikivi/couplet-composer/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/anttikivi/couplet-composer/compare/0.4.0-rc.6...0.4.0
[0.4.0-rc.6]: https://github.com/anttikivi/couplet-composer/compare/0.4.0-rc.5...0.4.0-rc.6
[0.4.0-rc.5]: https://github.com/anttikivi/couplet-composer/compare/0.4.0-rc.4...0.4.0-rc.5
[0.4.0-rc.4]: https://github.com/anttikivi/couplet-composer/compare/0.4.0-rc.3...0.4.0-rc.4
[0.4.0-rc.3]: https://github.com/anttikivi/couplet-composer/compare/0.4.0-rc.2...0.4.0-rc.3
[0.4.0-rc.2]: https://github.com/anttikivi/couplet-composer/compare/0.4.0-rc.1...0.4.0-rc.2
[0.4.0-rc.1]: https://github.com/anttikivi/couplet-composer/compare/0.3.0...0.4.0-rc.1
[0.3.0]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.16...0.3.0
[0.3.0-dev.16]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.15...0.3.0-dev.16
[0.3.0-dev.15]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.14...0.3.0-dev.15
[0.3.0-dev.14]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.13...0.3.0-dev.14
[0.3.0-dev.13]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.12...0.3.0-dev.13
[0.3.0-dev.12]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.11...0.3.0-dev.12
[0.3.0-dev.11]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.10...0.3.0-dev.11
[0.3.0-dev.10]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.9...0.3.0-dev.10
[0.3.0-dev.9]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-alpha.3...0.3.0-dev.9
[0.3.0-alpha.3]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-alpha.2...0.3.0-alpha.3
[0.3.0-alpha.2]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-alpha.1...0.3.0-alpha.2
[0.3.0-alpha.1]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.8...0.3.0-alpha.1
[0.3.0-dev.8]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.7...0.3.0-dev.8
[0.3.0-dev.7]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.6...0.3.0-dev.7
[0.3.0-dev.6]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.5...0.3.0-dev.6
[0.3.0-dev.5]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.4...0.3.0-dev.5
[0.3.0-dev.4]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.3...0.3.0-dev.4
[0.3.0-dev.3]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.2...0.3.0-dev.3
[0.3.0-dev.2]: https://github.com/anttikivi/couplet-composer/compare/0.3.0-dev.1...0.3.0-dev.2
[0.3.0-dev.1]: https://github.com/anttikivi/couplet-composer/compare/0.2.5...0.3.0-dev.1
[0.2.5]: https://github.com/anttikivi/couplet-composer/compare/0.2.4...0.2.5
[0.2.4]: https://github.com/anttikivi/couplet-composer/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/anttikivi/couplet-composer/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/anttikivi/couplet-composer/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/anttikivi/couplet-composer/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/anttikivi/couplet-composer/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/anttikivi/couplet-composer/releases/tag/0.1.0
