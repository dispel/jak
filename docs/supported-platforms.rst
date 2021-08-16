.. _support_detailed:


Supported platforms
===================

Python
------

jak is explicitly tested on Pythons:

- 3.6
- 3.7
- 3.8
- 3.9
- PyPy3

Works but CI fails:

- `PyPy3 <http://pypy.org/>`_. (It works just fine locally but travis seems to have trouble with it, so we removed it from CI for now. The issue is that pycrypto fails to install under it, and pycrypto seems to explicitly state that they dont work with pypy. Nonetheless, we've gotten this working on our machines just fine...)

jak follows the `Python end of support dates <https://docs.python.org/devguide/index.html#branchstatus>`_, which in practice means that support ends on the following dates:

- 3.6 (PEP 494) support ends 2021-12-23
- 3.7 (PEP 537) support ends 2023-06-27
- 3.8 (PEP 569) support ends 2024-10

OS
--

We believe jak should work well on most `*nix <https://en.wikipedia.org/wiki/Unix-like>`_ systems. But is mainly developed on Ubuntu and tested on Ubuntu and macOS.
