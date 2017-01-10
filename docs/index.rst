.. jak documentation master file, created by
   sphinx-quickstart on Mon Jan  9 13:16:07 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

jak
===

.. Release \v |version|. (:ref:`Installation <install>`)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Jak is a tool for encrypting text files. It works extra well if used in a git repository.

****JAK IS NOT READY YET, YOU ARE WELCOME TO CHECK IT OUT BUT WE HIGHLY RECOMMEND AGAINST USING IT ON ANY ACTUAL SECRETS YET!****

Install
-------

.. sourcecode:: shell

   pip install jak


Quickstart
----------

.. sourcecode:: shell

   cd ~/folderThatMayOrMayNotBeARepo
   jak start

   edit jakfile # add which files you want to have be encrypted.

   jak encrypt all

   # All files should now be encrypted.


TODO: (have a video here of jak usage)


Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   guide/usage
   guide/advanced
   guide/commands


Support (Python & OS)
---------------------

jak is tested on Python:

 - 2.7.10 - 2.7.LATEST
 - 3.3 - 3.6
 - `PyPy <http://pypy.org/>`_

jak is planning to drop Python 2 support when `this clock reaches zero <https://pythonclock.org/>`_ in the name of `courage <http://www.theverge.com/2016/9/7/12838024/apple-iphone-7-plus-headphone-jack-removal-courage>`_, progress and maintaining a clean codebase.

jak seems to work well on most `*nix <https://en.wikipedia.org/wiki/Unix-like>`_ systems.


Currently planned features
--------------------------

- Support for binary files (non text files)
- Windows support


License
-------
Copyright 2016-2017 Dispel, LLC and contributors


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
