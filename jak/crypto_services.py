# -*- coding: utf-8 -*-

"""
jak.crypto_services
---

Logic for performing encryption and decryption
"""

import base64
import binascii
from io import open
from . import helpers
from .compat import b
from Crypto import Random
from Crypto.Cipher import AES
from .exceptions import JakException
from . import password_services as ps

ENCRYPTED_BY_HEADER = u'- - - Encrypted by jak - - -\n\n'


class AES256Cipher(object):
    """AES256 using CFB mode and a 16bit block size."""

    def __init__(self, mode=AES.MODE_CFB):
        """You can override the mode if you want, But you had better know
        what you are doing."""

        self.cipher = AES
        self.block_size = AES.block_size
        self.mode = mode
        self.fingerprint_length = 128

    def _has_integrity(self, key, encrypted_secret, iv):
        """Validate that the fingerprint (HMAC) will match (aka is the password correct?)"""
        existing_fingerprint = encrypted_secret[:self.fingerprint_length]
        new_fingerprint = self._create_integrity_fingerprint(key, iv)
        return b(new_fingerprint) == existing_fingerprint

    def _old_python_create_integrity_fingerprint(self, password, salt):
        """Used to generate a PBKDF2 HMAC if python version doesn't have a
        pbkdf2_hmac package built in.

        Only reason we keep this is because of old ubuntu LTS. Come 2018 or so
        we can probably remove this. And throw a "upgrade your python plz" message instead.
        https://www.dlitz.net/software/pycrypto/api/current/Crypto.Protocol.KDF-module.html#PBKDF2
        """
        from Crypto.Protocol.KDF import PBKDF2
        from Crypto.Hash import HMAC, SHA512

        def prf(p, s):
            return HMAC.new(key=p, msg=s, digestmod=SHA512).digest()

        return PBKDF2(password=password, salt=salt, count=10000, prf=prf,
                      dkLen=int(self.fingerprint_length / 2))

    def _create_integrity_fingerprint(self, key, iv):
        """Generate a fingerprint during encrypt to check integrity on decrypt
        uses PBKDF2 (PKCS #5 v2.0)

        for more info see source code here:
        https://hg.python.org/cpython/file/2.7/Lib/hashlib.py
        """
        try:
            from hashlib import pbkdf2_hmac
        except ImportError:

            # Must be on python older than 2.7.8...
            digest = self._old_python_pbkdf2(password=b(key), salt=iv)
        else:
            digest = pbkdf2_hmac(hash_name='SHA512', password=b(key),
                                 salt=iv, iterations=10000)

        fingerprint = binascii.hexlify(digest)
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


def all(callable_action, password, password_file, jakfile_dict):
    """Read the jakfile and decrypt all the files in it.

    callable_action MUST be one of encrypt_file or decrypt_file (FIXME, throw warning if not?)

    """
    password = ps.get_password(password, password_file, jakfile_dict)

    results = ''
    for index, protected_file in enumerate(jakfile_dict['protected_files']):
        try:
            result = callable_action(protected_file, password, password_file)
        except JakException as je:
            result = je.__str__()

        results += result

        # Only add newline if we are not on the last protected file.
        if index + 1 != len(jakfile_dict['protected_files']):
            results += '\n'

    return results


def encrypt_file(filename, password, password_file=None, jakfile_dict=None):
    """Encrypts a file"""
    password = ps.get_password(password, password_file, jakfile_dict)

    try:
        with open(filename, 'rt', encoding='utf-8') as f:
            secret = f.read()
    except IOError:
        return "Sorry I can't find the file: {}".format(filename)

    if len(secret) == 0:
        raise JakException('Hmmmm "{}" seems to be completely empty, skipping...'.format(filename))

    if ENCRYPTED_BY_HEADER in secret:
        raise JakException('I already encrypted the file: "{}".'.format(filename))

    # Encrypt
    aes256_cipher = AES256Cipher()
    encrypted_secret = aes256_cipher.encrypt(key=password, secret=secret)

    # Make it prettier for the file
    nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)
    encrypted_chunks = helpers.grouper(nice_enc_secret.decode('utf-8'), 60)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(ENCRYPTED_BY_HEADER)
        for encrypted_chunk in encrypted_chunks:
            f.write(encrypted_chunk + '\n')

    return '{} - is now encrypted.'.format(filename)


def decrypt_file(filename, password, password_file=None, jakfile_dict=None):
    """Decrypts a file"""
    password = ps.get_password(password, password_file, jakfile_dict)

    try:
        with open(filename, 'rt', encoding='utf-8') as f:
            encrypted_secret = f.read()
    except IOError:
        return "Sorry I can't find the file: {}".format(filename)

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
