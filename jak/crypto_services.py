import os
import hmac
import base64
import hashlib
import binascii
from io import open
from Crypto import Random
from .compat import bytes
from builtins import str as text
from Crypto.Cipher import AES
from .exceptions import JakException

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
        self.HMAC_length = 128
        self.integrity_algorithm = hashlib.sha512

    def has_integrity(self, key, encrypted_secret, iv):
        """Validate that the fingerprints (HMACs) will match (aka is the password correct?)"""
        existing_fingerprint = encrypted_secret[:self.HMAC_length]
        new_fingerprint = self.create_integrity_fingerprint(key, iv)
        return new_fingerprint == existing_fingerprint

    def create_integrity_fingerprint(self, key, iv):
        """Generate an hmac to as to check integrity"""
        return hmac.new(bytes(key), iv, self.integrity_algorithm).hexdigest()

    def decrypt(self, key, encrypted_secret):
        """Decrypts an encrypted secret."""
        iv = encrypted_secret[self.HMAC_length:self.HMAC_length + self.block_size]
        if not self.has_integrity(key, encrypted_secret, iv):
            raise JakException('Wrong password. Aborting...')

        # pop the HMAC off
        encrypted_secret = encrypted_secret[self.HMAC_length:]

        # Setup cipher and perform actual decryption
        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        return cipher_instance.decrypt(encrypted_secret)[self.block_size:]

    def encrypt(self, key, secret):
        """Encrypts a secret"""
        if len(key) != 32:
            raise JakException(
                ("Password must be exactly 32 characters long. \n"
                 "I would recommend you use the genpass command to generate a strong password."))

        iv = self.generate_iv()

        # For checking the integrity of password on decryption
        fingerprint = self.create_integrity_fingerprint(key, iv)

        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        return fingerprint + iv + cipher_instance.encrypt(secret)

    def generate_iv(self):
        """Generates an Initialization Vector (IV)."""
        return Random.new().read(self.block_size)


def generate_256bit_key():
    """Generate a secure password key."""
    return binascii.hexlify(os.urandom(16))


def encrypt_file(key, filename):
    """Encrypts a file"""
    with open(filename, 'rt', encoding='utf-8') as f:
        secret = f.read()

        if len(secret) == 0:
            raise JakException('The file "{}" is empty, aborting...'.format(filename))

        if ENCRYPTED_BY_HEADER in secret:
            raise JakException('The file "{}" is already encrypted by me. Aborting...'.format(filename))

        aes256_cipher = AES256Cipher()
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret)
        nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(ENCRYPTED_BY_HEADER)
        f.write(text(nice_enc_secret))


def decrypt_file(key, filename):
    """Decrypts a file"""
    with open(filename, 'rt', encoding='utf-8') as f:
        encrypted_secret = f.read()

        if len(encrypted_secret) == 0:
            raise JakException('The file "{}" is empty, aborting...'.format(filename))

        aes256_cipher = AES256Cipher()
        encrypted_secret = encrypted_secret.replace(ENCRYPTED_BY_HEADER, '')
        encrypted_secret = base64.urlsafe_b64decode(bytes(encrypted_secret))
        decrypted_secret = aes256_cipher.decrypt(key=key, encrypted_secret=encrypted_secret)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text(decrypted_secret))
