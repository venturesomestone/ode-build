#!/usr/bin/env python

# ------------------------------------------------------------- #
#                         Ode Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

import io
import os

from glob import glob

from setuptools import find_packages, setup


# Package metadata
NAME = "ode-composer"
DESCRIPTION = "Tool for building, testing, and preparing binary " \
    "distribution archives of Obliging Ode."
URL = "https://github.com/anttikivi/ode-composer"
EMAIL = "antti@anttikivi.fi"
AUTHOR = "Antti Kivi"
REQUIRES_PYTHON = ">=2.7.11"
VERSION = None

# The packages that Ode Composer needs
REQUIRED = []

# The optional packages that Ode Composer can use
EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in the MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the __version__.py module of the package as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"],
        include=("*", "components")),
    entry_points={
        "console_scripts": ["ode-composer=ode_composer.__main__:main"]
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="SEE LICENCE IN LICENCE",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: Other/Proprietary License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
