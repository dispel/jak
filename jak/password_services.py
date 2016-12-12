# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
import binascii
from io import open
from .exceptions import JakException


def generate_256bit_key():
    """Generate a secure cryptographically random key."""
    return binascii.hexlify(os.urandom(16))


def select_key(key=None, key_file=None, jakfile_dict=None):
    """Select a password or complain about passing too many.

    Pseudocode:
    REJECT IF NO KEYS
    IF CLI
        REJECT IF 2 KEYS FROM CLI
        PROCEED IF 1 KEY FROM CLI

    REJECT IF 2 KEYS IN JAKFILE
    PROCEED IF 1 KEY IN JAKFILE

    Plaintext: CLI input keys override the jakfiles. Abort if 2 keys from CLI or jakfile.
    """
    if not key and not key_file and not jakfile_dict:
        raise JakException('Please provide some sort of key for encrypting. Aborting...')

    if key and key_file:
        raise JakException('Please only pass me one key to avoid confusion. Aborting... ')

    if key:
        return key

    if key_file:
        try:
            with open(key_file, 'rt', encoding='utf-8') as f:
                key = f.read()
        except IOError:
            raise JakException("Sorry I can't find the key file: {}".format(key_file))
        else:
            key = key.replace('\n', '')
            return key

    if 'key' in jakfile_dict and 'key_file' in jakfile_dict:
        msg = '''Your jakfile should not contain a "key" and a "key_file" value. Choose one.
Aborting...'''
        raise JakException(msg)

    if 'key' in jakfile_dict:
        return jakfile_dict['key']

    if 'key_file' in jakfile_dict:
        filepath = jakfile_dict['key_file']
        try:
            with open(filepath, 'rt', encoding='utf-8') as f:
                key = f.read()
        except IOError:
            raise JakException("Sorry I can't find the key file: {}".format(filepath))
        else:
            key = key.replace('\n', '')
            return key
