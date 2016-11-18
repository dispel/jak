from Crypto.Cipher import AES
from Crypto import Random
import base64
from io import open
import os
import binascii
from .exceptions import JakException


class AES256Cipher(object):
    """AES256 using CFB mode and a 16bit block size."""

    def __init__(self, mode=AES.MODE_CFB):
        """You can override the mode if you want, But you had better know
        what you are doing."""

        self.cipher = AES
        self.block_size = AES.block_size
        self.mode = mode

    def decrypt(self, key, encrypted_secret):
        """Decrypts an encrypted secret.
        both key and encrypted_secret should be bytestrings
        """

        iv = encrypted_secret[:self.block_size]
        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        return cipher_instance.decrypt(encrypted_secret)[self.block_size:]

    def encrypt(self, key, secret):
        """Encrypts a secret piece of text
        both key and secret should be bytestrings
        """

        iv = self.generate_iv()
        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)

        # FIXME ask crypto expert whether attaching IV like this is ok.
        return iv + cipher_instance.encrypt(secret)

    def generate_iv(self):
        """Generates an Initialization Vector (IV)"""

        return Random.new().read(self.block_size)


def generate_256bit_key():
    """Generate a secure password key for people"""

    return binascii.hexlify(os.urandom(16))


def encrypt_file(key, filename):
    """Encrypts a file"""

    with open(filename, 'rt') as f:
        secret = f.read()

        if len(secret) == 0:
            raise JakException('The file "{}" is empty, aborting...'.format(filename))

        aes256_cipher = AES256Cipher()
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret)
        nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)

    with open(filename, 'w') as f:
        try:
            nice_encoded_secret = nice_enc_secret.decode()
            f.write(nice_encoded_secret)
        except Exception as e:
            print("oh shit rolling back file")
            f.write(secret)


def decrypt_file(key, filename):
    """Decrypts a file"""

    with open(filename, 'rt') as f:
        encrypted_secret = f.read()
        aes256_cipher = AES256Cipher()
        encrypted_secret = base64.urlsafe_b64decode(encrypted_secret.encode())
        decrypted_secret = aes256_cipher.decrypt(key=key, encrypted_secret=encrypted_secret)

    with open(filename, 'w') as f:
        f.write(decrypted_secret.decode())
