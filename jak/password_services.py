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


def get_password(cli_password=None, cli_password_file=None, jakfile_dict=None):
    """Select a password or complain about passing too many.

    Pseudocode:
    REJECT IF NO PASSWORDS
    IF CLI
        REJECT IF 2 PASSWORDS FROM CLI
        PROCEED IF 1 PASSWORD FROM CLI

    REJECT IF 2 PASSWORDS IN JAKFILE
    PROCEED IF 1 PASSWORD IN JAKFILE

    Plaintext: CLI input passwords override the jakfiles. Abort if 2 passwords from CLI or jakfile.
    """
    if not cli_password and not cli_password_file and not jakfile_dict:
        raise JakException('Please provide some sort of password for encrypting. Aborting...')

    if cli_password and cli_password_file:
        raise JakException('Please only pass me one password to avoid confusion. Aborting... ')

    if cli_password:
        return cli_password

    if cli_password_file:
        try:
            with open(cli_password_file, 'rt', encoding='utf-8') as f:
                password = f.read()
        except IOError:
            raise JakException("Sorry I can't find the password file: {}".format(cli_password_file))
        else:
            password = password.replace('\n', '')
            return password

    if 'password' in jakfile_dict and 'password_file' in jakfile_dict:
        msg = '''Your jakfile should not contain a "password" and a "password_file" value. Choose one.
Aborting...'''
        raise JakException(msg)

    if 'password' in jakfile_dict:
        return jakfile_dict['password']

    if 'password_file' in jakfile_dict:
        filepath = jakfile_dict['password_file']
        try:
            with open(filepath, 'rt', encoding='utf-8') as f:
                password = f.read()
        except IOError:
            raise JakException("Sorry I can't find the password file: {}".format(filepath))
        else:
            password = password.replace('\n', '')
            return password
