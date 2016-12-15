# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

from . import outputs
from io import open
import click
import os


def create_jakfile(jakfile='jakfile'):
    """"""
    from . import password_services as ps
    key = ps.generate_256bit_key().decode('utf-8')
    fresh_jakfile = outputs.FRESH_JAKFILE.format(key=key)
    try:
        with open(jakfile, 'r'):
            return "You already seem to have a jakfile."
    except IOError:
        with open(jakfile, 'w') as f:
            f.write(fresh_jakfile)
        return "I created a fresh new jakfile for you. You should check it out!"


def is_git_repository():
    return os.path.exists('.git')


def want_to_add_pre_commit_encrypt_hook():
    """"""
    # put msg in output.py?
    msg = '''Do you want to add a git pre-commit hook?
The hook will attempt to encrypt all files in your jakfile's "files_to_encrypt" list.
Trust but verify: always eyeball encrypted files before pushing. [y/n]'''
    response = click.prompt(msg, default='Y')
    response = response.lower()
    return response == 'y' or response == 'yes'


def add_pre_commit_encrypt_hook():
    """"""
    with open('.git/hooks/jak.pre-commit.py', 'w') as f:
        f.write(outputs.PRE_COMMIT_ENCRYPT)
    # os.chmod('.git/hooks/jak.pre-commit.py', '0755')

    if not os.path.exists('.git/hooks/pre-commit'):
        with open('.git/hooks/pre-commit', 'w') as f:
            f.write(outputs.PRE_COMMIT_CALL)
        os.chmod('.git/hooks/pre-commit', 0o755)
        return '''
Successfully added a fresh .git/hooks/pre-commit hook with Jak enabled.
'''
    else:
        return '''
You already enabled git's pre-commit hook. I don't want to step on your toes.
Please add the following block into your .git/hooks/pre-commit script above the exit 0 call:

#----Begin jak Block ----

PURPLE='\\033[1;35m'
NC='\\033[0m' # No Color

printf "🌰  ${PURPLE}jak: pre-commit > Encrypting files listed in jakfile.${NC}\\n"

# See http://click.pocoo.org/6/python3/ for more info
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Encrypt any staged files that are protected by jak
python .git/hooks/jak.pre-commit.py

#----End jak Block ----
'''

    # Does .git/hooks/pre-commit exist?
    # IF it doesnt
    #   Create the file
    # add our lines to the end
    #
    pass
