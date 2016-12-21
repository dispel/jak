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


def encrypt_file(jwd, filepath, key, **kwargs):
    """Encrypts a file"""

    try:
        with open(filepath, 'rt', encoding='utf-8') as f:
            secret = f.read()
    except IOError:
        return "Sorry I can't find the file: {}".format(filepath)

    if len(secret) == 0:
        raise JakException('Hmmmm "{}" seems to be completely empty, skipping...'.format(filepath))

    if ENCRYPTED_BY_HEADER in secret:
        raise JakException('I already encrypted the file: "{}".'.format(filepath))

    # FIXME REFACTOR
    if helpers.is_there_a_backup(jwd=jwd, filepath=filepath):
        backup_encrypted_secret = helpers.get_backup_content_for_file(jwd=jwd, filepath=filepath)
    else:
        backup_encrypted_secret = False

    aes256_cipher = AES256Cipher()
    should_generate_new_secret = True
    if backup_encrypted_secret:
        ugly_backup_encrypted_secret = base64.urlsafe_b64decode(b(backup_encrypted_secret))
        iv = aes256_cipher.extract_iv(encrypted_secret=ugly_backup_encrypted_secret)
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret, iv=iv)

        if encrypted_secret == ugly_backup_encrypted_secret:
            should_generate_new_secret = False

    if should_generate_new_secret:
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret)

    # Prettier
    nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)

    encrypted_chunks = helpers.grouper(nice_enc_secret.decode('utf-8'), 60)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ENCRYPTED_BY_HEADER)
        for encrypted_chunk in encrypted_chunks:
            f.write(encrypted_chunk + '\n')

    return '{} - is now encrypted.'.format(filepath)


def decrypt_file(jwd, filepath, key, **kwargs):
    """Decrypts a file

    FIXME REFACTOR
    This file is doing way too much:
    - choose key
    - open file and read it
    - backup encrypted version
    - decrypt content (probably still a wrapper around the cipher class)
        - remove header
        - b64decode
        - setup->call cipher
    - write back into file
    """
    try:
        with open(filepath, 'rt', encoding='utf-8') as f:
            encrypted_secret = f.read()
    except IOError:
        return "Sorry I can't find the file: {}".format(filepath)

    if len(encrypted_secret) == 0:
        raise JakException('The file "{}" is empty, aborting...'.format(filepath))

    # Remove header.
    encrypted_secret = encrypted_secret.replace(ENCRYPTED_BY_HEADER, '')

    try:
        ugly_encrypted_secret = base64.urlsafe_b64decode(b(encrypted_secret))
    except (TypeError, binascii.Error):
        return 'The file "{}" is already decrypted, or is not in a format I recognize.'.format(
            filepath)

    # Remember the encrypted file in the .jak folder
    # FIXME will this have issues on WINDOWS?
    # The reason to remember is because we don't want a re-encrypt
    # of files to produce new encryptions if nothing has changed (which it would
    # with a new IV). This way it works way better with VCS.
    # import pdb; pdb.set_trace()
    helpers.backup_file_content(jwd, filepath, encrypted_secret)

    # Perform Decrypt
    aes256_cipher = AES256Cipher()
    decrypted_secret = aes256_cipher.decrypt(key=key, encrypted_secret=ugly_encrypted_secret)

    # Write back unencrypted content to the file
    try:
        decrypted_secret_as_string = decrypted_secret.decode('utf-8')
    except UnicodeDecodeError:
        # This happens when the encrypted secret (not the fingerprint part)
        # is edited, basically we decrypt into garbledygook and so the string
        # reader freaks out.
        return 'The output was not what I expected...'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(decrypted_secret_as_string)

    return '{} - is now decrypted.'.format(filepath)
