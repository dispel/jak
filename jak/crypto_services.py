from Crypto.Cipher import AES
from Crypto import Random
# from .padding import pad32, PKCS7_16, unPKCS7_16
import base64
from io import open


class AES256Cipher(object):
    """
    http://stackoverflow.com/questions/1220751/how-to-choose-an-aes-encryption-mode-cbc-ecb-ctr-ocb-cfb
    """

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


def encrypt_file(key, filename):
    """Encrypts a file"""
    with open(filename, 'rt') as f:
        secret = f.read()
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

    # TODO
    # if cant find file should raise FileNotFoundError

    with open(filename, 'rt') as f:
        encrypted_secret = f.read()
        aes256_cipher = AES256Cipher()
        encrypted_secret = base64.urlsafe_b64decode(encrypted_secret.encode())
        decrypted_secret = aes256_cipher.decrypt(key=key, encrypted_secret=encrypted_secret)

    with open(filename, 'w') as f:
        f.write(decrypted_secret.decode())
