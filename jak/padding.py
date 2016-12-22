import six


def pad(data, bs=16):
    """PKCS#7 Padding

    Pad with remaining blocksize.
    so if blocksize is 4 and you provide data 'aa' it should pad it as
    'aa\x02\x02'
    """
    length = bs - len(data) % bs
    data += chr(length) * length
    return data


def unpad(data):
    """remove PKCS#7 padding by removing as many digits as
    the padding indicates are padding.
    """
    amount_of_padding = ord(data[-1])
    return data[:-amount_of_padding]
