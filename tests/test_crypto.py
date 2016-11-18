import pytest
import jak.crypto_services as crypto
from Crypto.Cipher import AES
import six


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


def test_encrypt_exceptions(cipher):
    with pytest.raises(ValueError) as excinfo:
        cipher.encrypt(key=b'11111111111111111', secret=b'my secret')
        assert 'AES key must be either 16, 24, or 32 bytes long' in str(excinfo.value)


def test_encrypt_decrypt(cipher):
    key = b'ldsjfhdskjfhdskljfhdsklfjh347398'
    secret = b'my secret'
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
