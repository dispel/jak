# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

from . import outputs
from io import open
import click
import os
from . import helpers


def create_jakfile(jakfile='jakfile'):
    """Checks whether you have a jakfile or need a new one."""
    if os.path.exists(jakfile):
        msg = helpers.two_column('Is there already a jakfile?', 'Yep!')
        msg += '\n' + helpers.two_column('  Doing nothing, but feeling good about life', 'Done')
    else:
        from . import password_services as ps
        key = ps.generate_256bit_key().decode('utf-8')
        fresh_jakfile = outputs.FRESH_JAKFILE.format(key=key)
        helpers.create_or_overwrite_file(filepath=jakfile, content=fresh_jakfile)
        msg = helpers.two_column('Is there already a jakfile?', 'Nope!')
        msg += '\n' + helpers.two_column('  Creating ./jakfile', 'Done')
        msg += '\n' + helpers.two_column('  TODO Creating ./keyfile', 'Done')
    return msg + '\n'


def is_git_repository():
    return os.path.exists('.git')


def want_to_add_pre_commit_encrypt_hook():
    """"""
    msg = outputs.QUESTION_WANT_TO_ADD_PRE_COMMIT
    response = click.prompt(msg, default='Y')
    response = response.lower()
    return response == 'y' or response == 'yes'


def add_pre_commit_encrypt_hook():
    """"""
    with open('.git/hooks/jak.pre-commit.py', 'w') as f:
        f.write(outputs.PRE_COMMIT_ENCRYPT)

    if not os.path.exists('.git/hooks/pre-commit'):
        with open('.git/hooks/pre-commit', 'w') as f:
            f.write(outputs.PRE_COMMIT_CALL)
        os.chmod('.git/hooks/pre-commit', 0o755)
        msg = helpers.two_column('Is there a pre-commit hook?', 'Nope!')
        msg += '\n' + helpers.two_column('  Creating pre-commit hook call (.git/hooks/pre-commit)', 'Done')
        msg += '\n' + helpers.two_column('  Creating encryption logic (.git/hooks/jak.pre-commit.py)', 'Done')
    else:
        msg = helpers.two_column('Is there a pre-commit hook?', 'Yep!')
        msg += '\n' + helpers.two_column('  Creating encryption logic (.git/hooks/jak.pre-commit.py)', 'Done')
        msg += outputs.PRE_COMMIT_EXISTS
    return msg + '\n'
