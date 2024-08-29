#!/usr/bin/env python3
#
#  IRIS Seika.io Module Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import setuptools


setuptools.setup(
     name='iris_seika_module',
     version='1.0.0',
     packages=['iris_seika_module', 'iris_seika_module.seika_handler'],
     author="DFIR-IRIS",
     author_email="contact@dfir-iris.org",
     description="An interface module for Seika.io and DFIR-IRIS",
     long_description="An interface module for Seika.io and DFIR-IRIS",
     long_description_content_type="text/markdown",
     url="https://github.com/dfir-iris/iris-seika-module",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: LGPLv3",
         "Operating System :: OS Independent",
     ],
     install_requires=[
        "setuptools",
        "pyunpack"
    ]
 )
