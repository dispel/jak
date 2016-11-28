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
    jakfile = tmpdir.join("jakfile")
    jakfile.write(jakfile_content)
    assert jakfile.read() == jakfile_content

    result = helpers.read_jakfile_to_dict(jakfile.strpath)

    assert isinstance(result, dict)
    assert 'protected' in result
    assert 'password_file' in result


def test_create_jakfile_error(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write('gobbledigook')
    result = helpers.create_jakfile(jakfile.strpath)
    assert result == "You already seem to have a jakfile."


def test_create_jakfile(tmpdir):
    jakfile = tmpdir.join("jakfile")

    # I still want it to go in the tmpdir and not affect the actual location
    # without the jakfile.write it should not exist there.
    result = helpers.create_jakfile(jakfile.strpath)
    assert result == "I created a fresh new jakfile for you. You should check it out!"
