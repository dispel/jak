# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner
from jak.app import main as jak
import jak.crypto_services as crypto


@pytest.fixture
def runner():
    return CliRunner()


def test_empty(runner):
    result = runner.invoke(jak)
    assert result.exit_code == 0
    assert not result.exception


@pytest.mark.parametrize('version_flag', ['--version', '-v'])
def test_version(runner, version_flag):
    result = runner.invoke(jak, [version_flag])
    assert not result.exception
    assert result.exit_code == 0
    assert '(Troubled Toddler)' in result.output.strip()


@pytest.mark.parametrize('cmd, filepath', [
    ('encrypt', 'filethatdoesnotexist'),
    ('decrypt', 'filethatdoesnotexist2')])
def test_file_not_found(runner, cmd, filepath):
    result = runner.invoke(jak, [cmd, filepath, '-k', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'])
    assert 'find the file: {}'.format(filepath) in result.output


def test_jakfile_valid_json():
    # TODO
    pass


def test_encrypt_smoke(runner):
    with runner.isolated_filesystem():
        with open('secret.txt', 'w') as f:
            f.write('secret')
        runner.invoke(jak, ['encrypt', 'secret.txt', '--key', '8aa07783be74904fa34be710a160325e'])
        with open('secret.txt', 'r') as f:
            result = f.read()
        assert crypto.ENCRYPTED_BY_HEADER in result


def test_decrypt_smoke(runner):
    contents = '''- - - Encrypted by jak - - -

NzBlNmNkMjg1NDQyZWY1YzljZTA0NWYzMWE1MzcxYzBiYzU0OTcxZGVkZjQy
MDkwNWY0Yzc2ZDE3Y2E4ZDliYTQwMWZmNTEyNjFhYWZlNjRiNzlmYTAyZDg2
ZWI2M2RlNzk2OGM3NDczNjBmMjIwOWQxMjg5OGM2NjIyZWNkYzLH7uJuJhZI
ymTsQyVWEJwdMFLRmsjO

'''
    with runner.isolated_filesystem():

        with open('secret.txt', 'w') as f:
            f.write(contents)
        runner.invoke(jak, ['decrypt', 'secret.txt', '--key', '8aa07783be74904fa34be710a160325e'])
        with open('secret.txt', 'r') as f:
            result = f.read()
        assert crypto.ENCRYPTED_BY_HEADER not in result
        assert result == 'secret'
