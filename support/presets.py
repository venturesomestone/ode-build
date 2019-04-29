# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""This support module parses presets of the scripts."""

import sys

from absl import logging

if sys.version_info.major == 2:
    import ConfigParser as configparser
else:
    import configparser


def _load_preset_files_impl(preset_file_names, substitutions=None):
    if not substitutions:
        substitutions = {}
    # TODO SafeConfigParser is deprecated in Python 3.2. Instead,
    # you should use ConfigParser.
    config = configparser.SafeConfigParser(substitutions, allow_no_value=True)
    if config.read(preset_file_names) == []:
        logging.fatal(
            "The preset file isn't found (tried %s)",
            preset_file_names
        )
    return config


_PRESET_PREFIX = "preset: "


def _get_preset_options_impl(config, substitutions, preset_name):
    section_name = _PRESET_PREFIX + preset_name
    if section_name not in config.sections():
        return (None, None, None)
    build_script_opts = []
    build_script_impl_opts = []
    missing_opts = []
    dash_dash_seen = False
    for o in config.options(section_name):
        try:
            a = config.get(section_name, o)
        except configparser.InterpolationMissingOptionError as e:
            # e.reference contains the correctly formatted
            # option.
            missing_opts.append(e.reference)
            continue
        if not a:
            a = ""
        if substitutions:
            if o in substitutions:
                continue
        opt = None
        if o == "mixin-preset":
            # Split on newlines and filter out empty lines.
            mixins = filter(None, [m.strip() for m in a.splitlines()])
            for mixin in mixins:
                (base_build_script_opts,
                 base_build_script_impl_opts,
                 base_missing_opts) = \
                    _get_preset_options_impl(config, substitutions, mixin)
                build_script_opts += base_build_script_opts
                build_script_impl_opts += base_build_script_impl_opts
                missing_opts += base_missing_opts
        elif o == "dash-dash":
            dash_dash_seen = True
        elif a == "":
            opt = "--" + o
        else:
            opt = "--" + o + "=" + a
        if opt:
            if not dash_dash_seen:
                build_script_opts.append(opt)
            else:
                build_script_impl_opts.append(opt)
    return (build_script_opts, build_script_impl_opts, missing_opts)


def get_preset_options(substitutions, preset_file_names, preset_name):
    """Gets the options in a preset."""
    if substitutions:
        config = _load_preset_files_impl(preset_file_names, substitutions)
    else:
        config = _load_preset_files_impl(preset_file_names)

    build_script_opts, build_script_impl_opts, missing_opts = \
        _get_preset_options_impl(config, substitutions, preset_name)
    if not build_script_opts and not build_script_impl_opts:
        logging.fatal("Preset '%s' isn't found", preset_name)
    if missing_opts:
        logging.fatal(
            "Missing option(s) for preset '%s': %s",
            preset_name,
            ", ".join(missing_opts)
        )
    return build_script_opts + ["--"] + build_script_impl_opts


def get_all_preset_names(preset_file_names):
    """Gets the names of the presets in a preset file."""
    config = _load_preset_files_impl(preset_file_names)
    return [name[len(_PRESET_PREFIX):] for name in config.sections()
            if name.startswith(_PRESET_PREFIX)]
