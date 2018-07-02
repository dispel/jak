# -*- coding: utf-8 -*-
import pytest
import six
from jak import helpers

jakfile_content_1 = """
// Comment 1
{
// Comment 2
"password_file": "jakpassword",
// Comment 3
"files_to_encrypt": [ "env", "env2" ]  // Inline-Comment 4
// "commented out line": 5
} // Comment 5 (seriously?)
// Comment 6
// Comment 7
"""

@pytest.mark.parametrize('filename, file_content, expected_output', [
    ("testfile", "Strîng can't decode", "Strîng can't decode"),
    ("testfile2", b"A\xc3\xa0d some w\xc3\xabird \xc3\xa7haracters y\xc3\xb6", 'Aàd some wëird çharacters yö')
])
def test_create_or_overwrite_file_decoding(tmpdir, filename, file_content, expected_output):
    testfile = tmpdir.join(filename)

    helpers.create_or_overwrite_file(filepath=testfile.strpath, content=file_content)
    result = testfile.read()
    assert result == expected_output
    assert type(result) == str

def test_remove_comments_from_JSON():
    result = helpers._remove_comments_from_JSON(jakfile_content_1)
    assert result == '{"password_file":"jakpassword","files_to_encrypt":["env","env2"]}'


def test_read_jakfile_to_dict(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write(jakfile_content_1)
    assert jakfile.read() == jakfile_content_1

    result = helpers.read_jakfile_to_dict(jwd=jakfile.dirpath().strpath)

    assert isinstance(result, dict)
    assert 'files_to_encrypt' in result
    assert 'password_file' in result

def test_read_jakfile_to_dict_malformed(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write("There is nothing to see here")
    assert jakfile.read() == "There is nothing to see here"

    with pytest.raises(ValueError):
        helpers.read_jakfile_to_dict(jwd=jakfile.dirpath().strpath)


def test_grouper():
    assert helpers.grouper('aaa', 1) == ('a', 'a', 'a')
    assert helpers.grouper('aaa', 5) == ('aaa', )
    assert helpers.grouper('aaabbbcc', 3) == ('aaa', 'bbb', 'cc')

    # Raise error due to 2 not being iterable
    with pytest.raises(TypeError):
        helpers.grouper(2, 1)


def test_generate_256bit_key():
    key = helpers.generate_256bit_key()
    assert len(key) == 64
    assert isinstance(key, six.binary_type)


def test_get_jak_working_directory(tmpdir):
    '''
    /repo/.git/gitfile
    /repo/sub1/sub2/nestedfile
    '''
    # No parent .git
    norepo = tmpdir.mkdir('norepo')
    result = helpers.get_jak_working_directory(cwd=norepo.strpath)
    assert result == norepo.strpath

    # Current has .git
    repo = tmpdir.mkdir('repo')
    gitfile = repo.mkdir('.git').join('gitfile')
    gitfile.write('this is a git repo')
    result = helpers.get_jak_working_directory(cwd=repo.strpath)
    assert result == repo.strpath

    # Parent has a .git
    nested = repo.mkdir('sub1').mkdir('sub2')
    result = helpers.get_jak_working_directory(cwd=nested.strpath)
    assert '/repo' in result
    assert result.count('/') > 3
    assert 'sub' not in result


def test_does_jwd_have_gitignore(tmpdir):
    repo = tmpdir.mkdir("repo_folder")
    git_ignore = repo.join(".gitignore")
    git_ignore.write("i exist")

    # this will pass because the .gitignore is in the CWD
    assert helpers.does_jwd_have_gitignore(cwd=repo.strpath)

    subdir = repo.mkdir('sub')
    # This will fail because there is no .git folder in any parent
    # and the CWD does not have a .gitignore
    assert not helpers.does_jwd_have_gitignore(cwd=subdir.strpath)

    repo.mkdir('.git')
    # This will be true because the parent now has .git and .gitignore
    assert helpers.does_jwd_have_gitignore(cwd=subdir.strpath)


def test_create_backup_filepath():
    output = helpers.create_backup_filepath(jwd='/a/b/c', filepath='/a/b/c/d/e.txt')
    assert output == '/a/b/c/.jak/d_e.txt_backup'

    # Special case, root.
    output = helpers.create_backup_filepath(jwd='/', filepath='/a')
    assert output == '/.jak/a_backup'

    output = helpers.create_backup_filepath(jwd='/a/b', filepath='/a/b/c')
    assert output == '/a/b/.jak/c_backup'

    output = helpers.create_backup_filepath(jwd='/a/b', filepath='/a/b/c/d/e')
    assert output == '/a/b/.jak/c_d_e_backup'
