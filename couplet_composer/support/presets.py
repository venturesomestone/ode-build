# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem project.
#
# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License
#
# ------------------------------------------------------------- #

"""This support module parses presets of the scripts."""

import logging
import sys

if sys.version_info.major == 2:
    import ConfigParser as configparser
else:
    import configparser


def _create_configuration_parser(substitutions=None):
    """
    Creates the configuration parser for parsing the preset
    files.

    substitutions -- The values that should override the
    arguments in the preset files. The substitutions are
    currently disabled.
    """
    substitute_values = {} if not substitutions else substitutions
    return configparser.ConfigParser(substitute_values, allow_no_value=True)


def get_mixin_option_name():
    """
    Gives the name of the option that provides mix-in preset.
    """
    return "mix-in-preset"


def get_dash_dash_option_name():
    """
    Gives the name of the option that acts as the double dash.
    """
    return "dash-dash"


def _read_preset(parser, name, substitutions=None):
    """
    Reads the options from the given preset loaded into the
    configuration parser.

    Returns three values: the first one is a dictionary
    containing the names of the preset options and the values
    associated with them, the second one is a dictionary
    containing the names of the preset options and the values
    associated with them that are given after the double dash,
    and the third one contains a list of the erroneous options.

    parser -- The parser from which the preset options are read.

    name -- The name of the preset.

    substitutions -- The values that should override the
    arguments in the preset files. The substitutions are
    currently disabled.
    """
    if name not in parser.sections():
        return None

    # The variables inside the function are often modified but
    # the changing state isn't exposed to the scope outside the
    # function.
    options = {}
    options_after_end = {}
    missing_options = []
    dash_dash_seen = False

    for option in parser.options(name):
        value = None

        try:
            value = parser.get(section=name, option=option)
        except configparser.InterpolationMissingOptionError as e:
            # e.reference contains the correctly formatted
            # option.
            missing_options.append(e.reference)

        if substitutions and option in substitutions:
            # TODO Substitute the value
            pass

        if option == get_mixin_option_name():
            # Multiple mix-in presets are allowed in one option.
            mixins = [mixin.strip() for mixin in value.splitlines()]

            for mixin in mixins:
                (mixin_options,
                 mixin_options_after_end,
                 missing_mixin_options) = _read_preset(
                    parser=parser,
                    name=mixin,
                    substitutions=substitutions
                )
                options.update(mixin_options)
                options_after_end.update(mixin_options_after_end)
                missing_options.extend(missing_mixin_options)

        elif option == get_dash_dash_option_name():
            dash_dash_seen = True
        else:
            pair_to_add = {option: value}
            if dash_dash_seen:
                options_after_end.update(pair_to_add)
            else:
                options.update(pair_to_add)

    return options, options_after_end, missing_options


def get_preset_options(preset_file_names, preset_name, substitutions=None):
    """
    Gets the options in the given preset. This function isn't
    pure as it reads the given preset files.

    Returns two values: the first one is a dictionary containing
    the names of the preset options and the values associated
    with them and the second one is a dictionary containing the
    names of the preset options and the values associated with
    them that are given after the double dash.

    preset_file_names -- The files from which the presets are
    read.

    preset_name -- The name of the preset that is read.

    substitutions -- The values that should override the
    arguments in the preset files. The substitutions are
    currently disabled.
    """
    config_parser = _create_configuration_parser(substitutions=substitutions)

    files_read = config_parser.read(preset_file_names)

    if files_read == []:
        logging.warning(
            "The preset files aren't found (tried %s)",
            preset_file_names
        )
        return []

    options, options_after_end, missing_options = _read_preset(
        parser=config_parser,
        name=preset_name,
        substitutions=substitutions
    )

    if not options and not options_after_end:
        logging.warning("No options were found for preset '%s'", preset_name)

    if missing_options:
        logging.warning(
            "The missing options for preset '%s': %s",
            preset_name,
            ", ".join(missing_options)
        )

    return options, options_after_end


def get_all_preset_names(preset_file_names):
    """
    Gets the names of the presets in a preset file. This function
    isn't pure as it reads the given preset files.

    preset_file_names -- The files from which the presets are
    read.
    """
    config_parser = _create_configuration_parser()
    files_read = config_parser.read(preset_file_names)
    if files_read == []:
        logging.warning(
            "The preset files aren't found (tried %s)",
            preset_file_names
        )
        return []
    return config_parser.sections()
