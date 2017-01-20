# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import six


def pad(data, bs=16):
    """PKCS#7 Padding. Takes a bytestring data and an optional blocksize 'bs'"""
    length = bs - (len(data) % bs)
    data += six.int2byte(length) * length
    return data


def unpad(data):
    """remove PKCS#7 padding by removing as many digits as
    the padding indicates are padding.

    :data: is a bytestring.
    Returns the unpadded bytestring.
    """

    # Python 3 raises the TypeError
    try:
        return data[:-ord(data[-1])]
    except TypeError:
        return data[:-data[-1]]
