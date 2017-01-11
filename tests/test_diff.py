# -*- coding: utf-8 -*-

import jak.diff as difflib
from jak.exceptions import JakException
import pytest

example_diff = '''
- - - Encrypted by jak - - -

<<<<<<< HEAD
ZDRiM2Q0Yjg0ZTFkNDg3NzRhOTljOWVmYjAxOTE4NmI4Y2UzMTkwNTM5N2Nj
YjdiYmQyZDU3MjI1MDkwY2ExYmU0NTMzOGYxYTViY2I0YWNlYzdmOWM2OTgz
NmI5ODkxOWNhNjc5YjdiNGQ5ZDJiMTYyNDFhMzcwMWYxNDVmMWO8ttnsUSsa
iDNgzDF18NB5RMHOOxjt13wRdV_RHxtZgw==
=======
MGUwMWJhYjgxNDcyMjY2MjhmMzMzNWFlYTMwZDYzYzc5ZDc0NzVhMDc0M2Ji
ZWUyMDc2NTAyZWM5MTRkMzQ5MmU4NTBlYzY1YjlmYTUwYTdlN2M2MDg3ZTI4
NGMxNDZjYzJiZDczNGE1ZDEzYmRkZDMyY2IwMDI5Mjc3MWJmOWNXRvFeiNn8
b6JFJwpATrZOE2srs1sc3p2TM529sw-11Q==
>>>>>>> f8eb651525b7403aa5ed93c251374ddef8796dee
'''


def test_diff_decrypt():
    local = 'ZDRiM2Q0Yjg0ZTFkNDg3NzRhOTljOWVmYjAxOTE4NmI4Y2UzMTkwNTM5N2NjYjdiYmQyZDU3MjI1MDkwY2ExYmU0NTMzOGYxYTViY2I0YWNlYzdmOWM2OTgzNmI5ODkxOWNhNjc5YjdiNGQ5ZDJiMTYyNDFhMzcwMWYxNDVmMWO8ttnsUSsaiDNgzDF18NB5RMHOOxjt13wRdV_RHxtZgw=='  # noqa
    remote = 'MGUwMWJhYjgxNDcyMjY2MjhmMzMzNWFlYTMwZDYzYzc5ZDc0NzVhMDc0M2JiZWUyMDc2NTAyZWM5MTRkMzQ5MmU4NTBlYzY1YjlmYTUwYTdlN2M2MDg3ZTI4NGMxNDZjYzJiZDczNGE1ZDEzYmRkZDMyY2IwMDI5Mjc3MWJmOWNXRvFeiNn8b6JFJwpATrZOE2srs1sc3p2TM529sw-11Q=='  # noqa
    expected_local = 'API=TRUE'
    expected_remote = 'BOOM=SHAKA'
    (dlocal, dremote) = difflib._decrypt(
        key='1e1862c99f9211a01eebedb00ae1475a1e1862c99f9211a01eebedb00ae1475a',
        local=local,
        remote=remote)
    assert dlocal == expected_local
    assert dremote == expected_remote


def test_extract_merge_conflict_parts():

    result = difflib._extract_merge_conflict_parts(content=example_diff)
    assert len(result) == 5
    assert result[0] == '<<<<<<< HEAD\n'
    expected = '''ZDRiM2Q0Yjg0ZTFkNDg3NzRhOTljOWVmYjAxOTE4NmI4Y2UzMTkwNTM5N2Nj
YjdiYmQyZDU3MjI1MDkwY2ExYmU0NTMzOGYxYTViY2I0YWNlYzdmOWM2OTgz
NmI5ODkxOWNhNjc5YjdiNGQ5ZDJiMTYyNDFhMzcwMWYxNDVmMWO8ttnsUSsa
iDNgzDF18NB5RMHOOxjt13wRdV_RHxtZgw==
'''
    assert result[1] == expected
    assert result[2] == '=======\n'
    expected = '''MGUwMWJhYjgxNDcyMjY2MjhmMzMzNWFlYTMwZDYzYzc5ZDc0NzVhMDc0M2Ji
ZWUyMDc2NTAyZWM5MTRkMzQ5MmU4NTBlYzY1YjlmYTUwYTdlN2M2MDg3ZTI4
NGMxNDZjYzJiZDczNGE1ZDEzYmRkZDMyY2IwMDI5Mjc3MWJmOWNXRvFeiNn8
b6JFJwpATrZOE2srs1sc3p2TM529sw-11Q==
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
    # create a folder for htem to put the files so we dont pollute.
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
