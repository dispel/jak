# -*- coding: utf-8 -*-

from jak import helpers

jakfile_content = """
// Comment 1
{
// Comment 2
"password_file": "jakpassword",
// Comment 3
"protected": [ "env", "env2" ]  // Inline-Comment 4
// "commented out line": 5
} // Comment 5 (seriously?)
// Comment 6
// Comment 7
"""


def test_remove_comments_from_JSON():
    result = helpers._remove_comments_from_JSON(jakfile_content)
    assert result == '{"password_file":"jakpassword","protected":["env","env2"]}'


def test_read_jakfile_to_dict(tmpdir):
    tempfile = tmpdir.mkdir("sub").join("jakfile")
    tempfile.write(jakfile_content)
    assert tempfile.read() == jakfile_content

    result = helpers.read_jakfile_to_dict()

    assert isinstance(result, dict)
    assert 'protected' in result
    assert 'password_file' in result
