# -*- coding: utf-8 -*-

import os
import pytest
from jak import decorators
from jak import start
from jak.exceptions import JakException

CWD = os.getcwd()

def test__select_files_logic():
    myinput = {'all_or_filepath': 'all', 'jakfile_dict': {"there is nothing in here": "yes nothing"} }
    with pytest.raises(JakException) as exception:
        decorators._select_files_logic(**myinput)
    assert "Expected key missing:" in str(exception.value)

def test_read_jakfile_standard_format():
    @decorators.read_jakfile
    def this_is_wrapped(**kwargs):
        return kwargs['jakfile_dict']
    wrapped = this_is_wrapped()

def test_read_jakfile_malformed(tmpdir):
    try:
        start.create_jakfile(tmpdir)
        jakfile = open("jakfile", "r")
        prior_content = jakfile.read()
        jakfile.close()
        my_jakfile = {
      "there is nothing": ["to see here"],
      "my dear": "comrade"
    }
        jakfile = open("jakfile", "a")
        jakfile.write("we are messing with stuff a bit")
        jakfile.close()
        @decorators.read_jakfile
        def this_is_wrapped(**kwargs):
            return kwargs['jakfile_dict']
        with pytest.raises(JakException) as myerror:
            wrapped = this_is_wrapped()
        assert "Your jakfile has malformed syntax (probably)." in str(myerror.value)
    finally:
        jakfile = open("jakfile", "w")
        if prior_content != "":
            jakfile.write(prior_content)
        else:
            jakfile.write("""
{
  // This list is for the encrypt/decrypt all commands and for the
  // pre-commit hook (optional) protection.
  "files_to_encrypt": ["path/to/file"],
  "keyfile": ".jak/keyfile"
}""")
        jakfile.close()

def test_select_key():
    pass


@pytest.mark.parametrize('input, output', [
    ({
        'all_or_filepath': 'all',
        'jakfile_dict': {'files_to_encrypt': []}
    }, []
    ),
    ({
        'all_or_filepath': 'all',
        'jakfile_dict': {'files_to_encrypt': ['a', 'b/c', '../d', '/a/b/c']}
    }, [
        CWD + '/a',
        CWD + '/b/c',
        '/'.join(CWD.split('/')[:-1]) + '/d',
        '/a/b/c']
    ),
    ({'all_or_filepath': 'filepath'}, [CWD + '/filepath']),
    ({'all_or_filepath': '/a/b/c'}, ['/a/b/c']),
    (
        {'all_or_filepath': '~/dude/myfile'},
        ['~/dude/myfile'.replace('~', os.path.expanduser('~'))]
    )
])
def test_select_files(input, output):
    assert decorators._select_files_logic(**input) == output

def test_select_key_logic(tmpdir):

    # !CLIP & !CLIPF
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic()
    assert 'Please provide a key' in exception.__str__()

    # CLIP & CLIPF
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic("key", "keyfile")
    assert 'Please only pass me one key' in exception.__str__()

    # CLIP
    assert "key" == decorators.select_key_logic("key")

    with pytest.raises(JakException) as exception:
        print(decorators.select_key_logic(keyfile ="not_a_keyfile"))
    assert "I can't find the key file" in exception.__str__()

    # CLIPF
    keyfile = tmpdir.mkdir("a").join("keyfile")
    keyfile.write('abc')
    assert 'abc' == decorators.select_key_logic(keyfile=keyfile.strpath)

    # CLIP & JAKPF
    assert decorators.select_key_logic(key='abc', jakfile_dict={'keyfile': 'def'}) == 'abc'

    # CLIPF & JAKPF
    keyfile = tmpdir.mkdir("b").join("keyfile")
    keyfile.write('clipfjakpf')
    assert decorators.select_key_logic(
        keyfile=keyfile.strpath,
        jakfile_dict={'keyfile': 'def'}
    ) == 'clipfjakpf'

    # JAKPF
    keyfile = tmpdir.mkdir("e").join("keyfile")
    key = 'jakpf'
    keyfile.write(key)
    assert decorators.select_key_logic(jakfile_dict={'keyfile': keyfile.strpath}) == key

    # JAKPF but doesn't exist
    # with pytest.raises(IOError) as exception:
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic(jakfile_dict={'keyfile': 'badpath'})
