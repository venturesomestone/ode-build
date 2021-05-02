# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""A module that defines the tests for the shell utilities."""

from couplet_composer.util import shell


def test_quote_command():
    cmd = ["app", "--option", "value", "--another-option=and-value"]
    expected = "app --option value --another-option=and-value"
    assert shell.quote_command(cmd) == expected
