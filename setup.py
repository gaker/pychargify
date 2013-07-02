#!/usr/bin/env python
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pychargify import get_version


setup(
    name='pychargify',
    version=get_version(),
    description="",
    packages=find_packages(),
    test_suite='nose.collector',
    install_requires=['requests==1.2.3', 'python-dateutil==2.1', ],
)
