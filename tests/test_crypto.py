import pytest
import jak.crypto_services as crypto
from Crypto.Cipher import AES
import six
from jak.crypto_services import ENCRYPTED_BY_HEADER
from jak.exceptions import JakException
# import os


@pytest.fixture
def cipher():
    return crypto.AES256Cipher()


def test_cipher(cipher):
    assert cipher.cipher == AES
    assert cipher.block_size == AES.block_size
    assert cipher.mode == AES.MODE_CFB


def test_generate_iv(cipher):
    result = cipher.generate_iv()
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
    assert decrypted == secret
    assert encrypted != secret
    assert encrypted != decrypted


def test_generate_256bit_key():
    key = crypto.generate_256bit_key()
    assert len(key) == 32
    assert isinstance(key, six.binary_type)


def test_encrypt_file(tmpdir):
    tempfile = tmpdir.mkdir("sub").join("hello")
    tempfile.write("secret")
    assert tempfile.read() == "secret"
    key = crypto.generate_256bit_key()
    crypto.encrypt_file(key, tempfile.dirname + "/hello")
    assert tempfile.read() != "secret"
    assert ENCRYPTED_BY_HEADER in tempfile.read()


def test_decrypt_file():
    # TODO
    pass


def test_encrypt_and_decrypt_a_file():
    # TODO
    pass
