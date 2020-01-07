# -*- coding: utf-8 -*-

import os
import pytest
from jak import decorators
from jak.exceptions import JakException

CWD = os.getcwd()


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


def test_select_files_logic_exception():
    input = {
        'all_or_filepath': 'all',
        'jakfile_dict': { 'there is nothing in here': 'yes nothing' }
    }
    with pytest.raises(JakException) as exception:
        decorators._select_files_logic(**input)
    assert "Expected key missing:" in str(exception.value)


def test_select_key_logic(tmpdir):
    """
    CLI = Command line interface.
    P = Password
    PF = Password file
    JAKPF = Password file that is referenced in the jakfile
    """
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

    # Bad CLIPF
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
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic(jakfile_dict={'keyfile': 'badpath'})
