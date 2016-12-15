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


def grouper(iterable, n):
    """split iterable data into n-length blocks
    grouper('aaa', 2) == ('aa', 'a')
    """
    return tuple(iterable[i:i + n] for i in range(0, len(iterable), n))


def backup_file_content(filepath, content):
    """backs up a string in the .jak folder.

    TODO Needs test
    """
    filepath = '.jak/' + filepath[filepath.rfind('/') + 1:] + '_backup'
    return create_or_overwrite_file(filepath=filepath, content=content)


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


def get_filepath_end_extension(full_filepath):
    """
    /hello/there.ext > (/hello/there, .ext)
    there > (there, '')
    /hello/there > (/hello/there, '')
    """
    final_dot = full_filepath.rfind('.')
    if final_dot != -1:
        filepath = full_filepath[:full_filepath.rfind('.')]
        ext = full_filepath[full_filepath.rfind('.'):]
    else:
        filepath = full_filepath
        ext = ''
    return filepath, ext
