# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import six

if six.PY3:
    import codecs

    def b(x):
        if isinstance(x, six.binary_type):
            return x
        else:
            return codecs.latin_1_encode(x)[0]
else:
    def b(x):
        if isinstance(x, six.binary_type):
            return x
        else:
            return bytes(x)
