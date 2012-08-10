#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-prefinery',
      version='0.1.1',
      packages=find_packages(exclude=[]),
      package_data={'prefinery': ['templates/prefinery/*']},
      exclude_package_data={'prefinery': ['bin/*.pyc']},
      )
