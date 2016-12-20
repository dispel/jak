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
        runner.invoke(jak, ['encrypt', 'secret.txt', '--key', 'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])
        with open('secret.txt', 'r') as f:
            result = f.read()
        assert crypto.ENCRYPTED_BY_HEADER in result


def test_decrypt_smoke(runner):
    contents = '''- - - Encrypted by jak - - -

MTBjYjg4NGEyMmE3NDg1ZmFiYzJlZGNiNTQ2Y2ZjMzM4MGRiM2NmZDFmMzM5
MWU5NjhhYjFiYzNhMDk3MGI1MjEyZjNiYWM3ZDNkMzEwYzBjMjBhOTU5OGRm
NjVlNTJjMzA5OTY4ZTNiMzViYTg5YWMxNTk5ODY4ZjY1NTNmNTDNWQ1MkblC
ATn69JrYbdhyhQNgpXpWQw==
'''
    with runner.isolated_filesystem():

        with open('secret.txt', 'w') as f:
            f.write(contents)
        runner.invoke(jak, ['decrypt', 'secret.txt', '--key', 'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])
        with open('secret.txt', 'r') as f:
            result = f.read()
        assert crypto.ENCRYPTED_BY_HEADER not in result
        assert result == 'secret'
