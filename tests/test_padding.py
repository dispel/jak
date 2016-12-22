import pytest
from jak.padding import pad, unpad


def test_pad():
    assert pad('a') == 'a\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
    assert pad('aaaaaaaaa') == 'aaaaaaaaa\x07\x07\x07\x07\x07\x07\x07'
    assert pad('aaaaaaaaaaaaaaa') == 'aaaaaaaaaaaaaaa\x01'


def test_unpad():
    assert unpad('aaaaaaaaaaaaaaa\x01') == 'aaaaaaaaaaaaaaa'
    assert unpad('a\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f') == 'a'
    assert unpad('aaaaaaaaaaaaaa\x02\x02') == 'aaaaaaaaaaaaaa'
    assert unpad('aaaaaaaaaaaaaaaaa\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f') == 'aaaaaaaaaaaaaaaaa'  # noqa
