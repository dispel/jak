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


@main.command(help='jak encrypt <file> (-p OR -pf) <pass>')
@click.argument('filename')
@click.option('-p', '--password', default=None)
@click.option('-pf', '--password-file', default=None)
def encrypt(filename, password, password_file):
    """Encrypts file(s)"""
    try:
        if filename == 'all':
            click.echo(
                cs.all(callable_action=cs.encrypt_file,
                       password=password,
                       password_file=password_file))
        else:
            click.echo(cs.encrypt_file(filename, password, password_file))
    except JakException as je:
        click.echo(je)


@main.command(help='jak decrypt <file> (-p OR -pf) <pass>')
@click.argument('filename')
@click.option('-p', '--password', default=None)
@click.option('-pf', '--password-file', default=None)
def decrypt(filename, password, password_file):
    """Decrypt file(s)"""
    try:
        if filename == 'all':
            click.echo(
                cs.all(callable_action=cs.decrypt_file,
                       password=password,
                       password_file=password_file))
        else:
            click.echo(cs.decrypt_file(filename, password, password_file))
    except JakException as je:
        click.echo(je)


@main.command(help='Generates a valid secure password.')
def genpass():
    """Generate a password for use with jak."""
    password = ps.generate_256bit_key().decode()
    output = '''Here is your shiny new password. It is 32 characters (bytes) and will work just fine with AES256.


{password}

Remember to keep this password secret and save it. Without it you will NOT be able
to decrypt any file(s) you encrypt using it.
    '''.format(password=password)
    click.echo(output)


#
# TODO FUTURE
#

# @main.command()
# def protect():
#     """Add file to jakfile if it is not already in there"""
#     click.echo("TODO")
#
#
# @main.command()
# def abandon():
#     """Remove file to jakfile if it is in there"""
#     click.echo("TODO")
#
#
# @main.command()
# def stomp():
#     """alias for encrypt-all"""
#     encrypt_all()
#
#
# @main.command()
# def shave():
#     """alias for decrypt-all"""
#     decrypt_all()
#
#
# @main.command()
# def unprotect():
#     """alias for abandon"""
#     click.echo("TODO")
