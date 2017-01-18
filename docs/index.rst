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

   # All files listen in the jakfile should now be encrypted.

We also made this video that might be helpful for running through a basic setup in a git repository.

.. raw:: html

   <asciinema-player src="_static/videos/quickstart.json"></asciinema-player>


Stewardship
-----------

`Dispel <https://dispel.io>`_ is the main steward of jaks development. But all contributions are encouraged and welcome. Please read the :ref:`contribution guide <contributor>` for more information on contributing.


Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   guide/usage
   guide/advanced
   guide/commands
   guide/contributor
   support


.. _support_short:

Support
-------

jak works if you have a modern Python (2.7-3.5) installed on a `*nix <https://en.wikipedia.org/wiki/Unix-like>`_ system.

:ref:`You can read about it in excrutiating detail here. <support_detailed>`

Proposed future features and enhancements
-----------------------------------------

- Support for binary files (non text files)
- Windows support
- Upgradeable encryption. Basically all encryption eventually gets old, so if we can make a smooth way for people to migrate between the encryption jak implements that seems like a pretty good idea.
- Easier key rotation.


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
