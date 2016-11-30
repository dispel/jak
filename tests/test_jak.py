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


@pytest.mark.parametrize('cmd, filename', [
    ('encrypt', 'filethatdoesnotexist'),
    ('decrypt', 'filethatdoesnotexist2')])
def test_file_not_found(runner, cmd, filename):
    result = runner.invoke(jak, [cmd, filename, '-p', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'])
    assert 'find the file: {}'.format(filename) in result.output


def test_jakfile_valid_json():
    # TODO
    pass

def test_encrypt_smoke(runner):
    with runner.isolated_filesystem():
        with open('secret.txt', 'w') as f:
            f.write('secret')
        setup_file = runner.invoke(jak, ['encrypt', 'secret.txt', '--password', '8aa07783be74904fa34be710a160325e'])
        with open('secret.txt', 'r') as f:
            result = f.read()
        assert crypto.ENCRYPTED_BY_HEADER in result

def test_decrypt_smoke(runner):
    with runner.isolated_filesystem():
        with open('secret.txt', 'w') as f:
            f.write('- - - Encrypted by jak - - -\n\nNzBlNmNkMjg1NDQyZWY1YzljZTA0NWYzMWE1MzcxYzBiYzU0OTcxZGVkZjQy\nMDkwNWY0Yzc2ZDE3Y2E4ZDliYTQwMWZmNTEyNjFhYWZlNjRiNzlmYTAyZDg2\nZWI2M2RlNzk2OGM3NDczNjBmMjIwOWQxMjg5OGM2NjIyZWNkYzLH7uJuJhZI\nymTsQyVWEJwdMFLRmsjO\n')
        setup_file = runner.invoke(jak, ['decrypt', 'secret.txt', '--password', '8aa07783be74904fa34be710a160325e'])
        with open('secret.txt', 'r') as f:
            result = f.read()
        assert not crypto.ENCRYPTED_BY_HEADER in result
        assert result == 'secret'
