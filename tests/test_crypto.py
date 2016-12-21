# -*- coding: utf-8 -*-

import six
import pytest
import binascii
from jak import helpers
from Crypto.Cipher import AES
from click.testing import CliRunner
import jak.crypto_services as crypto
from jak.exceptions import JakException

try:
    from unittest import mock
except ImportError:
    import mock


@pytest.fixture
def runner():
    return CliRunner()


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


@pytest.mark.parametrize('key', [
    '',
    '1',
    '1111111111111111',  # 16
    '111111111111111111111111',  # 24
    '11111111111111111111111111111111',  # 32
    '111111111111111111111111111111111111111111111111111111111111111',  # 63
    '11111111111111111111111111111111111111111111111111111111111111111',  # 65
])
def test_encrypt_exceptions(cipher, key):
    with pytest.raises(JakException) as excinfo:
        cipher.encrypt(key=key, secret='my secret')
    assert 'Key must be exactly 64 characters' in str(excinfo.value)


def test_encrypt_decrypt(cipher):
    key = 'f2f3222f8b1c799b6abc78e26e5a9378814bc23f04a10576610827569e956b42'
    secret = 'secret'

    encrypted = cipher.encrypt(key=key, secret=secret)
    decrypted = cipher.decrypt(key=key, encrypted_secret=encrypted)
    assert isinstance(encrypted, six.binary_type)
    assert isinstance(decrypted, six.binary_type)
    assert decrypted.decode('utf-8') == secret
    assert encrypted != secret
    assert encrypted != decrypted


def test_extract_iv(cipher):
    cipher.fingerprint_length = 1
    cipher.block_size = 3
    assert cipher.extract_iv("abcdefg") == "bcd"

    # not an iterable.
    with pytest.raises(TypeError):
        cipher.extract_iv(5)


def test_create_integrity_fingerprint(cipher):
    iv = cipher._generate_iv()
    key = helpers.generate_256bit_key().decode('utf-8')

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
        key = helpers.generate_256bit_key().decode('utf-8')
        new_way = cipher._create_integrity_fingerprint(key, iv)
        old_way = cipher._old_python_create_integrity_fingerprint(key, iv)
        assert new_way == binascii.hexlify(old_way)
    else:
        pass


def test_has_integrity(cipher):
    key = 'd2944c68b750474b85609147ce6d3aae875e6ae8ac63618086a58b1c1716402d'
    secret = 'integrity'
    encrypted = cipher.encrypt(key, secret)
    iv = encrypted[cipher.fingerprint_length:cipher.fingerprint_length + cipher.block_size]
    assert cipher._has_integrity(binascii.unhexlify(key), encrypted, iv) is True

    bad_key = '02944c68b750474b85609147ce6d3aae875e6ae8ac63618086a58b1c1716402d'
    assert bad_key != key
    assert cipher._has_integrity(binascii.unhexlify(bad_key), encrypted, iv) is False


def test_encrypt_file(tmpdir):
    secretfile = tmpdir.mkdir("sub").join("hello")
    secretfile.write("secret")
    assert secretfile.read() == "secret"
    key = helpers.generate_256bit_key().decode('utf-8')
    crypto.encrypt_file(jwd=secretfile.dirpath().strpath, filepath=secretfile.strpath, key=key)
    assert secretfile.read() != "secret"
    assert crypto.ENCRYPTED_BY_HEADER in secretfile.read()


def test_bad_encrypt_file_filepath(tmpdir):
    key = helpers.generate_256bit_key().decode('utf-8')
    result = crypto.encrypt_file(jwd='', filepath="", key=key)
    assert "can't find the file: " in result


def test_decrypt_file(runner, tmpdir):
    with runner.isolated_filesystem():
        secretfile = tmpdir.mkdir("sub").join("hello")
        secretfile.write("""- - - Encrypted by jak - - -

    Y2JjMzYxYzM4YzZhNWMwMjEwMGQ2ZTI4ZDUzYmFlMTUxMjMxMTNlNmEyNjVi
    N2RhYTE1MDkxYmMxMjUzOWQ3NTA2ZDRhZDRlOTUwNGQ3MDUyYTUzMzhkNTk3
    Y2JmMDdkN2VjOWQ2MDEzYTA5NmFlODM0OGUxMTI3Njk4YzA0MTn7m1e7RBW1
    DmeAbo2cg46cmhWwsKHbug==""")
        key = '2a57929b3610ba53b96f472b0dca27402a57929b3610ba53b96f472b0dca2740'
        crypto.decrypt_file(jwd=secretfile.dirpath().strpath, filepath=secretfile.strpath, key=key)
        assert secretfile.read() == "secret\n"


def test_encrypt_and_decrypt_a_file(runner, tmpdir):
    with runner.isolated_filesystem():
        secretfile = tmpdir.mkdir("sub").join("hello")
        secret_content = "supercalifragialisticexpialidocious"
        secretfile.write(secret_content)
        assert secretfile.read() == secret_content
        key = helpers.generate_256bit_key().decode('utf-8')
        crypto.encrypt_file(jwd=secretfile.dirpath().strpath, filepath=secretfile.strpath, key=key)

        # File has changed
        assert secretfile.read() != secret_content

        # File has the header (which we now assume means it is encrypted,
        # which might be presumptuous.)
        assert crypto.ENCRYPTED_BY_HEADER in secretfile.read()

        crypto.decrypt_file(jwd=secretfile.dirpath().strpath, filepath=secretfile.strpath, key=key)

        # Back to original
        assert secretfile.read() == secret_content
