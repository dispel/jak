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


def generate_256bit_key():
    """Generate a secure password key."""
    return binascii.hexlify(os.urandom(16))

def check_password_type(password, password_file):
    """Will check to see if password is a string or read in from file"""
    if password and password_file:
        raise JakException('Cannot pass both a password and password_file. Aborting...')

    if password:
        return password

    if password_file:
        with open(password_file, 'rt', encoding='utf-8') as f:
            password = f.read()
            password = password.replace('\n', '')
        return password

    if not password and not password_file:
        raise JakException('Please provide a password or password_file. Aborting...')
