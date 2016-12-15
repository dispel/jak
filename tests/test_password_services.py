# -*- coding: utf-8 -*-

import pytest
import jak.password_services as ps
import six
from jak.exceptions import JakException


def test_generate_256bit_key():
    key = ps.generate_256bit_key()
    assert len(key) == 32
    assert isinstance(key, six.binary_type)


def test_select_key(tmpdir):

    # !CLIP & !CLIPF
    with pytest.raises(JakException) as exception:
        ps.select_key()
    assert 'Please provide some sort of key' in exception.__str__()

    # CLIP & CLIPF
    with pytest.raises(JakException) as exception:
        ps.select_key("key", "keyfile")
    assert 'Please only pass me one key' in exception.__str__()

    # CLIP
    assert "key" == ps.select_key("key")

    # CLIPF
    keyfile = tmpdir.mkdir("a").join("keyfile")
    keyfile.write('abc')
    assert 'abc' == ps.select_key(keyfile=keyfile.strpath)

    # CLIP & JAKP
    assert ps.select_key(key='abc', jakfile_dict={'key': 'def'}) == 'abc'

    # CLIP & JAKPF
    assert ps.select_key(key='abc', jakfile_dict={'keyfile': 'def'}) == 'abc'

    # CLIP & JAKPF & JAKP
    assert ps.select_key(
        key='abc',
        jakfile_dict={'key': 'def', 'keyfile': 'ghi'}
    ) == 'abc'

    # CLIPF & JAKPF
    keyfile = tmpdir.mkdir("b").join("keyfile")
    keyfile.write('clipfjakpf')
    assert ps.select_key(
        keyfile=keyfile.strpath,
        jakfile_dict={'keyfile': 'def'}
    ) == 'clipfjakpf'

    # CLIPF & JAKP
    keyfile = tmpdir.mkdir("c").join("keyfile")
    keyfile.write('clipfjakpf')
    assert ps.select_key(
        keyfile=keyfile.strpath,
        jakfile_dict={'key': 'def'}
    ) == 'clipfjakpf'

    # CLIPF & JAKPF & JAKP
    keyfile = tmpdir.mkdir("d").join("keyfile")
    keyfile.write('clipfjakpfjakp')
    assert ps.select_key(
        keyfile=keyfile.strpath,
        jakfile_dict={'keyfile': 'def', 'key': 'ghi'}
    ) == 'clipfjakpfjakp'

    # JAKP
    assert ps.select_key(jakfile_dict={'key': 'abc'}) == 'abc'

    # JAKP & JAKPF
    with pytest.raises(JakException) as exception:
        ps.select_key(jakfile_dict={'key': 'abc', 'keyfile': 'def'})
    assert 'Your jakfile should not contain a "key" and a "keyfile"' in exception.__str__()

    # JAKPF
    keyfile = tmpdir.mkdir("e").join("keyfile")
    key = 'jakpf'
    keyfile.write(key)
    assert ps.select_key(jakfile_dict={'keyfile': keyfile.strpath}) == key

    # JAKPF but doesn't exist
    # with pytest.raises(IOError) as exception:
    with pytest.raises(JakException) as exception:
        ps.select_key(jakfile_dict={'keyfile': 'badpath'})
