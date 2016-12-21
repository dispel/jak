# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
from io import open
from . import helpers
from functools import wraps
from .exceptions import JakException


def _select_files_logic(**kwargs):
    if kwargs['all_or_filepath'] == 'all':
        filepaths = kwargs['jakfile_dict']['files_to_encrypt']
    else:
        filepaths = [kwargs['all_or_filepath']]

    files = []
    for fp in filepaths:

        # Some OS expand this out automagically but in case one doesnt...
        if fp[0] == '~':
            fp = fp.replace('~', os.path.expanduser('~'))
        files.append(os.path.abspath(fp))
    return files


def select_files(f):
    """Select which files you want to act upon"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        kwargs['files'] = _select_files_logic(**kwargs)
        return f(*args, **kwargs)
    return wrapper


def attach_jwd(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        kwargs['jwd'] = helpers.get_jak_working_directory()
        return f(*args, **kwargs)
    return wrapper


def read_jakfile(f):
    """Parse the jakfile and assign it to the jakfile_dict value"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            kwargs['jakfile_dict'] = helpers.read_jakfile_to_dict()
        except IOError:
            kwargs['jakfile_dict'] = {}
        return f(*args, **kwargs)
    return wrapper


def select_key(f):
    """Let's find your key champ!"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        kwargs['key'] = select_key_logic(key=kwargs['key'],
                                         keyfile=kwargs['keyfile'],
                                         jakfile_dict=kwargs['jakfile_dict'])
        result = f(*args, **kwargs)
        return result
    return wrapper


def select_key_logic(key=None, keyfile=None, jakfile_dict=None):
    """Select a password or complain about passing too many.

    Pseudocode:
    REJECT IF NO KEYS
    IF CLI
        REJECT IF 2 KEYS FROM CLI
        PROCEED IF 1 KEY FROM CLI

    GET FROM KEYFILE

    Plaintext: CLI input keys override the jakfiles. Abort if 2 keys from CLI.
    """

    # Take from them everything, give to them nothing!
    msg = '''Please provide a key in one of the three ways:
1. -k <key>
2. -kf <keyfile path>
3. "keyfile" value in your jakfile (recommended)'''
    try:
        if not key and not keyfile and 'keyfile' not in jakfile_dict:
            raise JakException(msg)
    except TypeError:
        raise JakException(msg)

    if key and keyfile:
        raise JakException('Please only pass me one key to avoid confusion. Aborting... ')

    if key:
        return key

    if keyfile:
        try:
            with open(keyfile, 'rt', encoding='utf-8') as f:
                key = f.read()
        except IOError:
            raise JakException("Sorry I can't find the key file: {}".format(keyfile))
        else:
            key = key.replace('\n', '')
            return key

    # At this point they must have supplied a keyfile value in their jakfile
    filepath = jakfile_dict['keyfile']
    try:
        with open(filepath, 'rt', encoding='utf-8') as f:
            key = f.read()
    except IOError:
        raise JakException("Sorry I can't find the key file: {}".format(filepath))
    else:
        key = key.replace('\n', '')
        return key
