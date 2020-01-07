"""
Copyright 2018 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
import json
import errno
import binascii
from io import open


def grouper(iterable, n):
    """split iterable data into n-length blocks
    grouper('aaa', 2) == ('aa', 'a')
    """
    return tuple(iterable[i:i + n] for i in range(0, len(iterable), n))


def create_or_overwrite_file(filepath, content):
    """"""
    # If not a path and just a file default to a local folder.
    dirname = os.path.dirname(filepath) or '.'

    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)

        # Guard against race condition
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    try:
        content = content.decode('utf-8')
    except AttributeError:
        pass

    with open(filepath, 'w') as f:
        f.write(content)


def create_backup_filepath(jwd, filepath):
    """Example:
    Input: jwd='/a/b/c', filepath: '/a/b/c/d/e.txt'
    Output: /a/b/c/.jak/d_e.txt_backup

    Input: jwd='/', filepath: '/a'
    Output: /.jak/a_backup

    Input: jwd='/a/b', filepath: '/a/b/c'
    Output: /a/b/.jak/c_backup

    FIXME: There is probably a way cleaner way to write this function.
    """

    # To make this easier to understand:
    # filepath === /a/b/c/d
    # jwd = /a
    filename = filepath.replace(jwd, '')  # /b/c/d

    # Special case: root.
    if ('/' not in filename):
        return '/.jak/{}_backup'.format(filename)

    filename = filename[1:]  # b/c/d
    filename = filename.replace('/', '_')  # b_c_d
    return '{}/.jak/{}_backup'.format(jwd, filename)  # /a/.jak/b_c_d_backup


def backup_file_content(jwd, filepath, content):
    """backs up a string in the .jak folder."""
    backup_filepath = create_backup_filepath(jwd=jwd, filepath=filepath)
    return create_or_overwrite_file(filepath=backup_filepath, content=content)


def is_there_a_backup(jwd, filepath):
    """Check if a backup for a file exists"""
    filename = create_backup_filepath(jwd=jwd, filepath=filepath)
    return os.path.exists(filename)


def get_backup_content_for_file(jwd, filepath):
    """Get the value of a previously encrypted file.
    The original use case is to restore encrypted state instead of randomizing
    a new one (due to IV random generation). This makes jak way more friendly
    to VCS systems such as git.

    TODO Needs test
    """
    filename = create_backup_filepath(jwd=jwd, filepath=filepath)
    with open(filename, 'rt') as f:
        encrypted_secret = f.read()
    return encrypted_secret


def two_column(left, right, col1_length=65, col2_length=1):
    """Two column layout for printouts.
    Example:
    I did this thing             done!
    """
    tmp = '%-{}s%-{}s'.format(col1_length, col2_length)

    # The space in front of the right column add minimal padding in case
    # lefts content is very long (>col1_length)
    return tmp % (left, ' ' + right)


def generate_256bit_key():
    """Generate a pseudo-random secure ready-for-crypto-use key.

    Generate it straight using urandom. Proving randomness is impossible, and a good source
    is a hotly debated subject. As always, opinions are welcome but please inform
    yourself first and be prepared to cite a source.

    Further Reading:
    https://docs.python.org/3.5/library/os.html#os.urandom
    https://docs.python.org/2.7/library/os.html#os.urandom
    https://sockpuppet.org/blog/2014/02/25/safely-generate-random-numbers/
    http://www.2uo.de/myths-about-urandom/
    https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/Random/__init__.py
    """
    return binascii.hexlify(os.urandom(32))


def get_jak_working_directory(cwd=os.getcwd()):
    """Finds a git repository parent and returns the path to it.
    if none is found default to current directory: './'"""

    # They are probably in a .git repo so let's check that right off the bat.
    if os.path.exists('{}/.git'.format(cwd)):
        return cwd

    cwd_path = cwd.split('/')

    # Remove final one since we already checked current directory above.
    del cwd_path[-1]

    # Traverse up looking for a folder with a .git folder in it.
    # For example if C has a .git in it
    # /A/B/C/D/E/.git --> False
    # /A/B/C/D/.git --> False
    # /A/B/C/.git --> True, returns '/A/B/C'
    for directory in reversed(cwd_path):
        dirpath = '/'.join(cwd_path)
        if os.path.exists('{}/.git'.format(dirpath)):
            return dirpath
        cwd_path.remove(directory)

    # No parent git repo, let's just use the current directory
    return cwd


def does_jwd_have_gitignore(cwd=os.getcwd()):
    """'' means they are in repo root."""
    jwd = get_jak_working_directory(cwd=cwd)
    return os.path.exists('{}/.gitignore'.format(jwd))


def read_jakfile_to_dict(jwd=get_jak_working_directory()):
    """Read the jakfile and dump its json comments into a dict for easy usage"""
    with open('{}/jakfile'.format(jwd), 'rt') as f:
        contents_raw = f.read()

    sans_comments = _remove_comments_from_JSON(contents_raw)
    return json.loads(sans_comments)


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
    tmp = re.sub(r'//.*\n', '\n', raw_json)
    tmp = "".join(tmp.replace('\n', '').split())
    return tmp
