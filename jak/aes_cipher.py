# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import binascii
from .compat import b
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA512
from .padding import pad, unpad
from .exceptions import JakException, WrongKeyException


class AES256Cipher(object):
    """AES256 using CBC mode and a 16bit block size."""

    def __init__(self, key, mode=AES.MODE_CBC):
        """You can override the mode if you want, But you had better know
        what you are doing."""

        self.cipher = AES
        self.mode = mode
        self.BLOCK_SIZE = AES.block_size
        self.SIG_SIZE = SHA512.digest_size

        # We force the key to be 64 hexdigits (nibbles) because we are sadists.
        key_issue_exception = JakException(
            ("Key must be 64 hexadecimal [0-f] characters long. \n"
             "jak recommends you use the 'keygen' command to generate a strong key."))

        # Long enough?
        if len(key) != 64:
            raise key_issue_exception

        try:
            self.key = binascii.unhexlify(key)
        except TypeError:

            # Not all of them are hexadecimals in all likelihood
            raise key_issue_exception

        # Generate a separate HMAC key. This is (to my understanding) not
        # strictly necessary.
        # But was recommended by Thomas Pornin (http://crypto.stackexchange.com/a/8086)
        self.hmac_key = SHA512.new(data=key).digest()

    def _generate_iv(self):
        """Generates an Initialization Vector (IV).

        This implementation is the currently recommended way of generating an IV
        in PyCrypto's docs (https://www.dlitz.net/software/pycrypto/api/current/)
        """
        return Random.new().read(self.BLOCK_SIZE)

    def _authenticate(self, data, signature):
        """True if key is correct and data has not been tampered with else False"""
        return HMAC.new(key=self.hmac_key, msg=data, digestmod=SHA512).digest() == signature

    def extract_iv(self, ciphertext):
        """Extract the IV"""
        return ciphertext[:self.BLOCK_SIZE]

    def decrypt(self, ciphertext):
        """Decrypts an encrypted secret."""
        signature = ciphertext[-self.SIG_SIZE:]
        iv = self.extract_iv(ciphertext=ciphertext)
        data = ciphertext[self.BLOCK_SIZE:-self.SIG_SIZE]

        if not self._authenticate(data=data, signature=signature):
            raise WrongKeyException('Wrong key OR the encrypted data has been tampered with. Either way I am aborting...')  # noqa

        # Setup cipher and perform actual decryption
        cipher_instance = self.cipher.new(key=self.key, mode=self.mode, IV=iv)
        data_padded = cipher_instance.decrypt(ciphertext=data)
        return unpad(data=data_padded)

    def encrypt(self, plaintext, iv=False):
        """Encrypts a secret"""

        # Convert secret to bytes (FIXME: why not just read it as bytes?)
        plaintext = plaintext.encode()

        if not iv:
            iv = self._generate_iv()

        cipher_instance = self.cipher.new(key=self.key, mode=self.mode, IV=iv)
        plaintext_padded = pad(data=plaintext)
        encrypted_data = cipher_instance.encrypt(plaintext=plaintext_padded)

        signature = HMAC.new(key=self.hmac_key, msg=encrypted_data, digestmod=SHA512).digest()

        # TODO Add Version
        return iv + encrypted_data + signature
