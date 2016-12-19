"""
Jak
---
Jak is a tool for making it dead simple to encrypt and decrypt files.

About versioning
----------------
Past, current and future versions.

0.X Troubled Toddler        <-- CURRENT
1.X Young Whippersnapper
2.X Teenage Wasteland
3.X Highschool Sweetheart
4.X Wannabee Scientist
5.X Jaded Hipster
6.X Midlife Maniac
7.X Dorky Parent
8.X Rattled Retiree
9.X Cranky Old Seafarer
10.X Wizened Witch

If in doubt about how version should increase see: http://semver.org/
The exception is version 1.X which is when we are saying that we are comfortable
with people using it. I Don't care what incompatible API changes happen during 0.X
it is NOT 1.X until we are 99.9 percent sure it is secure.

Semantic Versioning Cheatsheet
------------------------------
version 1.2.3 means MAJOR = 1, MINOR = 2, PATCH = 3.
MAJOR version when you make incompatible API changes,
MINOR version when you add functionality in a backwards-compatible manner, and
PATCH version when you make backwards-compatible bug fixes.

Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

__version__ = '0.9.1'
__version_full__ = "Jak v{0} ({1})".format(__version__, 'Troubled Toddler')
