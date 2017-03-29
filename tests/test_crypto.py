# -*- coding: utf-8 -*-

import six
import pytest
from jak import helpers
from jak.compat import b
from Crypto.Cipher import AES
from click.testing import CliRunner
import jak.crypto_services as crypto
from jak.exceptions import JakException


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cipher():
    key = '4e9e5f6688e2a011856f7d58a27f7d9695013a893d89ad7652f2976a5c61f97f'
    return crypto.AES256Cipher(key=key)


def test_cipher(cipher):
    assert cipher.cipher == AES
    assert cipher.BLOCK_SIZE == AES.block_size
    assert cipher.mode == AES.MODE_CBC


def test_bad_create_cipher():
    # Fails due to no key argument.
    with pytest.raises(TypeError):
        crypto.AES256Cipher()


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
    'notmadeupofonlyhexadecimalcharacters1111111111111111111111111111'  # 64
])
def test_bad_keys_for_cipher_exceptions(key):
    with pytest.raises(JakException) as excinfo:
        crypto.AES256Cipher(key=key)
    assert 'Key must be 64' in str(excinfo.value)


def test_encrypt_decrypt(cipher):
    secret = b'secret'

    ciphertext = cipher.encrypt(plaintext=secret)
    plaintext = cipher.decrypt(ciphertext=ciphertext)
    assert isinstance(ciphertext, six.binary_type)
    assert isinstance(plaintext, six.binary_type)
    assert plaintext == secret
    assert ciphertext != secret
    assert ciphertext != plaintext


def test_extractors(cipher):
    cipher.BLOCK_SIZE = len('IV')
    cipher.SIG_SIZE = len('signature')
    assert len(cipher.VERSION) == len('JAK-XXX')

    ciphertext = 'JAK-XXXIVpayloadsignature'
    assert cipher.extract_iv(ciphertext) == 'IV'
    assert cipher._extract_payload(ciphertext) == 'payload'
    assert cipher._extract_signature(ciphertext) == 'signature'
    assert cipher._extract_version(ciphertext) == 'JAK-XXX'


def test_authenticate(cipher):
    plaintext = b'integrity'
    ciphertext = cipher.encrypt(plaintext=plaintext)
    payload = cipher._extract_payload(ciphertext=ciphertext)
    signature = cipher._extract_signature(ciphertext=ciphertext)
    assert cipher._authenticate(data=payload, signature=signature) is True

    bad_key = '02944c68b750474b85609147ce6d3aae875e6ae8ac63618086a58b1c1716402d'
    assert bad_key != cipher.key

    # Maybe we should allow setting of key/hmac_key in a method?
    new_cipher = crypto.AES256Cipher(key=bad_key)
    assert new_cipher._authenticate(data=payload, signature=signature) is False


def test_authenticate_tampered(cipher):
    secret = b'integrity'
    ciphertext = cipher.encrypt(plaintext=secret)
    signature = cipher._extract_signature(ciphertext=ciphertext)
    payload = cipher._extract_payload(ciphertext=ciphertext)

    # Let's tamper with the payload
    dump = [x for x in payload]

    try:
        dump[5] = dump[5] + 1 if dump[5] != 255 else dump[5] - 1
    except TypeError:

        # Python 2 or PyPy
        x = ord(dump[5])
        dump[5] = chr(x + 1) if x != 255 else chr(x - 1)
        tampered_payload = "".join(dump)
    else:
        tampered_payload = b("".join(map(chr, dump)))

    assert payload != tampered_payload
    assert cipher._authenticate(data=tampered_payload, signature=signature) is False


def test_encrypt_file(tmpdir):
    secretfile = tmpdir.join("encrypt_file")
    secretfile.write("secret")
    assert secretfile.read() == "secret"
    key = helpers.generate_256bit_key().decode('utf-8')
    crypto.encrypt_file(jwd=secretfile.dirpath().strpath, filepath=secretfile.strpath, key=key)
    assert secretfile.read() != "secret"
    assert crypto.ENCRYPTED_BY_HEADER in secretfile.read()


def test_bad_encrypt_file_filepath(tmpdir):
    key = helpers.generate_256bit_key().decode('utf-8')
    with pytest.raises(JakException) as excinfo:
        crypto.encrypt_file(jwd='', filepath='', key=key)
    assert "can't find the file: " in str(excinfo.value)


def test_decrypt_file(runner, tmpdir):
    with runner.isolated_filesystem():
        secretfile = tmpdir.join("hello")
        secretfile.write("""- - - Encrypted by jak - - -

SkFLLTAwMI_ZCxve00vRIZq7if3C2cgVQ3Dlpjg2KPttRWtfq-bXOMsA1RUD
5h4PW-mnkFVkPJXWS0IHK95gfJNG9U13pcUoEj4bOGqtu62PCavRXZFcSwZ6
-rNE_PQvkoIFq7KlBFrdu8pWPCyFVvZjpGEFgw4=""")
        key = '2a57929b3610ba53b96f472b0dca27402a57929b3610ba53b96f472b0dca2740'
        crypto.decrypt_file(jwd=secretfile.dirpath().strpath, filepath=secretfile.strpath, key=key)
        assert secretfile.read().strip('\n') == "we attack at dawn"


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


def test_need_old_decrypt_version(cipher):
    same_version = b(cipher.VERSION)
    assert cipher._need_old_decrypt_function(version=same_version) is False

    different_version = b('JAK-XXX')
    assert cipher._need_old_decrypt_function(version=different_version) is True


def test_use_old_decrypt_version(cipher):

    # Build out this test once we add old decrypt function calls in here.
    # basically making sure it picks the right one.
    with pytest.raises(Exception):
        cipher._use_old_decrypt_function('version', 'ciphertext')
