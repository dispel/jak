# -*- coding: utf-8 -*-

import jak.diff as difflib
from jak.exceptions import JakException
import pytest

example_diff = '''
- - - Encrypted by jak - - -

<<<<<<< HEAD
SkFLLTAwMNdSsVOpbVZxcDCXjhXm-aGQCVwRHVjj-qYvBF3xFjKK7nI805NJ
XiKXTmyWTH71FWA3Qt8aKQ8REOJQXxZdhT9djYmp-b4lFuWn3Qyp8zaV1nfE
lzQwwLoSzJyKPPVYTg==
=======
SkFLLTAwMMsRkZLtneHqxqqm_WX4uRjBKsPPkNeGmrv8cxJfLu71A9haYELd
rLilAPevGzppR50xr1K0bn4Z88XWNp_cnU50GfD8Hy1jdiX4Wy53QJZlUPbt
PL2gvlgTqLxOzupXgA==
>>>>>>> f8eb651525b7403aa5ed93c251374ddef8796dee
'''


def test_diff_decrypt():
    local = 'SkFLLTAwMNdSsVOpbVZxcDCXjhXm-aGQCVwRHVjj-qYvBF3xFjKK7nI805NJXiKXTmyWTH71FWA3Qt8aKQ8REOJQXxZdhT9djYmp-b4lFuWn3Qyp8zaV1nfElzQwwLoSzJyKPPVYTg=='  # noqa
    remote = 'SkFLLTAwMMsRkZLtneHqxqqm_WX4uRjBKsPPkNeGmrv8cxJfLu71A9haYELdrLilAPevGzppR50xr1K0bn4Z88XWNp_cnU50GfD8Hy1jdiX4Wy53QJZlUPbtPL2gvlgTqLxOzupXgA=='  # noqa
    expected_local = 'SECRET'
    expected_remote = 'REMOTE_SECRET'

    (dlocal, dremote) = difflib._decrypt(
        key='2c596b43b406c47d67a620b890da19351c811b643698f9395ab6674cf9f6b7ca',
        local=local,
        remote=remote)

    assert dlocal == expected_local
    assert dremote == expected_remote


def test_extract_merge_conflict_parts():

    result = difflib._extract_merge_conflict_parts(content=example_diff)
    assert len(result) == 5
    assert result[0] == '<<<<<<< HEAD\n'
    expected = '''SkFLLTAwMNdSsVOpbVZxcDCXjhXm-aGQCVwRHVjj-qYvBF3xFjKK7nI805NJ
XiKXTmyWTH71FWA3Qt8aKQ8REOJQXxZdhT9djYmp-b4lFuWn3Qyp8zaV1nfE
lzQwwLoSzJyKPPVYTg==
'''
    assert result[1] == expected
    assert result[2] == '=======\n'
    expected = '''SkFLLTAwMMsRkZLtneHqxqqm_WX4uRjBKsPPkNeGmrv8cxJfLu71A9haYELd
rLilAPevGzppR50xr1K0bn4Z88XWNp_cnU50GfD8Hy1jdiX4Wy53QJZlUPbt
PL2gvlgTqLxOzupXgA==
'''
    assert result[3] == expected
    assert result[4] == '>>>>>>> f8eb651525b7403aa5ed93c251374ddef8796dee\n'


@pytest.mark.parametrize('f,lf,rf', [
    ('', '', ''),
    ('a', 'b', 'c'),
    ('env.yaml', 'env_LOCAL_1232342.yaml', 'env_REMOTE_1232342.yaml')
])
def test_smoke_vimdiff(f, lf, rf):
    expected = "vimdiff -f -d -c 'wincmd J' {} {} {}".format(f, lf, rf)
    assert expected in difflib._vimdiff(f, lf, rf)


@pytest.mark.parametrize('filepath,name,local,remote', [
    ('a', 'b', 'c', 'd'),
    ('', 'env.yaml', 'localcontent', 'remotecontent'),
    ('a/real/path', 'env.ext', u'localcontent', u'remotecontent')
])
def test_create_local_remote_diff_files(tmpdir, filepath, name, local, remote):
    # create a folder for them to put the files so we dont pollute.
    test_dir = tmpdir.mkdir('difftests')
    (local_result, remote_result) = difflib._create_local_remote_diff_files(
        test_dir.strpath + '/' + filepath + name,
        local,
        remote)
    assert filepath in remote_result and filepath in local_result

    with open(remote_result) as f:
        assert f.read() == remote

    with open(local_result) as f:
        assert f.read() == local


def test_diff_decrypt_wrongkey():
    local = 'SkFLLTAwMNdSsVOpbVZxcDCXjhXm-aGQCVwRHVjj-qYvBF3xFjKK7nI805NJXiKXTmyWTH71FWA3Qt8aKQ8REOJQXxZdhT9djYmp-b4lFuWn3Qyp8zaV1nfElzQwwLoSzJyKPPVYTg=='  # noqa
    remote = 'SkFLLTAwMMsRkZLtneHqxqqm_WX4uRjBKsPPkNeGmrv8cxJfLu71A9haYELdrLilAPevGzppR50xr1K0bn4Z88XWNp_cnU50GfD8Hy1jdiX4Wy53QJZlUPbtPL2gvlgTqLxOzupXgA=='  # noqa
    with pytest.raises(JakException):
        (dlocal, dremote) = difflib._decrypt(
            key='aaaaa1e1862c99f9211a01eebedb00ae1475a1e1862c99f9211aaaaaaaaaaaaa',
            local=local,
            remote=remote)
