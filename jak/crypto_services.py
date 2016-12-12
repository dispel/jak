# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import base64
import binascii
from io import open
from . import helpers
from .compat import b
from Crypto import Random
from Crypto.Cipher import AES
from .exceptions import JakException
from . import password_services as ps

ENCRYPTED_BY_HEADER = u'- - - Encrypted by jak - - -\n\n'


class AES256Cipher(object):
    """AES256 using CFB mode and a 16bit block size."""

    def __init__(self, mode=AES.MODE_CFB):
        """You can override the mode if you want, But you had better know
        what you are doing."""

        self.cipher = AES
        self.block_size = AES.block_size
        self.mode = mode
        self.fingerprint_length = 128

    def _has_integrity(self, key, encrypted_secret, iv):
        """Validate that the fingerprint (HMAC) will match (aka is the key correct?)"""
        existing_fingerprint = encrypted_secret[:self.fingerprint_length]
        new_fingerprint = self._create_integrity_fingerprint(key, iv)
        return b(new_fingerprint) == existing_fingerprint

    def _old_python_create_integrity_fingerprint(self, key, salt):
        """Used to generate a PBKDF2 HMAC if python version doesn't have a
        pbkdf2_hmac package built in.

        Only reason we keep this is because of old ubuntu LTS. Come 2018 or so
        we can probably remove this. And throw a "upgrade your python plz" message instead.
        https://www.dlitz.net/software/pycrypto/api/current/Crypto.Protocol.KDF-module.html#PBKDF2
        """
        from Crypto.Protocol.KDF import PBKDF2
        from Crypto.Hash import HMAC, SHA512

        def prf(p, s):
            return HMAC.new(key=p, msg=s, digestmod=SHA512).digest()

        return PBKDF2(password=key, salt=salt, count=10000, prf=prf,
                      dkLen=int(self.fingerprint_length / 2))

    def _create_integrity_fingerprint(self, key, iv):
        """Generate a fingerprint during encrypt to check integrity on decrypt
        uses PBKDF2 (PKCS #5 v2.0)

        for more info see source code here:
        https://hg.python.org/cpython/file/2.7/Lib/hashlib.py
        """
        try:
            from hashlib import pbkdf2_hmac
        except ImportError:

            # Must be on python older than 2.7.8...
            digest = self._old_python_create_integrity_fingerprint(key=b(key), salt=iv)
        else:
            digest = pbkdf2_hmac(hash_name='SHA512', password=b(key),
                                 salt=iv, iterations=10000)

        fingerprint = binascii.hexlify(digest)
        return b(fingerprint)

    def extract_iv(self, encrypted_secret):
        """Extract the IV"""
        return encrypted_secret[self.fingerprint_length:self.fingerprint_length + self.block_size]

    def decrypt(self, key, encrypted_secret):
        """Decrypts an encrypted secret."""
        iv = self.extract_iv(encrypted_secret)
        if not self._has_integrity(key, encrypted_secret, iv):
            raise JakException('Wrong key. Aborting...')

        # Pop the fingerprint off
        encrypted_secret = encrypted_secret[self.fingerprint_length:]

        # Setup cipher and perform actual decryption
        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        decrypted_secret_and_iv = cipher_instance.decrypt(encrypted_secret)
        just_decrypted_secret = decrypted_secret_and_iv[self.block_size:]
        return just_decrypted_secret

    def encrypt(self, key, secret, iv=False):
        """Encrypts a secret"""
        if len(key) != 32:
            raise JakException(
                ("Key must be exactly 32 characters long. \n"
                 "I would recommend you use the genpass command to generate a strong key."))

        if not iv:
            iv = self._generate_iv()

        # For checking the integrity of key on decryption
        fingerprint = self._create_integrity_fingerprint(key, iv)

        cipher_instance = self.cipher.new(key=key, mode=self.mode, IV=iv)
        encrypted_secret = cipher_instance.encrypt(secret)
        return fingerprint + iv + encrypted_secret

    def _generate_iv(self):
        """Generates an Initialization Vector (IV)."""
        return Random.new().read(self.block_size)


def all(callable_action, key, key_file, jakfile_dict):
    """Read the jakfile and decrypt all the files in it.

    callable_action MUST be one of encrypt_file or decrypt_file (FIXME, throw warning if not?)
    """
    key = ps.select_key(key, key_file, jakfile_dict)

    try:
        files_to_encrypt = jakfile_dict['files_to_encrypt']
    except KeyError:
        raise JakException('This command requires a jakfile with a "files_to_encrypt" value.\nAborting...')
    else:
        if not isinstance(files_to_encrypt, list):
            raise JakException("The jakfile's \"files_to_encrypt\" value must be a list (array).\nAborting...")

        if not files_to_encrypt:
            msg = '''Your jakfile's files_to_encrypt value is empty. It should be a list of files.
Aborting...'''
            raise JakException(msg)

    results = ''
    for index, protected_file in enumerate(files_to_encrypt):
        try:
            result = callable_action(protected_file, key, key_file)
        except JakException as je:
            result = je.__str__()

        results += result

        # Only add newline if we are not on the last protected file.
        if index + 1 != len(jakfile_dict['files_to_encrypt']):
            results += '\n'

    return results


def encrypt_file(filepath, key, key_file=None, jakfile_dict=None):
    """Encrypts a file"""
    key = ps.select_key(key, key_file, jakfile_dict)

    try:
        with open(filepath, 'rt', encoding='utf-8') as f:
            secret = f.read()
    except IOError:
        return "Sorry I can't find the file: {}".format(filepath)

    if len(secret) == 0:
        raise JakException('Hmmmm "{}" seems to be completely empty, skipping...'.format(filepath))

    if ENCRYPTED_BY_HEADER in secret:
        raise JakException('I already encrypted the file: "{}".'.format(filepath))

    # FIXME REFACTOR
    if helpers.is_there_a_backup(filepath):
        backup_encrypted_secret = helpers.get_backup_content_for_file(filepath)
    else:
        backup_encrypted_secret = False

    aes256_cipher = AES256Cipher()
    should_generate_new_secret = True
    if backup_encrypted_secret:
        ugly_backup_encrypted_secret = base64.urlsafe_b64decode(b(backup_encrypted_secret))
        iv = aes256_cipher.extract_iv(encrypted_secret=ugly_backup_encrypted_secret)
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret, iv=iv)

        if encrypted_secret == ugly_backup_encrypted_secret:
            should_generate_new_secret = False

    if should_generate_new_secret:
        encrypted_secret = aes256_cipher.encrypt(key=key, secret=secret)

    # Prettier
    nice_enc_secret = base64.urlsafe_b64encode(encrypted_secret)

    encrypted_chunks = helpers.grouper(nice_enc_secret.decode('utf-8'), 60)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ENCRYPTED_BY_HEADER)
        for encrypted_chunk in encrypted_chunks:
            f.write(encrypted_chunk + '\n')

    return '{} - is now encrypted.'.format(filepath)


def decrypt_file(filepath, key, key_file=None, jakfile_dict=None):
    """Decrypts a file

    FIXME REFACTOR
    This file is doing way too much:
    - choose key
    - open file and read it
    - backup encrypted version
    - decrypt content (probably still a wrapper around the cipher class)
        - remove header
        - b64decode
        - setup->call cipher
    - write back into file
    """
    key = ps.select_key(key, key_file, jakfile_dict)

    try:
        with open(filepath, 'rt', encoding='utf-8') as f:
            encrypted_secret = f.read()
    except IOError:
        return "Sorry I can't find the file: {}".format(filepath)

    if len(encrypted_secret) == 0:
        raise JakException('The file "{}" is empty, aborting...'.format(filepath))

    # Remove header.
    encrypted_secret = encrypted_secret.replace(ENCRYPTED_BY_HEADER, '')

    try:
        ugly_encrypted_secret = base64.urlsafe_b64decode(b(encrypted_secret))
    except (TypeError, binascii.Error):
        return 'The file "{}" is already decrypted, or is not in a format I recognize.'.format(filepath)

    # Remember the encrypted file in the .jak folder
    # FIXME will this have issues on WINDOWS?
    # The reason to remember is because we don't want a re-encrypt
    # of files to produce new encryptions if nothing has changed (which it would
    # with a new IV). This way it works way better with VCS.
    # import pdb; pdb.set_trace()
    helpers.backup_file_content(filepath, encrypted_secret)

    # Perform Decrypt
    aes256_cipher = AES256Cipher()
    decrypted_secret = aes256_cipher.decrypt(key=key, encrypted_secret=ugly_encrypted_secret)

    # Write back unencrypted content to the file
    try:
        decrypted_secret_as_string = decrypted_secret.decode('utf-8')
    except UnicodeDecodeError:
        # This happens when the encrypted secret (not the fingerprint part)
        # is edited, basically we decrypt into garbledygook and so the string
        # reader freaks out.
        return 'The output was not what I expected...'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(decrypted_secret_as_string)

    return '{} - is now decrypted.'.format(filepath)
