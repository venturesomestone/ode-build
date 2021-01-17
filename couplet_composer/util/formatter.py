# Copyright (c) 2021 Antti Kivi
# Licensed under the MIT License

"""A module that contains the custom formatter for logging.
"""

import logging

from typing import Any


class Formatter(logging.Formatter):
    """A class for creating object that is the formatter of the
        logging.
    """

    GREY = "\x1b[38;21m"
    YELLOW = "\x1b[33;21m"
    RED = "\x1b[31;21m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s " \
        "(%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: GREY + FORMAT + RESET,
        logging.INFO: GREY + FORMAT + RESET,
        logging.WARNING: YELLOW + FORMAT + RESET,
        logging.ERROR: RED + FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT + RESET
    }

    def format(self, record: Any) -> Any:
        """Formats the logging message.

        Args:
            record (Any): The logging record.

        Returns:
            The formatted message.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
