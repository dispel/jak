# -*- coding: utf-8 -*-
"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

FRESH_JAKFILE = u'''// For more information visit https://github.com/dispel/jak/
// Protip: Set your syntax highlighting to JavaScript.
{{
  // RECOMMENDED
  // List files to encrypt here so you can quickly encrypt/decrypt them all
  // using the "$> jak encrypt/decrypt all" commands.
  "files_to_encrypt": ["path/to/file"],

  // You can store your key in a file INSTEAD of having a "key" value.
  // This allows you to commit the jakfile. (never commit your key!)
  "keyfile": "{keyfile_path}"
}}'''

KEYGEN_RESPONSE = '''Here is your shiny new key.

{key}

Remember to keep this password secret and save it. Without it you will NOT be able
to decrypt any file(s) you encrypt using it.'''

PRE_COMMIT_CALL = '''#!/bin/sh
# ---- Begin jak Block ----

PURPLE='\\033[1;35m'
NC='\\033[0m' # No Color

printf "🌰  ${PURPLE}jak: pre-commit > Encrypting files listed in jakfile.${NC}\\n"

# See http://click.pocoo.org/6/python3/ for more info
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8


# Encrypt any staged files that are protected by jak
python .git/hooks/jak.pre-commit.py

# ---- End jak Block ----

# Place your custom pre-commit code here
'''

PRE_COMMIT_EXISTS = '''

jak says: EXISTING PRE-COMMIT HOOK, I DON'T WANT TO OVERRIDE IT WILLY NILLY
SEE .git/hooks/jak.pre-commit.py for further installation instructions.'''

PRE_COMMIT_ENCRYPT = '''#!/usr/bin/env python

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.

INSTALLATION
To enable the pre-commit hook,
Please add the following block into your .git/hooks/pre-commit script manually:

#----Begin jak Block ----

PURPLE='\033[1;35m'
NC='\033[0m' # No Color

printf "🌰  ${PURPLE}jak: pre-commit > Encrypting files listed in jakfile.${NC}\n"

# See http://click.pocoo.org/6/python3/ for more info
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Encrypt any staged files that are protected by jak
python .git/hooks/jak.pre-commit.py

#----End jak Block ----
"""

from __future__ import unicode_literals

import subprocess
from io import open
import os


def _remove_comments_from_JSON(raw_json):
    """Technically JSON does not have comments. But it is very user friendly to
    allow for commenting so we strip the comments out in this function.
    Example input:
    // Comment 0
    {
        // Comment 1
        "Ada": "Lovelace"  // Comment 2
        // Comment 3
    } // Comment 4
    Expected output:
    {
        "Ada": "Lovelace"
    }
    """
    import re
    tmp = re.sub(r'//.*\\n', '\\n', raw_json)
    tmp = "".join(tmp.replace('\\n', '').split())
    return tmp


def read_jakfile_to_dict():
    """Read the jakfile and dump it's json comments into a dict"""
    with open('jakfile', 'rt') as f:
        import json
        contents_raw = f.read()

    sans_comments = _remove_comments_from_JSON(contents_raw)
    return json.loads(sans_comments)


def get_staged():
    output = subprocess.check_output('git --no-pager diff --cached --name-only',
                                   shell=True)
    output_array = output.decode('utf-8').split('\\n')
    names = [name for name in output_array if name]
    return names


def try_encrypt(filename):
    proc = subprocess.Popen(["jak", "encrypt", filename], env=dict(os.environ))
    proc.communicate()


def git_add(filename):
    proc = subprocess.Popen(['git', 'add', filename])
    proc.communicate()


if __name__ == '__main__':
    staged_files = get_staged()
    files_to_encrypt = read_jakfile_to_dict()['files_to_encrypt']
    for staged_file in staged_files:
        if staged_file in files_to_encrypt:
            try_encrypt(staged_file)
            git_add(staged_file)
'''


FINAL_START_MESSAGE = '''- - - Setup complete! - - -

TL;DR;
1. If this is your first rodeo please look at your ./keyfile and your ./jakfile.
2. Keep your keyfile secret at all costs. Don't commit it to any VCS, don't email it, don't put it in dropbox, definitely don't put it in google drive, etc...!

{version}'''

QUESTION_WANT_TO_ADD_PRE_COMMIT = '''
Do you want to add a git pre-commit hook?
The hook will encrypt files listed in your jakfile
each time you git commit. [y/n]'''
