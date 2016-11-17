"""Jak is a CLI tool for encrypting files."""

import click
import base64
from .crypto_services import encrypt as c_encrypt, decrypt as c_decrypt
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


# TODO
# Takes a filename
# after reading file i would reocmmend calling an internal _encrypt
# function that we can then more easily test...
# TODO http://click.pocoo.org/6/options/#values-from-environment-variables
@main.command(help='Encrypts a file')
@click.argument('filename')
@click.option('-p', '--password', required=True, default=None)
def encrypt(filename, password):
    """Encrypts a file"""

    # Debugging
    # click.echo(filename)
    # click.echo(password)

    # TODO open a file
    encrypted_secret = c_encrypt(key=password, secret=filename)

    # TODO Push that back into the file
    click.echo(base64.urlsafe_b64encode(encrypted_secret))


@main.command(help='Decrypts a file')
@click.argument('filename')
@click.option('-p', '--password', required=True, default=None)
def decrypt(password, filename):
    """Decrypts a file"""

    # Only need str because of unicode on 2.7 -.-
    # dont even know if I wanna keep the base64 encoding/decoding
    # only makes sense for readability...
    filename = base64.urlsafe_b64decode(str(filename))

    unencrypted_secret = c_decrypt(key=password, encrypted_secret=filename)
    click.echo(unencrypted_secret)


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
