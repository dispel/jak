from Crypto.Cipher import AES
from Crypto import Random
import base64
from io import open
import os
import binascii
from .exceptions import JakException
from builtins import str as text
from .compat import bytes

ENCRYPTED_BY_HEADER = text('- - - Encrypted by jak - - -\n')


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

        if len(key) != 32:
            raise JakException(
                ("Password must be exactly 32 characters long. \n"
                 "I would recommend you use the genpass command to generate a strong password."))

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

    with open(filename, 'rt', encoding='utf-8') as f:
        secret = f.read()

        if len(secret) == 0:
            raise JakException('The file "{}" is empty, aborting...'.format(filename))

        aes256_cipher = AES256Cipher()
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret)
        nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)

    with open(filename, 'w', encoding='utf-8') as f:
        # nice_encoded_secret = nice_enc_secret.decode()
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
        # import pdb; pdb.set_trace()
        encrypted_secret = base64.urlsafe_b64decode(bytes(encrypted_secret))
        decrypted_secret = aes256_cipher.decrypt(key=key, encrypted_secret=encrypted_secret)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text(decrypted_secret))
