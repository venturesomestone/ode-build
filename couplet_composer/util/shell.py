# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""A module that contains contains several shell helpers.
"""

import pipes


def _quote(arg):
    return pipes.quote(str(arg))


def quote_command(args):
    """Quotes a command for printing it."""
    return " ".join([_quote(a) for a in args])
