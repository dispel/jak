"""Jak is a CLI tool for encrypting files."""

import click
from .crypto_services import encrypt_file, decrypt_file
from .version import __version_full__


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True)
def main(version):
    """jak is a tool for encrypting files and keeping track of them.
    Its intended use is for files in git repos that developers do
    not want to enter their permanent git history. However, it can
    be used for encrypting any files you like."""
    if version:
        click.echo(__version_full__)

    # TODO if possible show help text if they just type "$> jak"


@main.command(help='Encrypts a file')
@click.argument('filename')
@click.option('-p', '--password', required=True, default=None)
def encrypt(filename, password):
    """Encrypts a file"""
    try:
        encrypt_file(key=password, filename=filename)
    except FileNotFoundError:
        click.echo('Sorry I can\'t find the file: {}'.format(filename))
    else:
        click.echo('{} - is now encrypted.'.format(filename))


@main.command(help='Decrypts a file')
@click.argument('filename')
@click.option('-p', '--password', required=True, default=None)
def decrypt(password, filename):
    """Decrypts a file"""
    try:
        decrypt_file(key=password, filename=filename)
    except FileNotFoundError:
        click.echo('Sorry I can\'t find the file: {}'.format(filename))
    else:
        click.echo('{} - is now decrypted.'.format(filename))


#
# TODO FUTURE
#

# @main.command()
# def protect():
#     """"""
#     click.echo("TODO")
#
#
# @main.command()
# def abandon():
#     """"""
#     click.echo("TODO")


# @main.command()
# def encrypt_all():
#     """Encrypt all protected files"""
#     click.echo("TODO")
#
#
# @main.command()
# def decrypt_all():
#     """Decrypt all protected files"""
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
