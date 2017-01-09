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

Jak is a tool for encrypting and decrypting text files. It works extra well if used in a git repository.


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

   jak encrypt all  # or jak stomp
   jak decrypt all  # jak shave


TODO: (have a video here of jak usage)


Table of Contents:

.. toctree::
   :maxdepth: 2

   guide/usage
   guide/advanced
   api


Support
-------

jak is tested on Python:

 - 2.7 (latest)
 - 3.3 - 3.6
 - `PyPy <http://pypy.org/>`_

jak is currently planning to drop Python 2 support when `this clock reaches zero <https://pythonclock.org/>`_.

jak seems to work well on most unix* systems. But development happens on ubuntu and macOS.
**jak will support windows soon.**

Encryption
----------

jak uses AES256 which is secure (source) as long as you feed it a good password. jak will generate this password for you if you ask nicely.

.. toctree::
   :maxdepth: 2



.. _license:

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
