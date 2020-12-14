# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A support module that contains helper functions for parsing
and displaying the presets.
"""

import configparser
import logging
import sys

from typing import List, Tuple

from .run_mode import RunMode


CONFIGURATION_PRESET_PREFIX = "{}:".format(RunMode.configure.value)
COMPOSING_PRESET_PREFIX = "{}:".format(RunMode.compose.value)

_MIXIN_OPTION = "mix-in-preset"
_DASH_DASH_OPTION = "dash-dash"


def _create_configuration_parser(
    substitutions: dict = None
) -> configparser.ConfigParser:
    """Creates the configuration parser for parsing the preset
    files.

    Args:
        substitutions (dict): The values that should override the
            arguments in the preset files. The substitutions are
            currently disabled.

    Returns:
        An object of the type ConfigParser.
    """
    substitute_values = {} if not substitutions else substitutions
    return configparser.ConfigParser(substitute_values, allow_no_value=True)


def _read_preset(
    parser: configparser.ConfigParser,
    name: str,
    run_mode: RunMode,
    substitutions: dict = None) -> Tuple[dict, dict, list]:
    """Reads the options from the given preset loaded into the
    configuration parser.

    Arguments:
        parser (ConfigParser): The parser that reads the options.
        name (str): The name of the preset.
        run_mode (RunMode): The mode that the script is invoked
            in.
        substitutions (dict): The values that should override the
            arguments in the preset files. The substitutions are
            currently disabled.

    Returns:
        Three values: the first one is a dictionary containing
        the names of the preset options and the values associated
        with them, the second one is a dictionary containing the
        names of the preset options and the values associated
        with them that are given after the double dash, and the
        third one contains a list of the erroneous options.
    """
    logging.debug("Starting to read the preset '%s'", name)

    is_mode_specific_preset = name.startswith(CONFIGURATION_PRESET_PREFIX) \
        or name.startswith(COMPOSING_PRESET_PREFIX)

    name_with_prefix = None

    if run_mode is RunMode.configure:
        name_with_prefix = "{}{}".format(CONFIGURATION_PRESET_PREFIX, name)
        logging.debug(
            "Checking whether a mode-specific preset portion '%s' exists for "
            "the preset '%s'",
            name_with_prefix,
            name
        )
    elif run_mode is RunMode.compose:
        name_with_prefix = "{}{}".format(COMPOSING_PRESET_PREFIX, name)
        logging.debug(
            "Checking whether a mode-specific preset portion '%s' exists for "
            "the preset '%s'",
            name_with_prefix,
            name
        )

    if name not in parser.sections() \
            and name_with_prefix not in parser.sections():
        return None

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

        if option == _MIXIN_OPTION and not is_mode_specific_preset:
            # Multiple mix-in presets are allowed in one option.
            mixins = [mixin.strip() for mixin in value.splitlines()]

            for mixin in mixins:
                (mixin_options,
                 mixin_options_after_end,
                 missing_mixin_options) = _read_preset(
                    parser=parser,
                    name=mixin,
                    run_mode=run_mode,
                    substitutions=substitutions
                )
                options.update(mixin_options)
                options_after_end.update(mixin_options_after_end)
                missing_options.extend(missing_mixin_options)

        elif option == _DASH_DASH_OPTION:
            dash_dash_seen = True
        else:
            pair_to_add = {option: value}
            if dash_dash_seen:
                options_after_end.update(pair_to_add)
            else:
                options.update(pair_to_add)

    if name_with_prefix and name_with_prefix in parser.sections():
        (mode_options,
         mode_options_after_end,
         missing_mode_options) = _read_preset(
            parser=parser,
            name=name_with_prefix,
            run_mode=run_mode,
            substitutions=substitutions
        )
        options.update(mode_options)
        options_after_end.update(mode_options_after_end)
        missing_options.extend(missing_mode_options)

    return options, options_after_end, missing_options


def get_preset_options(
    file_names: List[str],
    preset_name: str,
    run_mode: RunMode,
    substitutions: dict = None
) -> Tuple[dict, dict]:
    """Gets the options in the given preset.

    Arguments:
        file_names (list): The files from which the presets are
            read.
        preset_name (str): The name of the preset.
        run_mode (RunMode): The mode that the script is invoked
            in.
        substitutions (dict): The values that should override the
            arguments in the preset files. The substitutions are
            currently disabled.

    Returns:
        Two values: the first one is a dictionary containing the
        names of the preset options and the values associated
        with them and the second one is a dictionary containing
        the names of the preset options and the values associated
        with them that are given after the double dash.
    """
    config_parser = _create_configuration_parser(substitutions=substitutions)

    files_read = config_parser.read(file_names)

    if files_read == []:
        logging.warning(
            "The preset files aren't found (tried %s)",
            file_names
        )
        return []

    options, options_after_end, missing_options = _read_preset(
        parser=config_parser,
        name=preset_name,
        run_mode=run_mode,
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


def get_all_preset_names(file_names: List[str]) -> list:
    """Gets the names of the presets in a preset file.

    Args:
        file_names (list): The files from which the presets are
            read.

    Returns:
        A list with the names of the presets.
    """
    config_parser = _create_configuration_parser()
    files_read = config_parser.read(file_names)
    if files_read == []:
        logging.warning(
            "The preset files aren't found (tried %s)",
            file_names
        )
        return []
    return config_parser.sections()
