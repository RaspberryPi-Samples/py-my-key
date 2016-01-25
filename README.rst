===============================
Py-My-Key
===============================

.. image:: https://img.shields.io/pypi/v/py-my-key.svg
        :target: https://pypi.python.org/pypi/py-my-key/

.. image:: https://img.shields.io/pypi/pyversions/py-my-key.svg
        :target: https://pypi.python.org/pypi/py-my-key/

.. image:: https://img.shields.io/pypi/wheel/py-my-key.svg
        :target: https://pypi.python.org/pypi/py-my-key/

.. image:: https://img.shields.io/pypi/l/py-my-key.svg
        :target: https://pypi.python.org/pypi/py-my-key/

.. image:: https://img.shields.io/pypi/status/py-my-key.svg
        :target: https://pypi.python.org/pypi/py-my-key/

.. image:: https://img.shields.io/pypi/dm/py-my-key.svg
        :target: https://pypi.python.org/pypi/py-my-key/

.. image:: https://requires.io/github/RaspberryPi-Samples/py-my-key/requirements.svg?branch=master
        :target: https://requires.io/github/RaspberryPi-Samples/py-my-key/requirements/?branch=master

.. image:: https://landscape.io/github/RaspberryPi-Samples/py-my-key/master/landscape.svg?style=flat
        :target: https://landscape.io/github/RaspberryPi-Samples/py-my-key/master

.. image:: https://www.codacy.com/project/badge/BADGEID
        :target: https://www.codacy.com/app/s-celles/py-my-key/

.. image:: https://readthedocs.org/projects/py-my-key/badge/?version=latest
        :target: https://readthedocs.org/projects/py-my-key/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/travis/RaspberryPi-Samples/py-my-key.svg
        :target: https://travis-ci.org/RaspberryPi-Samples/py-my-key/


Access control with RaspberryPi and NFC card reader

* Documentation: https://py-my-key.readthedocs.org.

Features
--------

* TODO

Install
-------

.. code:: bash

    $ pip install py-my-key

Usage
-----

.. code:: python

    In [1]: from py_my_key import py_my_key

Development
-----------

You can help to develop this library.

Issues
^^^^^^

You can submit issues using https://github.com/RaspberryPi-Samples/py-my-key/issues

Clone
^^^^^

You can clone repository to try to fix issues yourself using:

::

    $ git clone https://github.com/RaspberryPi-Samples/py-my-key.git

Run unit tests
^^^^^^^^^^^^^^

Run all unit tests

::

    $ nosetests -s -v --with-doctest

Run a given test

::

    $ nosetests tests/test_rasp_access.py:Rasp_access.test_000_something -s -v

Install development version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ python setup.py install

or

::

    $ sudo pip install git+https://github.com/RaspberryPi-Samples/py-my-key.git

Collaborating
^^^^^^^^^^^^^

-  Fork repository
-  Create a branch which fix a given issue
-  Submit pull requests

https://help.github.com/categories/collaborating/

Examples
^^^^^^^^

see `samples <samples>`_ directory

Credits
---------

This package was created with Cookiecutter_ and the `lwalter86/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`lwalter86/cookiecutter-pypackage`: https://github.com/lwalter86/cookiecutter-pypackage
