"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
import errno
from io import open


def read_jakfile_to_dict(jakfile='jakfile'):
    """Read the jakfile and dump its json comments into a dict for easy usage"""
    with open(jakfile, 'rt') as f:
        import json
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


def create_jakfile(jakfile='jakfile'):
    """"""
    from . import password_services as ps
    from . import outputs
    key = ps.generate_256bit_key().decode('utf-8')
    fresh_jakfile = outputs.FRESH_JAKFILE.format(key=key)
    try:
        with open(jakfile, 'r'):
            return "You already seem to have a jakfile."
    except IOError:
        with open(jakfile, 'w') as f:
            f.write(fresh_jakfile)
        return "I created a fresh new jakfile for you. You should check it out!"


def grouper(iterable, n):
    """split iterable data into n-length blocks
    grouper('aaa', 2) == ('aa', 'a')
    """
    return tuple(iterable[i:i + n] for i in range(0, len(iterable), n))


def backup_file_content(filepath, content):
    """backs up a string in the .jak folder.

    TODO Needs test
    """
    filename = '.jak/' + filepath[filepath.rfind('/') + 1:] + '_backup'
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))

        # Guard against race condition
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'w') as f:
        f.write(content)

    return True


def is_there_a_backup(filepath):
    """Check if a backup for a file exists

    TODO Needs test
    """
    filename = '.jak/' + filepath[filepath.rfind('/') + 1:] + '_backup'
    return os.path.exists(filename)


def get_backup_content_for_file(filepath):
    """Get the value of a previously encrypted file.
    The original use case is to restore encrypted state instead of randomizing
    a new one (due to IV random generation). This makes jak way more friendly
    to VCS systems such as git.

    TODO Needs test
    """
    filename = '.jak/' + filepath[filepath.rfind('/') + 1:] + '_backup'
    with open(filename, 'rt') as f:
        encrypted_secret = f.read()
    return encrypted_secret
