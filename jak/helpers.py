"""
jak.helpers
-----------

Stuff that doesnt belong anywhere else ;p
"""


def read_jakfile_to_dict():
    """Read the jakfile and dump its json comments into a dict for easy usage"""
    with open('jakfile', 'rt') as jakfile:
        import json
        contents_raw = jakfile.read()

    sans_comments = _remove_comments_from_JSON(contents_raw)
    return json.loads(sans_comments)


def _remove_comments_from_JSON(raw_json):
    """Technically JSON does not have comments. But it is very user friendly to
    allow for commenting so we allow for it and strip them out here.

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


__all__ = [read_jakfile_to_dict]
