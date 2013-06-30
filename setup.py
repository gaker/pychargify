#!/usr/bin/env python
from setuptools import setup, find_packages

from pychargify import get_version


setup(
    name='pychargify',
    version=get_version(),
    description="",
    packages=find_packages(),
    install_requires=['requests', 'python-dateutil', ],
)