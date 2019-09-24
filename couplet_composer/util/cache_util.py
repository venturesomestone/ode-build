# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem project.
#
# Copyright 2019 Antti Kivi
# Licensed under the EUPL, version 1.2
#
# ------------------------------------------------------------- #

"""This utility module has the caching utilities."""

from functools import update_wrapper


__all__ = ["cached", "reify"]


def cached(func):
    """Decorator that caches result of method or function."""
    cache = {}

    def wrapper(*args, **kwargs):
        key = tuple(args) + tuple(kwargs.items())
        if key not in cache:
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        else:
            return cache[key]
    return update_wrapper(wrapper, func)


def reify(func):
    """
    Decorator that replaces the wrapped method with the result
    after the first call.

    Note: Support method that takes no arguments.
    """
    class Wrapper(object):
        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            result = func(obj)
            setattr(obj, func.__name__, result)
            return result
    return update_wrapper(Wrapper(), func)
