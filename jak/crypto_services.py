# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import base64
import binascii
from io import open
from . import helpers
from .compat import b
from .aes_cipher import AES256Cipher
from .exceptions import JakException, WrongKeyException

ENCRYPTED_BY_HEADER = u'- - - Encrypted by jak - - -\n\n'


def _read_file(filepath):
    """Helper for reading a file and making sure it has content."""
    try:
        with open(filepath, 'rb') as f:
            contents = f.read()
    except IOError:
        raise JakException("Sorry I can't find the file: {}".format(filepath))

    if len(contents) == 0:
        raise JakException('The file "{}" is empty, aborting...'.format(filepath))

    return contents


def _restore_from_backup(jwd, filepath, plaintext, aes256_cipher):
    """Return backup value (if such exists and content in file has not changed)

    We may want to replace this with a simpler "check last modified time" lookup
    that could happen in constant time instead.
    """
    if not helpers.is_there_a_backup(jwd=jwd, filepath=filepath):
        return None

    backup_ciphertext_original = helpers.get_backup_content_for_file(jwd=jwd, filepath=filepath)
    previous_enc = base64.urlsafe_b64decode(b(backup_ciphertext_original))
    iv = aes256_cipher.extract_iv(ciphertext=previous_enc)
    new_secret_w_same_iv = aes256_cipher.encrypt(plaintext=plaintext, iv=iv)

    if new_secret_w_same_iv == previous_enc:
        return backup_ciphertext_original

    return None


def write_ciphertext_to_file(filepath, ciphertext):
    ciphertext = b(ciphertext)
    ciphertext = ciphertext.replace(b'\n', b'')
    encrypted_chunks = helpers.grouper(ciphertext.decode('utf-8'), 60)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ENCRYPTED_BY_HEADER)
        for encrypted_chunk in encrypted_chunks:
            f.write(encrypted_chunk + '\n')


def encrypt_file(jwd, filepath, key, **kwargs):
    """Encrypts a file"""
    plaintext = _read_file(filepath=filepath)

    if b(ENCRYPTED_BY_HEADER) in plaintext:
        raise JakException('I already encrypted the file: "{}".'.format(filepath))

    aes256_cipher = AES256Cipher(key=key)

    ciphertext = _restore_from_backup(jwd=jwd,
                                      filepath=filepath,
                                      plaintext=plaintext,
                                      aes256_cipher=aes256_cipher)

    if not ciphertext:
        ciphertext_ugly = aes256_cipher.encrypt(plaintext=plaintext)

        # Base64 is prettier
        ciphertext = base64.urlsafe_b64encode(ciphertext_ugly)

    write_ciphertext_to_file(filepath=filepath, ciphertext=ciphertext)
    return '{} - is now encrypted.'.format(filepath)


def decrypt_file(filepath, key, jwd, **kwargs):
    """Decrypts a file"""
    original_ciphertext = _read_file(filepath=filepath)

    ciphertext_no_header = original_ciphertext.replace(b(ENCRYPTED_BY_HEADER), b'')

    # Remove the base64 encoding which is applied to make output prettier after encryption.
    try:
        ciphertext = base64.urlsafe_b64decode(ciphertext_no_header)
    except (TypeError, binascii.Error):
        return 'The file "{}" is already decrypted, or is not in a format I recognize.'.format(
            filepath)

    # Remember the encrypted file in the .jak folder
    # The reason to remember is because we don't want re-encryption of files to
    # be different from previous ones if the content has not changed (which it would
    # with a new random IV). This way it works way better with VCS systems like git.
    helpers.backup_file_content(jwd=jwd, filepath=filepath, content=ciphertext_no_header)

    # Perform decryption
    aes256_cipher = AES256Cipher(key=key)
    try:
        decrypted_secret = aes256_cipher.decrypt(ciphertext=ciphertext)
    except WrongKeyException as wke:
        raise JakException('{} - {}'.format(filepath, wke.__str__()))

    with open(filepath, 'wb') as f:
        f.write(decrypted_secret)

    return '{} - is now decrypted.'.format(filepath)
