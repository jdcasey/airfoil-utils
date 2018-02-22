#!/usr/bin/env python2

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import sys

# handle python 3
if sys.version_info >= (3,):
    use_2to3 = True
else:
    use_2to3 = False

setup(
    zip_safe=True,
    use_2to3=use_2to3,
    name='airfoil-utils',
    version='1.0',
    long_description='Generate printable files for airfoils from UIUC Airfoil database',
    classifiers=[
      "Development Status :: 4 - Beta",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Programming Language :: Python :: 2",
      "Topic :: Utilities",
    ],
    keywords='airfoil 3d-printing OpenSCAD SVG',
    author='John Casey',
    author_email='jdcasey@commonjava.org',
    url='https://github.com/jdcasey/airfoil-utils',
    download_url='https://github.com/jdcasey/airfoil-utils/archive/1.0.tar.gz',
    license='GPLv3+',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[
      "matplotlib",
      "requests",
      "click",
    ],
    entry_points={
      'console_scripts': [
        'foil2plot = airfoil:foil2plot',
        'foil2scad = airfoil:foil2scad',
        'foil2svg = airfoil:foil2svg',
      ],
    }
)

