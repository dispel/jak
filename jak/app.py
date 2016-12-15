# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import click
from . import crypto_services as cs
from . import password_services as ps
from . import __version_full__
from .exceptions import JakException
from . import helpers
from . import start as start_logic
from . import outputs
from .diff import diff as perform_diff


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class JakGroup(click.Group):
    def list_commands(self, ctx):
        """Override so we get them in the order we want in the help"""

        # These are the ones we care about having first for usability reasons
        show_at_top = ['start', 'keygen', 'encrypt', 'decrypt', 'stomp', 'shave']

        # Append extra commands that are not in the priority list to the end.
        all_commands = sorted(self.commands)
        extras = set(all_commands) - set(show_at_top)
        return show_at_top + sorted(list(extras))


@click.group(invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS,
             no_args_is_help=True,
             cls=JakGroup)
@click.option('-v', '--version', is_flag=True)
def main(version):
    """(c) Dispel LLC (GPLv3)

    Jak is a CLI tool for securely encrypting files.

    To get started I recommend typing "jak start" to create a jakfile (settings).

    Jaks intended use is for files in git repos that developers do
    not want to enter their permanent git history. But nothing prevents
    jak from being used with arbitrary files on a case by case basis.

    For full documentation see https://github.com/dispel/jak
    """
    if version:
        click.echo(__version_full__)


@main.command(help='Create a jakfile with some helpful examples.')
def start():
    """Create a jakfile with some helpful examples."""
    result = start_logic.create_jakfile()
    if start_logic.is_git_repository() and start_logic.want_to_add_pre_commit_encrypt_hook():
        result += start_logic.add_pre_commit_encrypt_hook()
    click.echo(result)


@main.command(help='Generates a valid secure secret key.')
@click.option('-m', '--minimal', is_flag=True)
def keygen(minimal):
    """Generate a strong key for use with jak."""
    key = ps.generate_256bit_key().decode('utf-8')
    if minimal:
        output = key
    else:
        output = outputs.KEYGEN_RESPONSE.format(key=key)
    click.echo(output)


def encrypt_inner(filepath, key=None, key_file=None):
    """Logic for encrypting file(s)"""
    try:
        jakfile_dict = helpers.read_jakfile_to_dict()
    except IOError:
        jakfile_dict = None

    try:
        if filepath == 'all':
            click.echo(cs.all(callable_action=cs.encrypt_file,
                              key=key,
                              key_file=key_file,
                              jakfile_dict=jakfile_dict))
        else:
            click.echo(cs.encrypt_file(filepath=filepath,
                                       key=key,
                                       key_file=key_file,
                                       jakfile_dict=jakfile_dict))
    except JakException as je:
        click.echo(je)


@main.command(help='jak encrypt <file>')
@click.argument('filepath')
@click.option('-k', '--key', default=None)
@click.option('-kf', '--key-file', default=None)
def encrypt(filepath, key, key_file):
    """Encrypts file(s)"""
    encrypt_inner(filepath, key, key_file)


def decrypt_inner(filepath, key=None, key_file=None):
    """Logic for decrypting file(s)"""
    try:
        jakfile_dict = helpers.read_jakfile_to_dict()
    except IOError:
        jakfile_dict = None

    try:
        if filepath == 'all':
            click.echo(cs.all(callable_action=cs.decrypt_file,
                              key=key,
                              key_file=key_file,
                              jakfile_dict=jakfile_dict))
        else:
            click.echo(cs.decrypt_file(filepath=filepath,
                                       key=key,
                                       key_file=key_file,
                                       jakfile_dict=jakfile_dict))
    except JakException as je:
        click.echo(je)


@main.command(help='jak decrypt <file>')
@click.argument('filepath')
@click.option('-k', '--key', default=None)
@click.option('-kf', '--key-file', default=None)
def decrypt(filepath, key, key_file):
    """Decrypt file(s)"""
    decrypt_inner(filepath, key, key_file)


@main.command()
def stomp():
    """alias for 'jak encrypt all'"""
    encrypt_inner(filepath='all')


@main.command()
def shave():
    """alias for 'jak decrypt all'"""
    decrypt_inner(filepath='all')


@main.command()
@click.argument('filepath')
@click.option('-k', '--key', default=None)
@click.option('-kf', '--key-file', default=None)
def diff(filepath, key, key_file):
    """If there is a merge conflict decrypt for easier diffing.
    The file needs to be in a git merge conflict format such as:

    <<<<<< HEAD
    <LOCAL>
    ======
    <REMOTE>
    >>>>>>>>> <somehash>
    """
    perform_diff(filepath=filepath, key=key, key_file=key_file)


#
# TODO FUTURE(?)
#

# @main.command()
# def protect():
#     """Add file to jakfiles "files_to_encrypt" list if it is not already in there"""
#     click.echo("TODO")
#
#
# @main.command()
# def abandon():
#     """Remove file from jakfile's "files_to_encrypt" list if it is in there"""
#     click.echo("TODO")
#
#
# @main.command()
# def unprotect():
#     """alias for abandon"""
#     click.echo("TODO")
