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


Python Support
--------------

jak is tested on Pythons:

- 2.7.10+
- 3.3
- 3.4
- 3.5
- `PyPy <http://pypy.org/>`_

Planned but not tested yet, but hopefully work:

- 3.6
- PyPy3

jak follows the `Python end of support dates <https://docs.python.org/devguide/index.html#branchstatus>`_, which in practice means that support ends on the following dates:

- 3.3 (PEP 398) support ends 2017-09-29
- 3.4 (PEP 429) support ends 2019-03-16
- 2.7 (PEP 373) support ends 2020-01-01
- 3.5 (PEP 478) support ends 2020-09-13
- 3.6 (PEP 494) support ends 2021-12-23

For all you Python 2.7 lunatics out there that means when `this clock reaches zero <https://pythonclock.org/>`_ we drop 2.7 in the name of `courage <http://www.theverge.com/2016/9/7/12838024/apple-iphone-7-plus-headphone-jack-removal-courage>`_, progress and maintaining a clean codebase. It is my understanding that dropping 2.7 may implicitly mean dropping PyPy as well, which may sway this decision, since jak is a sucker for scrappy whippersnappers.

It is however likely that even without explicitly testing for it the 3.X versions will continue to work just fine even after we officially stop supporting them.


OS Support
----------

jak seems to work well on most `*nix <https://en.wikipedia.org/wiki/Unix-like>`_ systems.


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
