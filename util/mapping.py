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

"""This support module has an enhanced dictionary class."""


class Mapping(dict):
    """
    Mapping() -> new empty dictionary

    Mapping(mapping) -> new dictionary initialized from a mapping
    object's (key, value) pairs

    Mapping(iterable) -> new dictionary initialized as if via:

    d = {}
    for k, v in iterable:
        d[k] = v

    Mapping(**kwargs) -> new dictionary initialized with the
    name=value pairs in the keyword argument list. For example:
    Mapping(one=1, two=2)
    """
    def __init__(self, *args, **kwargs):
        super(Mapping, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    self[key] = value
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Mapping, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Mapping, self).__delitem__(key)
        del self.__dict__[key]
