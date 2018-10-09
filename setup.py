# -*- coding: utf-8 -*-
__author__ = 'Brice Olivier'

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='visu-scanpath',
      version='0.2a0',
      description='Python tool for displaying a scanpath,'
      'a set of fixations and saccades,'
      ' with annotations and/or coloring fixations',
      install_requires=requirements,
      author='Brice Olivier',
      author_email='briceolivier1409@gmail.com',
      url='https://github.com/brice-olivier/',
      packages=['visuscanpath'],
      license=read('LICENSE'),
      long_description=read('README.md'))
