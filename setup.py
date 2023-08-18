#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="devenv.fuzzy_click",
    version="1.0.0",
    description="FZF integration for Click",
    author="devenv",
    author_email="boris.churzin@gmail.com",
    url="https://github.com/devenv/fuzzy-click",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click~=8.0",
        "click-plugins~=1.1.1",
        "click-command-tree~=1.1.0",
        "pyfzf~=0.3.1",
    ],
    extras_require={
        "dev": [
            "black>=22.0.0,<23.0.0",
            "flake8>=4.0.0,<5.0.0",
            "debugpy~=1.6.7",
        ],
    },
)
