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


def diff(filepath, key=None, key_file=None, jakfile_dict=None):
    """"""
    if not jakfile_dict:
        jakfile_dict = helpers.read_jakfile_to_dict()

    key = ps.select_key(key=key, key_file=key_file, jakfile_dict=jakfile_dict)

    with open(filepath, 'rt') as f:
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

    # import pdb; pdb.set_trace()

    decrypted_local = decrypted_local.decode('utf-8').rstrip('\n')
    decrypted_remote = decrypted_remote.decode('utf-8').rstrip('\n')

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

    # Python 3 does not have a decode for this
    # but it doesn't need to perform the decode so all is well here.
    # Obviously once we give up on python 2 we won't have to
    # do horrible stuff like this anymore.
    try:
        output = output.decode('utf-8')
    except AttributeError:
        pass

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)
