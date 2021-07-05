#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from setuptools import setup, find_packages

PACKAGE_NAME = 'reactor'

REQUIREMENTS = install_requires = []

setup(
    name=PACKAGE_NAME,
    version='0.1',
    author="elo",
    description="",
    author_email='exchange@elo.enterprises',
    url='https://github.com/elo-enterprises/reactor',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
    dependency_links=[
    ],
    entry_points={
        'console_scripts':
        [
            'reactor = {0}.bin.reactor:entry'.format(PACKAGE_NAME),
            'r = {0}.bin.reactor:entry'.format(PACKAGE_NAME),
        ]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
