# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import six


def pad(data, bs=16):
    """PKCS#7 Padding

    Pad with remaining blocksize.
    so if blocksize is 4 and you provide data 'aa' it should pad it as
    'aa\x02\x02'
    """
    length = bs - len(data) % bs
    data += six.int2byte(length) * length
    return data


def unpad(data):
    """remove PKCS#7 padding by removing as many digits as
    the padding indicates are padding.
    """
    amount_of_padding = six.byte2int(data[-1])
    return data[:-amount_of_padding]
