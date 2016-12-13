# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

from . import crypto_services as cs
from . import password_services as ps
from . import helpers
import base64
from .compat import b
from io import open


def diff(filename, key=None):
    """"""
    if not key:
        jakfile_dict = helpers.read_jakfile_to_dict()
        key = ps.select_key(jakfile_dict=jakfile_dict)

    with open(filename, 'rt') as f:
        encrypted_diff_file = f.read()

    # Strip the header
    tmp = encrypted_diff_file.replace(cs.ENCRYPTED_BY_HEADER, '')

    # Cleanup and waypoints
    tmp = tmp.replace('- - - Encrypted by jak - - -', '')
    tmp = tmp.rstrip('\n')
    git_start = '<<<<<<< HEAD'
    git_middle = '======='
    git_end = tmp[tmp.rfind('>>>>>>>'):].rstrip()

    local = tmp[tmp.find(git_start) + len(git_start):tmp.find(git_middle)]
    remote = tmp[tmp.find(git_middle) + len(git_middle):tmp.find(git_end)]

    ugly_local = base64.urlsafe_b64decode(b(local))
    ugly_remote = base64.urlsafe_b64decode(b(remote))

    aes256_cipher = cs.AES256Cipher()
    decrypted_local = aes256_cipher.decrypt(key=key, encrypted_secret=ugly_local)
    decrypted_remote = aes256_cipher.decrypt(key=key, encrypted_secret=ugly_remote)
    decrypted_local = decrypted_local.rstrip('\n')
    decrypted_remote = decrypted_remote.rstrip('\n')

    output = '''
{git_start}
{decrypted_local}
{git_middle}
{decrypted_remote}
{git_end}
'''.format(git_start=git_start,
           decrypted_local=decrypted_local,
           git_middle=git_middle,
           decrypted_remote=decrypted_remote,
           git_end=git_end)

    output = output.decode('utf-8')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(output)
