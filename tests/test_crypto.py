# -*- coding: utf-8 -*-

import pytest
import jak.crypto_services as crypto
import jak.password_services as ps
from Crypto.Cipher import AES
import six
from jak.exceptions import JakException
import binascii


@pytest.fixture
def cipher():
    return crypto.AES256Cipher()


def test_cipher(cipher):
    assert cipher.cipher == AES
    assert cipher.block_size == AES.block_size
    assert cipher.mode == AES.MODE_CFB


def test_generate_iv(cipher):
    result = cipher._generate_iv()
    assert len(result) == 16
    assert isinstance(result, six.binary_type)


@pytest.mark.parametrize('password', [
    '',
    '1',
    '1111111111111111',  # 16
    '111111111111111111111111',  # 24
    '111111111111111111111111111111111111111',  # 39
])
def test_encrypt_exceptions(cipher, password):
    with pytest.raises(JakException) as excinfo:
        cipher.encrypt(key=password, secret='my secret')
    assert 'Password must be exactly 32 characters' in str(excinfo.value)


def test_encrypt_decrypt(cipher):
    key = 'ldsjfhdskjfhdskljfhdsklfjh347398'
    secret = 'my secret'

    encrypted = cipher.encrypt(key=key, secret=secret)
    decrypted = cipher.decrypt(key=key, encrypted_secret=encrypted)
    assert isinstance(encrypted, six.binary_type)
    assert isinstance(decrypted, six.binary_type)
    assert decrypted.decode('utf-8') == secret
    assert encrypted != secret
    assert encrypted != decrypted


def test_create_integrity_fingerprint(cipher):
    iv = cipher._generate_iv()
    key = ps.generate_256bit_key().decode('utf-8')

    from datetime import datetime
    start = datetime.now()
    for x in range(15):
        fingerprint = cipher._create_integrity_fingerprint(key, iv)
    end = datetime.now()
    elapsed = end - start
    assert elapsed.total_seconds() > 0.1
    assert len(fingerprint) == cipher.fingerprint_length
    assert isinstance(fingerprint, six.binary_type)


def test_create_integrity_fingerprint_old_python(cipher):
    """Technically I dont need to check for python 3 here but otherwise I am
    just comparing the exact same thing against itself."""
    if six.PY3:
        iv = cipher._generate_iv()
        key = ps.generate_256bit_key().decode('utf-8')
        new_way = cipher._create_integrity_fingerprint(key, iv)
        old_way = cipher._old_python_create_integrity_fingerprint(key, iv)
        assert new_way == binascii.hexlify(old_way)
    else:
        pass


def test_has_integrity(cipher):
    key = 'lds3fhdskj2hdskl1fhdsklfjh347398'
    secret = 'integrity'
    encrypted = cipher.encrypt(key, secret)
    iv = encrypted[cipher.fingerprint_length:cipher.fingerprint_length + cipher.block_size]
    assert cipher._has_integrity(key, encrypted, iv) is True

    bad_key = '0ds3fhdskj2hdskl1fhdsklfjh347398'
    assert bad_key != key
    assert cipher._has_integrity(bad_key, encrypted, iv) is False


def test_encrypt_file(tmpdir):
    tempfile = tmpdir.mkdir("sub").join("hello")
    tempfile.write("secret")
    assert tempfile.read() == "secret"
    key = ps.generate_256bit_key().decode('utf-8')
    crypto.encrypt_file(filename=tempfile.strpath, password=key)
    assert tempfile.read() != "secret"
    assert crypto.ENCRYPTED_BY_HEADER in tempfile.read()


def test_decrypt_file(tmpdir):
    tempfile = tmpdir.mkdir("sub").join("hello")
    tempfile.write("""- - - Encrypted by jak - - -

NzIyMzVkODc3ZWFhM2VlMTg5MTYyZTllNTFlNGMxZmQzMzhmN2IwM2YxNmEz
OGNiMTI5MjI2ODA1ZWRmNDg5M2IxNGI5ZjNmNDk0ODVjNDcwOTE5MWI3N2Q5
Y2FlNTQwZWI2ZmY2MzE5YTZiOGU1NTA5ZGVhNmY2OTMxNTAyZDUcDK2xUZxf
DTHv3kq_ukiq7rO7MiJDgQ==
""")
    key = '2a57929b3610ba53b96f472b0dca2740'
    crypto.decrypt_file(filename=tempfile.strpath, password=key)
    assert tempfile.read() == "secret\n"


#
# def test_encrypt_and_decrypt_a_file():
#     # TODO
#     assert True is False
#
#
# def test_ed_all_password_cases():
#     """
#     password_file value not in jakfile
#     password_file value in jakfile but no value
#     password_file value in jakfile and has value (yay!)
#     """
#     assert True is False
#
#
# def test_ed_all_no_jakfile():
#     assert True is False
