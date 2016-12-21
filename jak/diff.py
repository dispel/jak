# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
import re
import click
import base64
import random
import binascii
import subprocess
from io import open
from . import helpers
from .compat import b
from .aes_cipher import AES256Cipher
from .exceptions import JakException
from . import decorators


def _create_local_remote_diff_files(filepath, local, remote):
    """
    Generates two files for use with diffing.

    <f>_LOCAL_<randint>.<ext>
    <f>_REMOTE_<randint>.<ext>

    Returns their paths as a tuple
    """
    tag = random.randrange(10000, 99999)
    (filepath, ext) = os.path.splitext(filepath)
    local_file_path = '{}_LOCAL_{}{}'.format(filepath, tag, ext)
    remote_file_path = '{}_REMOTE_{}{}'.format(filepath, tag, ext)

    helpers.create_or_overwrite_file(filepath=local_file_path, content=local)
    helpers.create_or_overwrite_file(filepath=remote_file_path, content=remote)
    return local_file_path, remote_file_path


def _vimdiff(filepath, local_file_path, remote_file_path):
    """
    Tried for a ludicrous amount of time to get it to open vimdiff automagically.
    Instead we settled on just letting user know what command they should run.
    """
    command = "vimdiff -f -d -c 'wincmd J' {merged} {local} {remote}".format(
        merged=filepath, local=local_file_path, remote=remote_file_path)

    return '''

~*Currently under development*~

To open the diff use this command:
$> {}'''.format(command)


def _opendiff(filepath, local_file_path, remote_file_path):
    """"""
    # Write to devnull so user doesnt see a bunch of messages.
    # FIXME put in logfile instead?
    FNULL = open(os.devnull, 'w')
    subprocess.Popen(['opendiff', local_file_path, remote_file_path, '-merge', filepath],
                     stdout=FNULL,
                     stderr=subprocess.STDOUT)
    return "Opened opendiff."


def _decrypt(key, local, remote):
    """
    TODO
    why not just use crypto libraries decrypt here instead?
    """
    try:
        ugly_local = base64.urlsafe_b64decode(b(local))
        ugly_remote = base64.urlsafe_b64decode(b(remote))
    except binascii.Error:
        msg = '''Failed during decryption. Are you sure the file you are pointing to is jak encrypted?

For example:
<<<<<<< SOMETHING
<some local like: asfs6e024f69113940ead0
19e7dc63e7eee99fb5db2ae37352c1d5de8643a3
f78ae736ae4027fae2acc1530a356dc6d1e360ca
cyz>
=======
<some remote like: asf6e024f69113940ead0
ff9790b8cccd50e1276c4b9ac18475d4e048f2e0
4e0034e782b64b1c9e1ac8c1cb81c3b4e43cb93f
cyz>
>>>>>>> SOMETHING'''
        raise JakException(msg)

    aes256_cipher = AES256Cipher()
    decrypted_local = aes256_cipher.decrypt(key=key, encrypted_secret=ugly_local)
    decrypted_remote = aes256_cipher.decrypt(key=key, encrypted_secret=ugly_remote)

    decrypted_local = decrypted_local.decode('utf-8').rstrip('\n')
    decrypted_remote = decrypted_remote.decode('utf-8').rstrip('\n')
    return decrypted_local, decrypted_remote


def _extract_merge_conflict_parts(content):
    regex = re.compile(r'(<<<<<<<\s\S+.)(.+)(=======.)(.+)(>>>>>>>\s\S+.)', re.DOTALL)
    return regex.findall(content)[0]


@decorators.read_jakfile
@decorators.select_key
def diff(filepath, key, **kwargs):
    """Diff and merge a file that has a merge conflict."""
    with open(filepath, 'rt') as f:
        encrypted_diff_file = f.read()

    (header, local, separator, remote, end) = _extract_merge_conflict_parts(encrypted_diff_file)
    (decrypted_local, decrypted_remote) = _decrypt(key, local, remote)

    output = '''{header}{local}
{separator}{remote}
{end}'''.format(
        header=header,
        local=decrypted_local,
        separator=separator,
        remote=decrypted_remote,
        end=end)

    # Python 3 does not have a decode for this
    # but it doesn't need to perform the decode so all is well here.
    # Obviously once we give up on python 2 we won't have to
    # do horrible stuff like this anymore.
    try:
        output = output.decode('utf-8')
    except AttributeError:
        pass

    msg = '''Which editor do you want to use?
plain (default): will simply decrypt the contents of the original file.
opendiff: The macOS default merge tool.
vimdiff: Hacker 4 life yo!

[plain, opendiff, vimdiff]'''
    response = click.prompt(msg, default='plain')

    if response == 'opendiff':
        (local_file_path, remote_file_path) = _create_local_remote_diff_files(
            filepath=filepath,
            local=decrypted_local,
            remote=decrypted_remote)
        result = _opendiff(filepath=filepath,
                           local_file_path=local_file_path,
                           remote_file_path=remote_file_path)
    elif response == 'vimdiff':
        (local_file_path, remote_file_path) = _create_local_remote_diff_files(
            filepath=filepath,
            local=decrypted_local,
            remote=decrypted_remote)
        result = _vimdiff(filepath=filepath,
                          local_file_path=local_file_path,
                          remote_file_path=remote_file_path)
    elif response == 'plain':
        result = "Ok, file decrypted, go ahead an edit it manually. Godspeed you master of the universe."
    else:
        return "Unrecognized choice. Aborting without changing anything."

    # Replace the original file with the decrypted output
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)

    return result
