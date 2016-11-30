# -*- coding: utf-8 -*-

import pytest
import jak.password_services as ps
import six
from jak.exceptions import JakException


def test_generate_256bit_key():
    key = ps.generate_256bit_key()
    assert len(key) == 32
    assert isinstance(key, six.binary_type)


def test_get_password(tmpdir):
    """
    IF CLI
        REJECT IF 2x CLI
        PROCEED 1x CLI
    ELSE
        REJECT IF NOT JAKFILE
        REJECT IF 2X JAKFILE
        PROCEED 1x JAKFILE
    """

    # !CLIP & !CLIPF
    with pytest.raises(JakException) as exception:
        ps.get_password()
    assert 'Please provide some sort of password' in exception.__str__()

    # CLIP & CLIPF
    with pytest.raises(JakException) as exception:
        ps.get_password("password", "passwordfile")
    assert 'Please only pass me one password' in exception.__str__()

    # CLIP
    assert "password" == ps.get_password("password")

    # CLIPF
    passfile = tmpdir.mkdir("a").join("passfile")
    passfile.write('abc')
    assert 'abc' == ps.get_password(cli_password_file=passfile.strpath)

    # CLIP & JAKP
    assert ps.get_password(cli_password='abc', jakfile_dict={'password': 'def'}) == 'abc'

    # CLIP & JAKPF
    assert ps.get_password(cli_password='abc', jakfile_dict={'password_file': 'def'}) == 'abc'

    # CLIP & JAKPF & JAKP
    assert ps.get_password(
        cli_password='abc',
        jakfile_dict={'password': 'def', 'password_file': 'ghi'}
    ) == 'abc'

    # CLIPF & JAKPF
    passfile = tmpdir.mkdir("b").join("passfile")
    passfile.write('clipfjakpf')
    assert ps.get_password(
        cli_password_file=passfile.strpath,
        jakfile_dict={'password_file': 'def'}
    ) == 'clipfjakpf'

    # CLIPF & JAKP
    passfile = tmpdir.mkdir("c").join("passfile")
    passfile.write('clipfjakpf')
    assert ps.get_password(
        cli_password_file=passfile.strpath,
        jakfile_dict={'password': 'def'}
    ) == 'clipfjakpf'

    # CLIPF & JAKPF & JAKP
    passfile = tmpdir.mkdir("d").join("passfile")
    passfile.write('clipfjakpfjakp')
    assert ps.get_password(
        cli_password_file=passfile.strpath,
        jakfile_dict={'password_file': 'def', 'password': 'ghi'}
    ) == 'clipfjakpfjakp'

    # JAKP
    assert ps.get_password(jakfile_dict={'password': 'abc'}) == 'abc'

    # JAKP & JAKPF
    with pytest.raises(JakException) as exception:
        ps.get_password(jakfile_dict={'password': 'abc', 'password_file': 'def'})
    assert 'Your jakfile should not contain a "password" and a "password_file"' in exception.__str__()

    # JAKPF
    passfile = tmpdir.mkdir("e").join("passfile")
    password = 'jakpf'
    passfile.write(password)
    assert ps.get_password(jakfile_dict={'password_file': passfile.strpath}) == password

    # JAKPF but doesn't exist
    # with pytest.raises(IOError) as exception:
    with pytest.raises(JakException) as exception:
        ps.get_password(jakfile_dict={'password_file': 'badpath'})
