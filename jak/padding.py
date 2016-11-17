import six


def pad32(string):
    """Force a string to be of length 32.
    Either by adding padding in the form of multiple '-' signs
    or by slicing the end"""
    if len(string) < 32:
        return string.ljust(32, '-')
    return string[:32]


def PKCS7_16(unpadded_text):
    """Takes a string and adds padding (PKCS7) to 16"""
    padding_number = 16 - (len(unpadded_text) % 16)
    padding = chr(padding_number) * padding_number if padding_number != 16 else ""
    return unpadded_text + padding


def unPKCS7_16(padded_text):
    """Takes bytes and removes padding"""
    final_byte = padded_text[-1:]
    padding_int = six.byte2int(final_byte)

    # If its not even an integer then it is definitely not padding
    if not isinstance(padding_int, six.integer_types):
        return padded_text

    # If it is not between 1-16 then it is not padding
    if (isinstance(padding_int, six.integer_types) and padding_int > 16):
        return padded_text

    # Let's make sure it is padding by counting the occurences. We would expect to find
    # as many occurences of padding as the padding_int number.
    # b"abcdefghijklmn\x02\x02" would have two occurences for example.
    # I wouldn't mind using reverse here but python 2 and three tend to dislike that...
    for each in range(1, padding_int + 1):
        current_char = padded_text[-each]

        # Python 2 has current_char as an integer automagically, which is bad for us.
        # while Python 3 returns the actual byte
        if isinstance(current_char, six.integer_types):
            current_char = chr(current_char).encode()

        if final_byte != current_char:

            # If a piece of the padding is not what we are expecting then it
            # wasn't padded and we should just return the whole thing
            return padded_text

    # Was padded since the above check worked out.
    return padded_text[:-padding_int]
