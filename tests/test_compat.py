# -*- coding: utf-8 -*-

from jak.compat import b


def test_b():
    assert b('a') == b'a'
    assert b(b'a') == b'a'
    assert b(u'a') == b'a'
    assert b(chr(222)) == b'\xde'
