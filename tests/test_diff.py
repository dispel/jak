# -*- coding: utf-8 -*-

import jak.diff as difflib
from jak.exceptions import JakException
import pytest

example_diff = '''
- - - Encrypted by jak - - -

<<<<<<< HEAD
Lh_8n6fURQtcJuJ7BYBURAmSbv6eUntMLLeTayRWKGYcxPRqH5GnTDa2JOG3
L4n1p01vSl4MZQcuTrVCDvTTDYQzTMSEl8NDDjHDFggItCunDkrpCNCxNmw4
qOd5ONit
=======
Xus4rdNzWu-B4MYmo9JNI6zUM7e9XTjqF02OEA7jSG6sHBMjiPEZjp1E6O_t
wKMDVvGx0xwbtxX9UKnhToR8dYLYXztnW5Q1vNZ4PsjF3SSVR6QUUbGuVjvD
izhcZbmf
>>>>>>> f8eb651525b7403aa5ed93c251374ddef8796dee
'''


def test_diff_decrypt():
    local = 'Lh_8n6fURQtcJuJ7BYBURAmSbv6eUntMLLeTayRWKGYcxPRqH5GnTDa2JOG3L4n1p01vSl4MZQcuTrVCDvTTDYQzTMSEl8NDDjHDFggItCunDkrpCNCxNmw4qOd5ONit'  # noqa
    remote = 'Xus4rdNzWu-B4MYmo9JNI6zUM7e9XTjqF02OEA7jSG6sHBMjiPEZjp1E6O_twKMDVvGx0xwbtxX9UKnhToR8dYLYXztnW5Q1vNZ4PsjF3SSVR6QUUbGuVjvDizhcZbmf'  # noqa
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
    expected = '''Lh_8n6fURQtcJuJ7BYBURAmSbv6eUntMLLeTayRWKGYcxPRqH5GnTDa2JOG3
L4n1p01vSl4MZQcuTrVCDvTTDYQzTMSEl8NDDjHDFggItCunDkrpCNCxNmw4
qOd5ONit
'''
    assert result[1] == expected
    assert result[2] == '=======\n'
    expected = '''Xus4rdNzWu-B4MYmo9JNI6zUM7e9XTjqF02OEA7jSG6sHBMjiPEZjp1E6O_t
wKMDVvGx0xwbtxX9UKnhToR8dYLYXztnW5Q1vNZ4PsjF3SSVR6QUUbGuVjvD
izhcZbmf
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
    local = 'ZDRiM2Q0Yjg0ZTFkNDg3NzRhOTljOWVmYjAxOTE4NmI4Y2UzMTkwNTM5N2NjYjdiYmQyZDU3MjI1MDkwY2ExYmU0NTMzOGYxYTViY2I0YWNlYzdmOWM2OTgzNmI5ODkxOWNhNjc5YjdiNGQ5ZDJiMTYyNDFhMzcwMWYxNDVmMWO8ttnsUSsaiDNgzDF18NB5RMHOOxjt13wRdV_RHxtZgw=='  # noqa
    remote = 'MGUwMWJhYjgxNDcyMjY2MjhmMzMzNWFlYTMwZDYzYzc5ZDc0NzVhMDc0M2JiZWUyMDc2NTAyZWM5MTRkMzQ5MmU4NTBlYzY1YjlmYTUwYTdlN2M2MDg3ZTI4NGMxNDZjYzJiZDczNGE1ZDEzYmRkZDMyY2IwMDI5Mjc3MWJmOWNXRvFeiNn8b6JFJwpATrZOE2srs1sc3p2TM529sw-11Q=='  # noqa
    expected_local = 'API=TRUE'
    expected_remote = 'BOOM=SHAKA'
    with pytest.raises(JakException) as wke:
        (dlocal, dremote) = difflib._decrypt(
            key='aaaaa1e1862c99f9211a01eebedb00ae1475a1e1862c99f9211aaaaaaaaaaaaa',
            local=local,
            remote=remote)
