# -*- coding: utf-8 -*-

"""
jak.crypto_services
---

Logic for performing encryption and decryption
"""

import hmac
import base64
import hashlib
import binascii
from io import open
from Crypto import Random
from .compat import b
from builtins import str as text
from Crypto.Cipher import AES
from .exceptions import JakException
from . import password_services as ps

ENCRYPTED_BY_HEADER = text('- - - Encrypted by jak - - -\n')


class AES256Cipher(object):
    """AES256 using CFB mode and a 16bit block size."""

    def __init__(self, mode=AES.MODE_CFB):
        """You can override the mode if you want, But you had better know
        what you are doing."""

        self.cipher = AES
        self.block_size = AES.block_size
        self.mode = mode

        # Just one of those things.
        self.fingerprint_length = 128
        self.integrity_algorithm = hashlib.sha512

    def _has_integrity(self, key, encrypted_secret, iv):
        """Validate that the fingerprint (HMAC) will match (aka is the password correct?)"""
        existing_fingerprint = encrypted_secret[:self.fingerprint_length]
        new_fingerprint = self._create_integrity_fingerprint(key, iv)
        return b(new_fingerprint) == existing_fingerprint

    def _create_integrity_fingerprint(self, key, iv):
        """Generate a fingerprint during encrypt to check integrity on decrypt

        FIXME
        technically using the same key for integrity checking and decrypting/encrypting
        is not a great idea. but otherwise we are asking users to keep track of two
        separate keys... One option i've been considering is just asking for a really long
        48 character password and use 32 for encrypting/decryption and final 16 for the
        integrity checking...
        """
        fingerprint = hmac.new(b(key), iv, self.integrity_algorithm).hexdigest()
        return b(fingerprint)

    def decrypt(self, key, encrypted_secret):
        """Decrypts an encrypted secret."""
        iv = encrypted_secret[self.fingerprint_length:self.fingerprint_length + self.block_size]
        if not self._has_integrity(key, encrypted_secret, iv):
            raise JakException('Wrong password. Aborting...')

        # Pop the fingerprint off
        encrypted_secret = encrypted_secret[self.fingerprint_length:]

        # Setup cipher and perform actual decryption
        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        decrypted_secret_and_iv = cipher_instance.decrypt(encrypted_secret)
        just_decrypted_secret = decrypted_secret_and_iv[self.block_size:]
        return just_decrypted_secret

    def encrypt(self, key, secret):
        """Encrypts a secret"""
        if len(key) != 32:
            raise JakException(
                ("Password must be exactly 32 characters long. \n"
                 "I would recommend you use the genpass command to generate a strong password."))

        iv = self._generate_iv()

        # For checking the integrity of password on decryption
        fingerprint = self._create_integrity_fingerprint(key, iv)

        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        encrypted_secret = cipher_instance.encrypt(secret)
        return fingerprint + iv + encrypted_secret

    def _generate_iv(self):
        """Generates an Initialization Vector (IV)."""
        return Random.new().read(self.block_size)


def all(callable_action, password, password_file):
    """Read the jakfile and decrypt all the files in it.

    callable_action MUST be one of encrypt_file or decrypt_file (FIXME, throw warning if not?)

    """
    try:
        with open('jakfile', 'rt') as jakfile:
            import json
            contents_raw = jakfile.read()
            contents = json.loads(contents_raw)
    except IOError:
        return 'You need to create a jakfile to use this functionality. Aborting...'

    # TODO test:
    # password_file not in there
    # password_file in there but no value
    # password_file in there and has value
    if contents['password_file']:
        password_file = contents['password_file']

    results = ''
    for index, protected_file in enumerate(contents['protected']):
        try:
            result = callable_action(protected_file, password, password_file)
        except JakException as je:
            result = je.__str__()

        try:
            results += result
        except Exception as e:
            import pdb; pdb.set_trace()

        # Only add newline if we are not on the final one.
        if index + 1 != len(contents['protected']):
            results += '\n'

    return results

def encrypt_file(filename, password, password_file=None):
    """Encrypts a file"""
    try:
        password = ps.get_password(password, password_file)
    except IOError:
        return 'Sorry I can‘t find the password file: {}'.format(password_file)

    try:
        with open(filename, 'rt', encoding='utf-8') as f:
            secret = f.read()
    except IOError:
        return 'Sorry I can‘t find the file: {}'.format(filename)

    if len(secret) == 0:
        raise JakException('The file "{}" is empty, aborting...'.format(filename))

    if ENCRYPTED_BY_HEADER in secret:
        raise JakException('The file "{}" is already encrypted by me.'.format(filename))

    # Encrypt
    aes256_cipher = AES256Cipher()
    encrypted_secret = aes256_cipher.encrypt(key=password, secret=secret)

    # Make it prettier for the file
    nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)

    # Write it to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(ENCRYPTED_BY_HEADER)
        f.write(nice_enc_secret.decode('utf-8'))

    return '{} - is now encrypted.'.format(filename)


def decrypt_file(filename, password, password_file=None):
    """Decrypts a file"""
    password = ps.get_password(password, password_file)

    try:
        with open(filename, 'rt', encoding='utf-8') as f:
            encrypted_secret = f.read()
    except IOError:
        return 'Sorry I can‘t find the file: {}'.format(filename)

    if len(encrypted_secret) == 0:
        raise JakException('The file "{}" is empty, aborting...'.format(filename))

    # Remove header.
    encrypted_secret = encrypted_secret.replace(ENCRYPTED_BY_HEADER, '')

    try:
        encrypted_secret = base64.urlsafe_b64decode(b(encrypted_secret))
    except (TypeError, binascii.Error):
        return 'The file "{}" is already decrypted, or is not in a format I recognize.'.format(filename)

    # Perform Decrypt
    aes256_cipher = AES256Cipher()
    decrypted_secret = aes256_cipher.decrypt(key=password, encrypted_secret=encrypted_secret)

    # Write back unencrypted content to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(decrypted_secret.decode('utf-8'))

    return '{} - is now decrypted.'.format(filename)
