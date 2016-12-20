# -*- coding: utf-8 -*-

import pytest
from jak import decorators
from jak.exceptions import JakException


def test_select_key():
    pass


def test_select_files():
    pass


def test_read_jakfile():
    pass


def test_select_key_logic(tmpdir):

    # !CLIP & !CLIPF
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic()
    assert 'Please provide some sort of key' in exception.__str__()

    # CLIP & CLIPF
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic("key", "keyfile")
    assert 'Please only pass me one key' in exception.__str__()

    # CLIP
    assert "key" == decorators.select_key_logic("key")

    # CLIPF
    keyfile = tmpdir.mkdir("a").join("keyfile")
    keyfile.write('abc')
    assert 'abc' == decorators.select_key_logic(keyfile=keyfile.strpath)

    # CLIP & JAKP
    assert decorators.select_key_logic(key='abc', jakfile_dict={'key': 'def'}) == 'abc'

    # CLIP & JAKPF
    assert decorators.select_key_logic(key='abc', jakfile_dict={'keyfile': 'def'}) == 'abc'

    # CLIP & JAKPF & JAKP
    assert decorators.select_key_logic(
        key='abc',
        jakfile_dict={'key': 'def', 'keyfile': 'ghi'}
    ) == 'abc'

    # CLIPF & JAKPF
    keyfile = tmpdir.mkdir("b").join("keyfile")
    keyfile.write('clipfjakpf')
    assert decorators.select_key_logic(
        keyfile=keyfile.strpath,
        jakfile_dict={'keyfile': 'def'}
    ) == 'clipfjakpf'

    # CLIPF & JAKP
    keyfile = tmpdir.mkdir("c").join("keyfile")
    keyfile.write('clipfjakpf')
    assert decorators.select_key_logic(
        keyfile=keyfile.strpath,
        jakfile_dict={'key': 'def'}
    ) == 'clipfjakpf'

    # CLIPF & JAKPF & JAKP
    keyfile = tmpdir.mkdir("d").join("keyfile")
    keyfile.write('clipfjakpfjakp')
    assert decorators.select_key_logic(
        keyfile=keyfile.strpath,
        jakfile_dict={'keyfile': 'def', 'key': 'ghi'}
    ) == 'clipfjakpfjakp'

    # JAKP
    assert decorators.select_key_logic(jakfile_dict={'key': 'abc'}) == 'abc'

    # JAKP & JAKPF
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic(jakfile_dict={'key': 'abc', 'keyfile': 'def'})
    assert 'Your jakfile should not contain a "key" and a "keyfile"' in exception.__str__()

    # JAKPF
    keyfile = tmpdir.mkdir("e").join("keyfile")
    key = 'jakpf'
    keyfile.write(key)
    assert decorators.select_key_logic(jakfile_dict={'keyfile': keyfile.strpath}) == key

    # JAKPF but doesn't exist
    # with pytest.raises(IOError) as exception:
    with pytest.raises(JakException) as exception:
        decorators.select_key_logic(jakfile_dict={'keyfile': 'badpath'})
