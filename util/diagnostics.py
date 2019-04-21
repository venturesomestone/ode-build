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

"""This support module contains the logging functions."""

from __future__ import print_function

import sys

from datetime import datetime


ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

RED = "\033[31m"
GREEN = "\033[32m"
ORANGE = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"

FAIL = "\033[91m"
OK_GREEN = "\033[92m"
WARNING = "\033[93m"
OK_BLUE = "\033[94m"
HEADER = "\033[95m"


VERBOSE = False

DEBUG = False


def _coerce_verbosity(verbosity_override=None):
    if verbosity_override is None:
        return VERBOSE
    else:
        return verbosity_override


def _coerce_debug(debug_override=None):
    if debug_override is None:
        return DEBUG
    else:
        return debug_override


def _printer(
        level, color=None, verbosity_check=lambda: True, print_script=False,
        show_date=False, show_type=False):
    def _printer_decorator(func):
        def _wrapper(message):
            msg = ""
            if print_script:
                msg += "{}: ".format(sys.argv[0])
            if show_date:
                msg += "[{}]".format(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if show_type:
                msg += "[{}]".format(level)
            if show_date or show_type:
                msg += " "
            if color is not None:
                msg += "{}".format(color)
            msg += message
            if color is not None:
                msg += "{}".format(ENDC)
            if verbosity_check():
                print(msg)
            sys.stdout.flush()
            return msg
        return _wrapper
    return _printer_decorator


@_printer(level="trace", verbosity_check=_coerce_verbosity)
def trace(message):
    """
    Print a trace diagnostic notification to the standard output.
    """
    return message


@_printer(level="trace", verbosity_check=lambda: True)
def trace_do_print(message):
    """
    Print a trace diagnostic notification to the standard output.
    """
    return message


@_printer(level="trace", color=ORANGE, verbosity_check=_coerce_verbosity)
def trace_head(message):
    """
    Print a trace diagnostic notification to the standard output.
    """
    return message


@_printer(level="debug", verbosity_check=_coerce_debug)
def debug(message):
    """
    Print a debug diagnostic notification to the standard output.
    """
    return message


@_printer(level="debug", color=OK_GREEN, verbosity_check=_coerce_debug)
def debug_ok(message):
    """
    Print a debug diagnostic notification to the standard output.
    """
    return message


@_printer(level="debug", color=WARNING, verbosity_check=_coerce_debug)
def debug_note(message):
    """
    Print a debug diagnostic notification to the standard output.
    """
    return message


@_printer(level="debug", color=ORANGE, verbosity_check=_coerce_debug)
def debug_head(message):
    """
    Print a debug diagnostic notification to the standard output.
    """
    return message


@_printer(level="note", color=OK_BLUE)
def fine(message):
    """
    Print a diagnostic notification to the standard output
    notifying some step is complete.
    """
    return message


@_printer(level="note", color=HEADER + BOLD)
def head(message):
    """
    Print a header diagnostic notification to the standard
    output.
    """
    return message


@_printer(level="note")
def note(message):
    """Print a diagnostic notification to the standard output."""
    return message


@_printer(level="warning", color=WARNING)
def warn(message):
    """Print a warning notification to the standard output."""
    return message


def warning(message):
    """Print a warning notification to the standard output."""
    warn(message=message)


def fatal(message):
    """Raise a fatal error."""
    @_printer(
        level="fatal error", color=BOLD + FAIL, verbosity_check=lambda: False)
    def _impl(msg):
        return msg
    raise SystemExit(_impl(message))
