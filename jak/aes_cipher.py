# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import binascii
from .compat import b
from Crypto import Random
from Crypto.Cipher import AES
from .exceptions import JakException


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
        """Validate that the fingerprint (HMAC) will match (aka is the key correct?)"""
        existing_fingerprint = encrypted_secret[:self.fingerprint_length]
        new_fingerprint = self._create_integrity_fingerprint(key, iv)
        return b(new_fingerprint) == existing_fingerprint

    def _old_python_create_integrity_fingerprint(self, key, salt):
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

        return PBKDF2(password=key, salt=salt, count=10000, prf=prf,
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
            digest = self._old_python_create_integrity_fingerprint(key=b(key), salt=iv)
        else:
            digest = pbkdf2_hmac(hash_name='SHA512', password=b(key),
                                 salt=iv, iterations=10000)

        fingerprint = binascii.hexlify(digest)
        return b(fingerprint)

    def extract_iv(self, encrypted_secret):
        """Extract the IV"""
        return encrypted_secret[self.fingerprint_length:self.fingerprint_length + self.block_size]

    def decrypt(self, key, encrypted_secret):
        """Decrypts an encrypted secret."""
        key = binascii.unhexlify(key)
        iv = self.extract_iv(encrypted_secret)
        if not self._has_integrity(key, encrypted_secret, iv):
            raise JakException('Wrong key. Aborting...')

        # Pop the fingerprint off
        encrypted_secret = encrypted_secret[self.fingerprint_length:]

        # Setup cipher and perform actual decryption
        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        decrypted_secret_and_iv = cipher_instance.decrypt(encrypted_secret)
        just_decrypted_secret = decrypted_secret_and_iv[self.block_size:]
        return just_decrypted_secret

    def encrypt(self, key, secret, iv=False):
        """Encrypts a secret"""
        if len(key) != 64:
            raise JakException(
                ("Key must be exactly 64 characters long. \n"
                 "I would recommend you use the keygen command to generate a strong key."))

        # Reduce the 64 hex digits to be 32 bytechars
        key = binascii.unhexlify(key)

        if not iv:
            iv = self._generate_iv()

        # For checking the integrity of key on decryption
        fingerprint = self._create_integrity_fingerprint(key, iv)

        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        encrypted_secret = cipher_instance.encrypt(secret)
        return fingerprint + iv + encrypted_secret

    def _generate_iv(self):
        """Generates an Initialization Vector (IV)."""
        return Random.new().read(self.block_size)
