# -*- coding: utf-8 -*-

import jak.crypto_services as cs
from jak.diff import diff

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


def test_diff(tmpdir):
    diff_file = tmpdir.join('env.yaml')
    diff_file.write(example_diff)
    diff(filename=diff_file.strpath, key='1e1862c99f9211a01eebedb00ae1475a')
    assert diff_file.read() == expected
