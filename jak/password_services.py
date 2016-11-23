# -*- coding: utf-8 -*-

"""
jak.password_services
---

logic related to passwords.
"""

import os
import binascii
from io import open
from .exceptions import JakException


def generate_256bit_key():
    """Generate a secure password key."""
    return binascii.hexlify(os.urandom(16))


def get_password(password, password_file):
    """Will check to see if password is a string or read in from file
    returns the password.
    """
    if password and password_file:
        raise JakException('Cannot pass both a --password and --password-file. Aborting...')

    if password:
        return password

    if password_file:
        with open(password_file, 'rt', encoding='utf-8') as f:
            password = f.read()
            password = password.replace('\n', '')
        return password

    if not password and not password_file:
        raise JakException('Please provide a password or password_file. Aborting...')
