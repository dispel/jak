from jak.padding import pad, unpad


def test_pad():
    """Allow me to introduce you to my old friend, the nuclear option."""
    assert pad(data=b'a') == b'a\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
    assert pad(data=b'aa') == b'aa\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e'
    assert pad(data=b'aaa') == b'aaa\r\r\r\r\r\r\r\r\r\r\r\r\r'
    assert pad(data=b'aaaa') == b'aaaa\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'
    assert pad(data=b'aaaaa') == b'aaaaa\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b'
    assert pad(data=b'aaaaaa') == b'aaaaaa\n\n\n\n\n\n\n\n\n\n'
    assert pad(data=b'aaaaaaa') == b'aaaaaaa\t\t\t\t\t\t\t\t\t'
    assert pad(data=b'aaaaaaaa') == b'aaaaaaaa\x08\x08\x08\x08\x08\x08\x08\x08'
    assert pad(data=b'aaaaaaaaa') == b'aaaaaaaaa\x07\x07\x07\x07\x07\x07\x07'
    assert pad(data=b'aaaaaaaaaa') == b'aaaaaaaaaa\x06\x06\x06\x06\x06\x06'
    assert pad(data=b'aaaaaaaaaaa') == b'aaaaaaaaaaa\x05\x05\x05\x05\x05'
    assert pad(data=b'aaaaaaaaaaaa') == b'aaaaaaaaaaaa\x04\x04\x04\x04'
    assert pad(data=b'aaaaaaaaaaaaa') == b'aaaaaaaaaaaaa\x03\x03\x03'
    assert pad(data=b'aaaaaaaaaaaaaa') == b'aaaaaaaaaaaaaa\x02\x02'
    assert pad(data=b'aaaaaaaaaaaaaaa') == b'aaaaaaaaaaaaaaa\x01'
    assert pad(data=b'aaaaaaaaaaaaaaaa') == b'aaaaaaaaaaaaaaaa\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'  # noqa


def test_unpad():
    assert b'a' == unpad(data=b'a\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f')
    assert b'aa' == unpad(data=b'aa\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e')
    assert b'aaa' == unpad(data=b'aaa\r\r\r\r\r\r\r\r\r\r\r\r\r')
    assert b'aaaa' == unpad(data=b'aaaa\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c')
    assert b'aaaaa' == unpad(data=b'aaaaa\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b')
    assert b'aaaaaa' == unpad(data=b'aaaaaa\n\n\n\n\n\n\n\n\n\n')
    assert b'aaaaaaa' == unpad(data=b'aaaaaaa\t\t\t\t\t\t\t\t\t')
    assert b'aaaaaaaa' == unpad(data=b'aaaaaaaa\x08\x08\x08\x08\x08\x08\x08\x08')
    assert b'aaaaaaaaa' == unpad(data=b'aaaaaaaaa\x07\x07\x07\x07\x07\x07\x07')
    assert b'aaaaaaaaaa' == unpad(data=b'aaaaaaaaaa\x06\x06\x06\x06\x06\x06')
    assert b'aaaaaaaaaaa' == unpad(data=b'aaaaaaaaaaa\x05\x05\x05\x05\x05')
    assert b'aaaaaaaaaaaa' == unpad(data=b'aaaaaaaaaaaa\x04\x04\x04\x04')
    assert b'aaaaaaaaaaaaa' == unpad(data=b'aaaaaaaaaaaaa\x03\x03\x03')
    assert b'aaaaaaaaaaaaaa' == unpad(data=b'aaaaaaaaaaaaaa\x02\x02')
    assert b'aaaaaaaaaaaaaaa' == unpad(data=b'aaaaaaaaaaaaaaa\x01')
    assert b'aaaaaaaaaaaaaaaa' == unpad(data=b'aaaaaaaaaaaaaaaa\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10')  # noqa
