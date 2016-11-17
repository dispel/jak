import pytest
from jak.padding import PKCS7_16, unPKCS7_16


@pytest.mark.parametrize("input, expected", [
    ("abcdefghijklmn", "abcdefghijklmn\x02\x02"),
    ("abcdefghijklmno", "abcdefghijklmno\x01"),
    ("a", "a\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f"),
    ("", ""),
    ("abcdefghijklmnop", "abcdefghijklmnop"),
    ("abcdefghij333", "abcdefghij333\x03\x03\x03")
])
def test_PKCS7_16(input, expected):
    assert PKCS7_16(input) == expected


@pytest.mark.parametrize("input, expected", [
    (b"abcdefghijklmn\x02\x02", b"abcdefghijklmn"),
    (b"abcdefghijklmno\x01", b"abcdefghijklmno"),
    (b"a\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f", b"a"),
    (b"abcdefghijklmnop", b"abcdefghijklmnop"),
    (b"abcdefghij333\x03\x03\x03", b"abcdefghij333")
])
def test_unPKCS7_16(input, expected):
    assert unPKCS7_16(input) == expected


def test_unPKCS7_16_should_raise():
    with pytest.raises(IndexError):
        unPKCS7_16(b"")
