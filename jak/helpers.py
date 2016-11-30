"""
jak.helpers
-----------

Stuff that doesnt belong anywhere else ;p
"""


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
    password = ps.generate_256bit_key().decode('utf-8')
    fresh_jakfile = '''// For more information visit https://github.com/dispel/jak
// A jakfile is JSON except it can have comments starting with double slashes "//"
// For good syntax highlighting I would recommend treating it as a JavaScript file.
{{

  // READ ME I'M IMPORTANT
  // A jakfile should have EITHER a strong 32 character password
  // OR a link to a "password_file" OR neither. A password or password file given through
  // the CLI will override the jakfiles password/password_file values. This is to
  // avoid confusion about which password a file is encrypted with.
  //
  // To better explain the asterisk * will denote which password will be used:
  // cli pass*
  // cli passfile*
  // cli pass + cli passfile              -> NOPE
  // jakfile pass*
  // jakfile passfile*
  // jakfile pass + jakfile passfile      -> NOPE
  // cli pass* + jakfile pass             -> OVERRIDE
  // cli passfile* + jakfile pass         -> OVERRIDE
  // cli pass + jakfile passfile          -> OVERRIDE
  // cli pass + cli passfile + jakfile x  -> NOPE
  // etc...

  // Recommended usage is to simply input a password in the jakfile and then
  // spam "jak encrypt/decrypt all" for all it's worth. Keep it simple stupid.

  // An encryptions strength is only as strong as the password used to encrypt it.
  // That is why I force you to use 32 characters (an astronomical number!)
  // in your password.
  // The password SHOULD BE AS RANDOM AS POSSIBLE.
  // Please use "$> jak genpass" to make a password
  // and share it securely with your team (not e-mail! Say it with me... NOT E-MAIL!).
  "password": "{password}",
  // OR
  // "password_file": "jakpasswordfile"

  // a list of protected files that will be encrypted/decrypted with the "all" command.
  // f.e.
  // $> jak encrypt all
  // $> jak decrypt all
  "protected_files": ["examplefile1", "examplefile2.txt", "/Users/thedude/mysecrets.txt"] // EDIT ME
}}'''.format(password=password)
    try:
        with open(jakfile, 'r'):
            return "You already seem to have a jakfile."
    except IOError:
        with open(jakfile, 'w+') as f:
            f.write(fresh_jakfile)
        return "I created a fresh new jakfile for you. You should check it out!"


def grouper(iterable, n):
    """split iterable data into n-length blocks
    grouper('aaa', 2) == ('aa', 'a')
    """
    return tuple(iterable[i:i + n] for i in range(0, len(iterable), n))
