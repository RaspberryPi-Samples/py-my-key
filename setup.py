#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import io

here = path.abspath(path.dirname(__file__))

NAME = 'py_my_key'
filename = path.join(NAME, 'version.py')
with open(filename) as f:
    exec(f.read())

filename = path.join(here, 'README.rst')
with io.open(filename, 'rt', encoding='UTF-8') as f:
    readme = f.read()

filename = path.join(here, 'HISTORY.rst')
with io.open(filename, 'rt', encoding='UTF-8') as f:
    history = f.read()

requirements = [
    # TODO: put package requirements here
    'tzlocal',
    'pingo'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name=NAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/development.html#single-sourcing-the-version
    version=__version__,

    description='Access control with RaspberryPi and NFC card reader',

    long_description=readme + '\n\n' + history,

    # The project's main homepage.
    url=__url__,

    # Author details
    author=__author__,
    author_email=__email__,

    # Choose your license
    license=__license__,
    zip_safe=False,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Environment :: Console',
        #'Topic :: Software Development :: Build Tools',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Cython',

        'Programming Language :: Python',
        #'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.4',

        'Topic :: Database',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

    ],

    # What does your project relate to?
    keywords='',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    test_suite='tests',
    install_requires=requirements,

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['check-manifest', 'nose'],
        'test': ['coverage', 'nose'],
        'hw_nxp_rpi': ['nxppy'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    #package_data={
    #    'sample': ['logging.conf'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'py_my_key=py_my_key.cli_rpi_access:main',
            'db_admin=py_my_key.cli_db_admin:main',
        ],
    },
)
