#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-prefinery',
      version='0.1',
      packages=find_packages(exclude=[]),
      exclude_package_data={'prefinery': ['bin/*.pyc']},
      )
