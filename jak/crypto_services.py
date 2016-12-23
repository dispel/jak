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
from .exceptions import JakException

ENCRYPTED_BY_HEADER = u'- - - Encrypted by jak - - -\n\n'


def _read_file(filepath):
    """Helper for reading a file and making sure it has content."""
    try:
        with open(filepath, 'rt', encoding='utf-8') as f:
            contents = f.read()
    except IOError:
        raise JakException("Sorry I can't find the file: {}".format(filepath))

    if len(contents) == 0:
        raise JakException('The file "{}" is empty, aborting...'.format(filepath))

    return contents


def _restore_from_backup(jwd, filepath, secret, aes256_cipher):
    """Return backup value (if such exists and content in file has not changed)

    We may want to replace this with a simpler "check last modified time" lookup
    that could happen in constant time instead.
    """
    if helpers.is_there_a_backup(jwd=jwd, filepath=filepath):
        backup_encrypted_secret = helpers.get_backup_content_for_file(jwd=jwd, filepath=filepath)
        previous_enc = base64.urlsafe_b64decode(b(backup_encrypted_secret))
        iv = aes256_cipher.extract_iv(encrypted_secret=previous_enc)
        new_secret_w_same_iv = aes256_cipher.encrypt(key=key, secret=secret, iv=iv)

        if new_secret_w_same_iv == previous_enc:
            return backup_encrypted_secret

    return None


def write_secret_to_file(filepath, nice_enc_secret):
    encrypted_chunks = helpers.grouper(nice_enc_secret.decode('utf-8'), 60)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ENCRYPTED_BY_HEADER)
        for encrypted_chunk in encrypted_chunks:
            f.write(encrypted_chunk + '\n')


def encrypt_file(jwd, filepath, key, **kwargs):
    """Encrypts a file"""
    secret = _read_file(filepath=filepath)

    if ENCRYPTED_BY_HEADER in secret:
        raise JakException('I already encrypted the file: "{}".'.format(filepath))

    aes256_cipher = AES256Cipher()

    # Try to restore from backup.
    nice_enc_secret = _restore_from_backup(jwd=jwd,
                                           filepath=filepath,
                                           secret=secret,
                                           aes256_cipher=aes256_cipher)

    if not nice_enc_secret:
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret)

        # Base64 is prettier
        nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)

    write_secret_to_file(filepath=filepath, nice_enc_secret=nice_enc_secret)
    return '{} - is now encrypted.'.format(filepath)


def decrypt_file(filepath, key, jwd, **kwargs):
    """Decrypts a file"""
    encrypted_secret = _read_file(filepath=filepath)

    # Remove header.
    encrypted_secret = encrypted_secret.replace(ENCRYPTED_BY_HEADER, '')

    # Remove the base64 encoding which is applied to make output prettier after encryption.
    try:
        ugly_encrypted_secret = base64.urlsafe_b64decode(b(encrypted_secret))
    except (TypeError, binascii.Error):
        return 'The file "{}" is already decrypted, or is not in a format I recognize.'.format(
            filepath)

    # Remember the encrypted file in the .jak folder
    # The reason to remember is because we don't want re-encryption of files to
    # be different from previous ones if the content has notchanged (which it would
    # with a new random IV). This way it works way better with VCS systems like git.
    helpers.backup_file_content(jwd=jwd, filepath=filepath, content=encrypted_secret)

    # Perform decryption
    aes256_cipher = AES256Cipher()
    decrypted_secret = aes256_cipher.decrypt(key=key, encrypted_secret=ugly_encrypted_secret)

    # Write back unencrypted content to the file
    try:
        decrypted_secret_as_string = decrypted_secret.decode('utf-8')
    except UnicodeDecodeError:

        # This happens when the encrypted secret (not the fingerprint part)
        # is edited, basically we decrypt into garbledygook and so the string
        # reader freaks out.
        return 'The encrypted content is malformatted and I cannot decrypt it.'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(decrypted_secret_as_string)

    return '{} - is now decrypted.'.format(filepath)
