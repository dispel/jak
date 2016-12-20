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
