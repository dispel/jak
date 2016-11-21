# -*- coding: utf-8 -*-

"""
jak.compat

This compat file is based on the one that the infamous requests library has.
Thanks Kenneth!
"""

import six


if six.PY3:
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)

if six.PY2:
    builtin_str = str
    bytes = str
    str = unicode  # noqa
    basestring = basestring
