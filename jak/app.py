# -*- coding: utf-8 -*-
"""
jak.app
---

Jak is a easy to use CLI tool for securely encrypting files.

TODOS
 - We have way too many functions named decrypt/encrypt now, it is straight up confusing.
"""

import click
from . import crypto_services as cs
from . import password_services as ps
from . import __version_full__
from .exceptions import JakException
from . import helpers


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True)
def main(version):
    """(c) Dispel LLC (GPLv3)

    Jak is a easy to use CLI tool for securely encrypting files.

    All passwords must be exactly 32 characters so that jak can generate
    a strong enough encryption (AES256).

    Jaks intended use is for files in git repos that developers do
    not want to enter their permanent git history. But nothing prevents
    jak from being used with arbitrary files on a case by case basis.
    """
    if version:
        click.echo(__version_full__)
    # TODO if possible show help text if they just type "$> jak"


def encrypt_inner(filepath, password=None, password_file=None):
    """shim with logic for encrypting file(s)"""
    try:
        jakfile_dict = helpers.read_jakfile_to_dict()
    except IOError:
        jakfile_dict = None

    try:
        if filepath == 'all':
            click.echo(cs.all(callable_action=cs.encrypt_file,
                              password=password,
                              password_file=password_file,
                              jakfile_dict=jakfile_dict))
        else:
            click.echo(cs.encrypt_file(filepath=filepath,
                                       password=password,
                                       password_file=password_file,
                                       jakfile_dict=jakfile_dict))
    except JakException as je:
        click.echo(je)


@main.command(help='jak encrypt <file> (-p OR -pf) <pass>')
@click.argument('filepath')
@click.option('-p', '--password', default=None)
@click.option('-pf', '--password-file', default=None)
def encrypt(filepath, password, password_file):
    """Encrypts file(s)"""
    encrypt_inner(filepath, password, password_file)


def decrypt_inner(filepath, password=None, password_file=None):
    """Shim with logic for decrypting file(s)"""
    try:
        jakfile_dict = helpers.read_jakfile_to_dict()
    except IOError:
        jakfile_dict = None

    try:
        if filepath == 'all':
            click.echo(cs.all(callable_action=cs.decrypt_file,
                              password=password,
                              password_file=password_file,
                              jakfile_dict=jakfile_dict))
        else:
            click.echo(cs.decrypt_file(filepath=filepath,
                                       password=password,
                                       password_file=password_file,
                                       jakfile_dict=jakfile_dict))
    except JakException as je:
        click.echo(je)


@main.command(help='jak decrypt <file> (-p OR -pf) <pass>')
@click.argument('filepath')
@click.option('-p', '--password', default=None)
@click.option('-pf', '--password-file', default=None)
def decrypt(filepath, password, password_file):
    """Decrypt file(s)"""
    decrypt_inner(filepath, password, password_file)


@main.command(help='Generates a valid secure password.')
def genpass():
    """Generate a password for use with jak."""
    password = ps.generate_256bit_key().decode('utf-8')
    output = '''Here is your shiny new password. It is 32 characters (bytes) and will work just fine with AES256.


{password}

Remember to keep this password secret and save it. Without it you will NOT be able
to decrypt any file(s) you encrypt using it.
    '''.format(password=password)
    click.echo(output)


@main.command(help='Create a jakfile with some helpful examples.')
def init():
    """Create a jakfile with some helpful examples."""
    from . import helpers
    result = helpers.create_jakfile()
    click.echo(result)


@main.command()
def stomp():
    """alias for 'jak encrypt all'"""
    encrypt_inner(filepath='all')


@main.command()
def shave():
    """alias for 'jak decrypt all'"""
    decrypt_inner(filepath='all')


#
# TODO FUTURE
#

# @main.command()
# def protect():
#     """Add file to jakfiles "protected_files" list if it is not already in there"""
#     click.echo("TODO")
#
#
# @main.command()
# def abandon():
#     """Remove file from jakfile's "protected_files" list if it is in there"""
#     click.echo("TODO")
#
#
#
#
# @main.command()
# def unprotect():
#     """alias for abandon"""
#     click.echo("TODO")
