# -*- coding: utf-8 -*-

import jak.crypto_services as cs
import jak.diff as difflib

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

def test_diff_decrypt():
    remote = 'OGE1N2Q4NDg0NjZiODc4NTg2MDZlOWIzZWVmYzk3NzAyYTBhOWM2ZjZiMzM2MTNmMWQwYmZiZmI4ZGZlOTI1N2ZkZjhhYTcyYjczN2RhYTc5MGEyOWQxNmMwY2I5N2I4NWIyNGU0MjM0ZTVhZmI5OTE0NzNkNjViOGQ1OTc5Yza31SqTBr-zoGQH_ozKRmU7of50xspI4o76BL8='
    local = 'NDNmZWYyZDU1YWMyYzU3NTRkMGNjY2RlNDA4ZmE3YmQ5ODQ1YzFlOWYzMWI0OTIzMmViYjAzY2E3ZTRiMmIyMDgwZDdjZGNiYWM1ZGQ2Y2YyNTcwMzQ4MmFkZWZlZmY4Yjg2NjhkODIzZTNmMzkxMTg2OGM5Y2M0NDhhODFiMmNf2cIoHpUqK9eXWuZk-kS_2egEM9AYGSXl'
    (dlocal, dremote) = difflib._decrypt(key='1e1862c99f9211a01eebedb00ae1475a', local=local, remote=remote)
    assert dlocal == "API=TRUE"
    assert dremote == "BOOM=SHAKA"


def test_diff_regex_groups():
    pass


def test_something_else():
    pass
