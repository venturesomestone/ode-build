# Configuring Couplet Composer

Couplet Composer is the tool used to set up, configure, and run the build of [Obliging Ode and Unsung Anthem](https://github.com/anttikivi/unsung-anthem) and as such. There are many different options for configuring Couplet Composer and this file contains the documentation for all of the supported options.

Please note that this documentation is only for the different options of Couplet Composer. For more detailed instructions on how to build Obliging Ode and Unsung Anthem, refer to their [documentation on building the project](https://github.com/anttikivi/unsung-anthem/blob/develop/docs/BUILDING.md).

#### Table of Contents

[Configuring the Build](#configuring-the-build)

[Command Line Options](#command-line-options)
- [Common Top-level Options](#common-top-level-options)
  - [Special Options](#special-options)
  - [Top-level Options](#top-level-options)
- [Common Options](#common-options)
  - [Build Target Options](#build-target-options)
- [Preset Mode Options](#preset-mode-options)

[Project Configuration File](#project-configuration-file)
- [Dependencies](#dependencies)
  - [`id.files`](#idfiles)
  - [`id.platforms`](#idplatforms)

## Configuring the Build

Couplet Composer and the build of Obliging Ode and Unsung Anthem can naturally be configured by using vast selection of command line options. While it is possible to use only traditional command line arguments, the *recommended* way to configure the builds is to use so called **preset mode** of Couplet Composer.

In preset mode, the command line only specifies the preset name. The actual options come from the selected preset in `util/composer-presets.ini`. For example, if you want to run the generic developer build, your configuring mode call looks something like this:

    ./configure preset --name dev

and you composing mode call looks something like this:

    ./compose preset --name dev

On Windows the calls should of course use the Window batch file script variants.

If you take a look into `util/composer-presets.ini` in Obliging Ode and Unsung Anthem, you can see how the preset is specified in the preset file.

    $ cat > ./unsung-anthem/util/composer-presets.ini
    ...
    [dev]
    test
    benchmark
    debug
    ninja

    [compose:dev]
    developer-build
    ...

First of all, only so called long names of the options should be used instead of the short, one-character variants. Each line below the names of the presets represent one option. If the command line option takes a value, it’s given in the following form: `option=value`.

You must give the options that are common to both configuring and composing mode below the simple name of the preset, in this case `[dev]`. However, some options are exclusive to either configuring or composing mode. You must give those options below the titles that have the name of the mode (either `configure:` or `compose:`) before the name of the preset. In this case, the options of the preset named `dev` that are exclusive to the composing mode are given below the title `[compose:dev]`.

To find out more about the command line options, please read more in the section [Command Line Options](#command-line-options).

You can also use your own local files containing presets for Couplet Composer. To add a path to the list of files from which Couplet Composer looks for preset, use the `--file` option.

    ./compose preset --file /path/to/my/file/presets.ini --name some_preset

You can specify the `--file` option multiple times to add more paths to the list of files.

## Command Line Options

### Common Top-level Options

These options can be used in all modes and should be added to presets sparingly. If you use these options as normal command line options when invoking Couplet Composer in preset mode, these will be passed through to the actual invocation of the script even though they’re not specified in the preset.

#### Special Options

**`-h`**, **`--help`**

Shows the help message of Couplet Composer and exits.

**`-v`**, **`--version`**

Shows the version of Couplet Composer and exits.

#### Top-level Options

**`-n`**, **`--dry-run`**

Makes Couplet Composer run so that it only prints the commands that would be run but doesn’t actually run them.

**`-j INTEGER`**, **`--jobs INTEGER`**

Specifies the maximum number of parallel builds jobs Couplet Composer uses.

**`-c`**, **`--clean`**

Cleans the build environment before the build.

**`--verbose`**

Prints debug-level logging output.

**`--repository REPOSITORY`**

Uses the specified string as the name of the local directory in which the repository of Obliging Ode and Unsung Anthem is. The default value is `unsung-anthem`.

### Common Options

These options are common to both configuring mode and composing mode but cannot be specified through command line in preset mode.

#### Build Target Options

Please note that this functionality is still under development.

**`--host-target TARGET`**

Builds the binaries for the specified host target. The host target is resolved automatically by default.

### Preset Mode Options

These options can only be used through command line in preset mode.

**`--file PATH`**

Adds a path to the list of files from which Couplet Composer looks for the presets. You can use this options multiple times to add more paths to the list.

**`--name PRESET`**

Uses the given preset.

**`--show`**

Shows the available presets in the preset files and exits.

**`--expand-script-invocation`**

Prints the build script invocation composed from the preset given using `--name` and exits without running it.

## Project Configuration File

### Dependencies

#### `id.files`

The `files` object contains the files and folders that are checked for when determining whether the script should install the dependency. It also gives information how the script should copy the files from the original project to the local dependencies folder.

There are two ways to give the paths of individual files or folders. First one is to include the so-called category directory name of the file in the path, for example `include` in `include/header.h`. The second one is to have the files grouped by their so-called category directory name. Then the directory name is a key in the `files` object and the value for that key contains the names of the files or the objects for the files in the directory.

```json
{
  "dependencies": {
    "id": {
      "files": ["include/header.h", "lib/liblibrary.a", "lib/liblibraryd.a"]
    }
  }
}
```

```json
{
  "dependencies": {
    "id": {
      "files": {
        "include": "header.h",
        "lib": ["liblibrary.a", "liblibraryd.a"]
      }
    }
  }
}
```

If a category has only one file in it, you can give it as a string instead of a list with a single string in it. For multiple files, you have to use a list.

```json
{
  "dependencies": {
    "id": {
      "files": {
        "lib": "liblibrary.a"
      }
    }
  }
}
```

```json
{
  "dependencies": {
    "id": {
      "files": {
        "lib": ["liblibrary.a", "liblibraryd.a"]
      }
    }
  }
}
```

If the script can’t install some file by using its build script, you can give the file as an object. The object should contain both the source file that needs to be copied and the destination file where the file should be copied to. The source file is always relative to the root directory of the dependency project. The destination files are always relative to the local dependencies directory. If you define files only as strings and not objects for a dependency that the script doesn’t build to binary but copies for example header files, the script uses the relative file path given as both the source file and the destination file. When you use an object with the source and destination defined, only the destination file uses the directory from the key.

```json
{
  "dependencies": {
    "id": {
      "files": {
        "include": {
          "src": "header.h",
          "dest": "header.h"
        }
      }
    }
  }
}
```

#### `id.platforms`
