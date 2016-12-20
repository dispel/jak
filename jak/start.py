# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
import click
import subprocess
from io import open
from . import outputs
from . import helpers


def create_jakfile(filepath):
    """Checks whether you have a jakfile or need a new one."""
    if os.path.exists(filepath + 'jakfile'):
        msg = helpers.two_column('Is there already a jakfile?', 'Yep!')
        msg += '\n' + helpers.two_column('  Doing nothing, but feeling good about life', 'Done')
    else:
        from . import password_services as ps
        key = ps.generate_256bit_key().decode('utf-8')
        keyfile_path = '.jak/keyfile'
        fresh_jakfile = outputs.FRESH_JAKFILE.format(keyfile_path=keyfile_path)
        helpers.create_or_overwrite_file(filepath=filepath + 'jakfile', content=fresh_jakfile)
        helpers.create_or_overwrite_file(filepath=filepath + keyfile_path, content=key)
        msg = helpers.two_column('Is there already a jakfile?', 'Nope!')
        msg += '\n' + helpers.two_column('  Creating ./jakfile', 'Done')
        msg += '\n' + helpers.two_column('  Creating ./.jak/keyfile', 'Done')
    return msg + '\n'


def find_git_repository_parent():
    """Just checking path exists is not enough, they might run a different
directory other than the repo root. This recursively checks up the path to
see if a parent directory is a git repo. This function should return the path
[relative to cwd] of the repo root. It returns the path prefix needed to put
all other files in the right spot."""
    if not os.path.exists('.git'):
        is_git_repository = False
        iterator = 0
        while (iterator <= len(os.getcwd().split('/'))):
            # TODO - go from the top down rather than bottom up - give full path info.
            prefix = '../'
            if os.path.exists(iterator*prefix + '.git'):
                click.echo("git repo, not in repo root folder")
                return iterator*prefix
            iterator += 1
        return ''
    else:
        return './'


def has_gitignore(filepath='.gitignore'):
    """Note here add a file path in case they are not in the repo root"""
    return os.path.exists(filepath)


def add_keyfile_to_gitignore(filepath='.gitignore'):
    """This function should open the gitignore file and add the .jak
folder [which contains the keyfile]. Note here add a file path in case
they are not in the repo root"""

    with open(filepath, 'r+') as f:
        gitignore = f.read()
        appended_text = '# Jak KeyFile\n .jak \n'
        try:
            appended_text = appended_text.decode('utf-8')
        except AttributeError:
            pass
        f.write(appended_text)
    return


def want_to_add_pre_commit_encrypt_hook():
    """"""
    msg = outputs.QUESTION_WANT_TO_ADD_PRE_COMMIT
    response = click.prompt(msg, default='Y')
    response = response.lower()
    return response == 'y' or response == 'yes'


def add_pre_commit_encrypt_hook(repo_root_filepath='./'):
    """"""
    jak_pre_commit_path = repo_root_filepath + '.git/hooks/jak.pre-commit.py'
    git_pre_commit_path = repo_root_filepath + '.git/hooks/pre-commit'

    helpers.create_or_overwrite_file(filepath=jak_pre_commit_path, content=outputs.PRE_COMMIT_ENCRYPT)

    if not os.path.exists(git_pre_commit_path):
        helpers.create_or_overwrite_file(filepath=git_pre_commit_path, content=outputs.PRE_COMMIT_CALL)
        os.chmod(git_pre_commit_path, 0o755)
        msg = helpers.two_column('Is there a pre-commit hook?', 'Nope!')
        msg += '\n' + helpers.two_column('  Creating pre-commit hook call (.git/hooks/pre-commit)', 'Done')
        msg += '\n' + helpers.two_column('  Creating encryption logic (.git/hooks/jak.pre-commit.py)', 'Done')
    else:
        msg = helpers.two_column('Is there a pre-commit hook?', 'Yep!')
        msg += '\n' + helpers.two_column('  Creating encryption logic (.git/hooks/jak.pre-commit.py)', 'Done')
        msg += outputs.PRE_COMMIT_EXISTS
    return msg + '\n'
