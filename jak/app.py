# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
import click
from . import helpers
from . import outputs
from . import __version_full__
from . import diff as diff_logic
from . import decorators
from . import start as start_logic
from . import crypto_services as cs
from .exceptions import JakException


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class JakGroup(click.Group):
    def list_commands(self, ctx):
        """Override so we get commands in help file them in the order we want in the help"""

        # These are the ones we care about having first for usability reasons
        show_at_top = ['start', 'keygen', 'encrypt', 'decrypt', 'stomp', 'shave', 'diff']

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
    """(c) Dispel LLC (Apache-2.0)

    Jak is a CLI tool for securely encrypting files.

    To get started I recommend typing "jak start" (preferably while your
    working directory is a git repository).

    Jaks intended use is for secret files in git repos that developers do
    not want to enter their permanent git history. But nothing prevents
    jak from being used outside of git.

    \b
    For more information about a certain command use:
      $> jak COMMAND --help

    For full documentation see https://github.com/dispel/jak"""
    if version:
        click.echo(__version_full__)


@main.command()
def start():
    """Initializes jak in your working directory."""
    click.echo('''- - - Welcome to jak - - -

"jak start" does a couple of things:
1. jakfile: File with per working directory settings for jak.
2. keyfile: Holds the key used to encrypt files.
    ''')
    jwd = helpers.get_jak_working_directory()
    click.echo(start_logic.create_jakfile(jwd=jwd))

    if not os.path.exists('{}/.git'.format(jwd)):
        msg = helpers.two_column('Is this a git repository?', 'Nope!')
        msg += '\n  jak says: I work great with git, but you do you.'
        click.echo(msg)
    else:
        click.echo(helpers.two_column('Is this a git repository?', 'Yep!'))
        if helpers.does_jwd_have_gitignore(cwd=jwd):
            click.echo(helpers.two_column('  Is there a .gitignore?', 'Yep!'))
            start_logic.add_keyfile_to_gitignore(filepath=jwd + '/.gitignore')
            click.echo(helpers.two_column('  Adding ".jak" to .gitignore', 'Done'))
        else:
            click.echo(helpers.two_column('  Is there a .gitignore?', 'Nope!'))
            helpers.create_or_overwrite_file(filepath=jwd + '/.gitignore',
                                             content='# Jak KeyFile\n .jak \n')
            click.echo(helpers.two_column('  Creating ./.gitignore', 'Done'))
            click.echo(helpers.two_column('  Adding ".jak" to .gitignore', 'Done'))

        if start_logic.want_to_add_pre_commit_encrypt_hook():
            click.echo('\n' + start_logic.add_pre_commit_encrypt_hook(jwd))

    click.echo(outputs.FINAL_START_MESSAGE.format(version=__version_full__))


@main.command()
@click.option('-m', '--minimal', is_flag=True)
def keygen(minimal):
    """Generate a strong key for use with jak.

    You can keep the key wherever, but I would recommend putting it
    in a .gitignored keyfile that your jakfile points to.

    Do not add this key to your git repository. Nor should you ever give it
    to anyone who should not have access. Remember, if you give someone a key
    they can look at your git history and encrypt files encrypted with that key
    that happened in the past. If your current or past keys get out, I would
    recommend cycling your secrets and your keys.

    In fact I would recommend cycling your keys every so often (3-6 months)
    anyway, just as a standard best practice. But in reality very few developers
    actually do this. =(
    """
    key = helpers.generate_256bit_key().decode('utf-8')
    if minimal:
        output = key
    else:
        output = outputs.KEYGEN_RESPONSE.format(key=key)
    click.echo(output)


@decorators.attach_jwd
@decorators.read_jakfile
@decorators.select_key
@decorators.select_files
def encrypt_inner(files, key, **kwargs):
    """Flow for encrypting file(s)"""
    for filepath in files:
        try:
            result = cs.encrypt_file(filepath=filepath, key=key, **kwargs)
        except JakException as je:
            click.echo(je)
        else:
            click.echo(result)


@main.command(help='jak encrypt <file>')
@click.argument('filepath')
@click.option('-k', '--key', default=None, metavar='<string>')
@click.option('-kf', '--keyfile', default=None, metavar='<file_path>')
def encrypt(filepath, key, keyfile):
    """Encrypt file(s)"""
    try:
        encrypt_inner(all_or_filepath=filepath, key=key, keyfile=keyfile)
    except JakException as je:
        click.echo(je)


@decorators.attach_jwd
@decorators.read_jakfile
@decorators.select_key
@decorators.select_files
def decrypt_inner(files, key, **kwargs):
    """Flow for decrypting file(s)"""
    for filepath in files:
        try:
            result = cs.decrypt_file(filepath=filepath, key=key, **kwargs)
        except JakException as je:
            click.echo(je)
        else:
            click.echo(result)


@main.command(help='jak decrypt <file>')
@click.argument('filepath')
@click.option('-k', '--key', default=None, metavar='<string>')
@click.option('-kf', '--keyfile', default=None, metavar='<file_path>')
def decrypt(filepath, key, keyfile):
    """Decrypt file(s)"""
    try:
        decrypt_inner(all_or_filepath=filepath, key=key, keyfile=keyfile)
    except JakException as je:
        click.echo(je)


@main.command()
@click.option('-k', '--key', default=None, metavar='<string>')
@click.option('-kf', '--keyfile', default=None, metavar='<file_path>')
def stomp(key, keyfile):
    """Alias for 'jak encrypt all'"""
    try:
        encrypt_inner(all_or_filepath='all', key=key, keyfile=keyfile)
    except JakException as je:
        click.echo(je)


@main.command()
@click.option('-k', '--key', default=None, metavar='<string>')
@click.option('-kf', '--keyfile', default=None, metavar='<file_path>')
def shave(key, keyfile):
    """Alias for 'jak decrypt all'"""
    try:
        decrypt_inner(all_or_filepath='all', key=key, keyfile=keyfile)
    except JakException as je:
        click.echo(je)


@main.command(options_metavar='<options>')
@click.argument('conflicted_file', metavar='<conflicted_file>')
@click.option('-k', '--key', default=None, metavar='<string>')
@click.option('-kf', '--keyfile', default=None, metavar='<file_path>')
def diff(conflicted_file, key, keyfile):
    """Decrypt conflicted file for an easier merge.

    \b
    Supported merge tools:
    plain: Just decrypted and you can sort it out in a text editor. (default)
    opendiff: macOS built in FileMerge GUI tool.
    vimdiff: I decrypt and give you the vimdiff command to run to finish the merge.
    """
    try:
        result = diff_logic.diff(filepath=conflicted_file, key=key, keyfile=keyfile)
    except JakException as je:
        result = je
    click.echo(result)
