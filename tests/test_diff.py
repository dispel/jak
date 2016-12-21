# -*- coding: utf-8 -*-

import jak.diff as difflib
import pytest

example_diff = '''
- - - Encrypted by jak - - -

<<<<<<< HEAD
NDNmZWYyZDU1YWMyYzU3NTRkMGNjY2RlNDA4ZmE3YmQ5ODQ1YzFlOWYzMWI0
OTIzMmViYjAzY2E3ZTRiMmIyMDgwZDdjZGNiYWM1ZGQ2Y2YyNTcwMzQ4MmFk
ZWZlZmY4Yjg2NjhkODIzZTNmMzkxMTg2OGM5Y2M0NDhhODFiMmNf2cIoHpUq
K9eXWuZk-kS_2egEM9AYGSXl
=======
OGE1N2Q4NDg0NjZiODc4NTg2MDZlOWIzZWVmYzk3NzAyYTBhOWM2ZjZiMzM2
MTNmMWQwYmZiZmI4ZGZlOTI1N2ZkZjhhYTcyYjczN2RhYTc5MGEyOWQxNmMw
Y2I5N2I4NWIyNGU0MjM0ZTVhZmI5OTE0NzNkNjViOGQ1OTc5Yza31SqTBr-z
oGQH_ozKRmU7of50xspI4o76BL8=
>>>>>>> f8eb651525b7403aa5ed93c251374ddef8796dee
'''

expected = '''
<<<<<<< HEAD
API=TRUE
=======
BOOM=SHAKA
>>>>>>> f8eb651525b7403aa5ed93c251374ddef8796dee
'''


# def test_diff(tmpdir):
#     diff_file = tmpdir.join('env.yaml')
#     diff_file.write(example_diff)
#     diff(filepath=diff_file.strpath, key='1e1862c99f9211a01eebedb00ae1475a')
#     assert diff_file.read() == expected

@pytest.mark.parametrize('local,remote,expected_local,expected_remote', [
    ('MGFlZDIzNGJmOTRjZWRiMTRkZjFhOWIyNWZjMzdkZGVmMzE0YjMzNTEzZGNmN2UxOGM2ZGRlNGE4YWRkYzdjMGZhMWVmMWJkZGQwNGQwYjIzZWQ5ZGJmMGJjNGE2YzZkMGQxZDMwNWI0YzAyZjZlNThlNzY2NjcwNzg1ODc0Y2ExP5X-vEPkWOx9cXjyODjeqpN0r0xTCqrs',  # noqa
     'ZDQzOWY3NzZhYzY2MTFhZmEzNjE0ZThjMzg1OGJkZWE4YjE4NWFhYTVjYTY0ODYxZGQ3ZGM4OWQ2ODY0OTIxOWE2ODA4MDVlNjg0NTAwOGNiNzE2OGNlNjA3ODI0ZTEwYzU0MjVmOTY4NDNiMzc3NTMzZjVjYzdjZTgwMjg5NWUJ_mcEwsoD-DsobpE3eeIAlfZfR-b47VTrRN8=',  # noqa
     'API=TRUE',
     'BOOM=SHAKA')
])
def test_diff_decrypt(local, remote, expected_local, expected_remote):
    (dlocal, dremote) = difflib._decrypt(
        key='1e1862c99f9211a01eebedb00ae1475a1e1862c99f9211a01eebedb00ae1475a',
        local=local,
        remote=remote)
    assert dlocal == expected_local
    assert dremote == expected_remote


# @pytest.mark.parametrize('local,remote,expected_local,expected_remote', [
#     ('',
#      '',
#      'API=TRUE',
#      'BOOM=SHAKA')
# ])
# def test_diff_decrypt_bad(local, remote, expected_local, expected_remote):
#     (dlocal, dremote) = difflib._decrypt(key='1e1862c99f9211a01eebedb00ae1475a', local=local, remote=remote)
#     assert dlocal != expected_local
#     assert dremote != expected_remote


def test_extract_merge_conflict_parts():

    result = difflib._extract_merge_conflict_parts(content=example_diff)
    assert len(result) == 5
    assert result[0] == '<<<<<<< HEAD\n'
    expected = '''NDNmZWYyZDU1YWMyYzU3NTRkMGNjY2RlNDA4ZmE3YmQ5ODQ1YzFlOWYzMWI0
OTIzMmViYjAzY2E3ZTRiMmIyMDgwZDdjZGNiYWM1ZGQ2Y2YyNTcwMzQ4MmFk
ZWZlZmY4Yjg2NjhkODIzZTNmMzkxMTg2OGM5Y2M0NDhhODFiMmNf2cIoHpUq
K9eXWuZk-kS_2egEM9AYGSXl
'''
    assert result[1] == expected
    assert result[2] == '=======\n'
    expected = '''OGE1N2Q4NDg0NjZiODc4NTg2MDZlOWIzZWVmYzk3NzAyYTBhOWM2ZjZiMzM2
MTNmMWQwYmZiZmI4ZGZlOTI1N2ZkZjhhYTcyYjczN2RhYTc5MGEyOWQxNmMw
Y2I5N2I4NWIyNGU0MjM0ZTVhZmI5OTE0NzNkNjViOGQ1OTc5Yza31SqTBr-z
oGQH_ozKRmU7of50xspI4o76BL8=
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
