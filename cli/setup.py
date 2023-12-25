# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='omdb-cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Click'],
    entry_points={'console_scripts': ['omdb = main:cli']},
)
