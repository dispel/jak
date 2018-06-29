# -*- coding: utf-8 -*-

import six
import pytest
from jak import helpers
from jak.aes_cipher import AES256Cipher
from jak.compat import b
from Crypto.Cipher import AES
from click.testing import CliRunner
import jak.crypto_services as crypto
from jak.exceptions import JakException

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def test__restore_from_backup_ciphertext_altered(tmpdir):
    make_backup = tmpdir.join("ourfile")
    plaintext = "even write in it for the test"
    make_backup.write(plaintext)
    assert make_backup.read() == plaintext
    key = "9412735d31033ed596de83344939677e24bad58e9576392252d16d2243d1d9c5"
    crypto.encrypt_file(make_backup.dirpath().strpath, make_backup.strpath, key=key)
    make_backup.write("This has to go at the very end doesn't it?")
    assert crypto.ENCRYPTED_BY_HEADER in make_backup.read()
    encrypted_junk = make_backup.read()
    encrypted_junk = encrypted_junk.replace("""- - - Encrypted by jak - - -

""","")
    is_decrypted = crypto.decrypt_file(jwd=make_backup.dirpath().strpath, filepath=make_backup.strpath, key=key)
    assert '- is now decrypted.' in is_decrypted
    aes256_cipher = AES256Cipher(key=key)
    restoration = crypto._restore_from_backup(make_backup.dirpath().strpath, make_backup.strpath, altered_plaintext, aes256_cipher)

def test__restore_from_backup_no_alteration(tmpdir):
    make_backup = tmpdir.join("ourfile")
    plaintext = "even write in it for the test"
    make_backup.write(plaintext)
    assert make_backup.read() == plaintext
    key = "9412735d31033ed596de83344939677e24bad58e9576392252d16d2243d1d9c5"
    crypto.encrypt_file(make_backup.dirpath().strpath, make_backup.strpath, key=key)
    encrypted_junk = make_backup.read()
    encrypted_junk = encrypted_junk.replace("""- - - Encrypted by jak - - -

""","")
    assert crypto.ENCRYPTED_BY_HEADER in make_backup.read()
    is_decrypted = crypto.decrypt_file(jwd=make_backup.dirpath().strpath, filepath=make_backup.strpath, key=key)
    assert '- is now decrypted.' in is_decrypted
    aes256_cipher = AES256Cipher(key=key)
    restoration = crypto._restore_from_backup(make_backup.dirpath().strpath, make_backup.strpath, b(plaintext), aes256_cipher)
    assert restoration == encrypted_junk

def test__restore_from_backup_plaintext_altered(tmpdir):
#   we change the plaintext after we've decrypted so it will be different from the stored backup
#   This tests if _restore_from_backup gives nothing in this situation
    plaintext = "even write in it for the test"
    make_backup = tmpdir.join("ourfile")
    make_backup.write(plaintext)
    assert make_backup.read() == plaintext
    key = "9412735d31033ed596de83344939677e24bad58e9576392252d16d2243d1d9c5"
    crypto.encrypt_file(make_backup.dirpath().strpath, make_backup.strpath, key=key)
    assert crypto.ENCRYPTED_BY_HEADER in make_backup.read()
    encrypted_junk = make_backup.read()
    encrypted_junk = encrypted_junk.replace("""- - - Encrypted by jak - - -

""","")
    is_decrypted = crypto.decrypt_file(jwd=make_backup.dirpath().strpath, filepath=make_backup.strpath, key=key)
    assert '- is now decrypted.' in is_decrypted
    aes256_cipher = AES256Cipher(key=key)
    altered_plaintext = plaintext + "wuba wuba dub"
    restoration = crypto._restore_from_backup(make_backup.dirpath().strpath, make_backup.strpath, b(altered_plaintext), aes256_cipher)
    assert restoration == None

def test_empty__read_file(tmpdir):
#   Fails due to nothing in file
    emptyfile = tmpdir.join("emptyfile")
    emptyfile.write("")
    assert len(emptyfile.read()) == 0
    with pytest.raises(JakException) as excempty:
        crypto._read_file(emptyfile.strpath)
    assert "is empty" in str(excempty.value)

def test_nonempty__read_file(tmpdir):
    file = tmpdir.join("emptyfile")
    file.write("something")
    assert len(file.read()) != 0
    assert crypto._read_file(file.strpath) == b("something")

def test_already_encrypted(tmpdir):
    encryptfile = tmpdir.join("already_encrypt")
    encryptfile.write("be encrypt")
    assert encryptfile.read() == "be encrypt"
    key = helpers.generate_256bit_key().decode('utf-8')
    crypto.encrypt_file(jwd=encryptfile.dirpath().strpath, filepath=encryptfile.strpath, key=key)
    assert encryptfile.read() != "be encrypt"
    assert crypto.ENCRYPTED_BY_HEADER in encryptfile.read()
    with pytest.raises(JakException) as excencrypted:
        crypto.encrypt_file(jwd=encryptfile.dirpath().strpath, filepath=encryptfile.strpath, key=key)
    assert "already encrypted the file" in str(excencrypted.value)

def test_already_decrypted(tmpdir):
    decryptfile = tmpdir.join("decryptfile")
    decryptfile.write("are we there yet?")
    key = helpers.generate_256bit_key().decode('utf-8')
    assert decryptfile.read() == "are we there yet?"
    out = crypto.decrypt_file(jwd=decryptfile.dirpath().strpath, filepath=decryptfile.strpath, key=key)
    assert out == 'The file "{}" is already decrypted, or is not in a format I recognize.'.format(
            decryptfile.strpath)

def test_wrong_key(tmpdir):
    wrongkey = tmpdir.join("wrongkey")
    wrongkey.write("I have to write this.")
    key = "519c4865ba5aaa0505f95ad4975a7ea3ac07b9ad1842c1c064662a893ae64966"
    crypto.encrypt_file(jwd=wrongkey.dirpath().strpath, filepath=wrongkey.strpath, key=key)
    assert wrongkey.read() != "I have to write this."
    badkey = "519c4865ba5aaa0505f95ad4975a7ea355555555555555555555555555555555"
    with pytest.raises(JakException) as excwrong:
        crypto.decrypt_file(jwd=wrongkey.dirpath().strpath, filepath=wrongkey.strpath, key=badkey)
    assert "Wrong key" in str(excwrong.value)

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
