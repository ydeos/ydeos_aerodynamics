#!/usr/bin/env python
# coding: utf-8

r"""ydeos_aerodynamics's setup.py"""

from distutils.core import setup

import ydeos_aerodynamics


setup(name=ydeos_aerodynamics.__project_name__,
      version=ydeos_aerodynamics.__version__,
      description=ydeos_aerodynamics.__description__,
      long_description='Aerodynamics computations: air characteristics, '
                       'apparent wind, true wind, vertical profile, '
                       'wind speed distribution, windage and sails force model',
      url=ydeos_aerodynamics.__url__,
      download_url=ydeos_aerodynamics.__download_url__,
      author=ydeos_aerodynamics.__author__,
      author_email=ydeos_aerodynamics.__author_email__,
      license=ydeos_aerodynamics.__license__,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.7'],
      keywords='aerodynamics',
      packages=['ydeos_aerodynamics'])
