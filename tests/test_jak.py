# -*- coding: utf-8 -*-

import os
import pytest
from click.testing import CliRunner
from jak.app import main as jak
import jak.crypto_services as cs


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
    assert 'find the file:' in result.output


def test_encrypt_smoke(runner):
    with runner.isolated_filesystem():
        with open('secret.txt', 'w') as f:
            f.write('secret')
        runner.invoke(jak,
                      ['encrypt',
                       os.path.abspath('secret.txt'),
                       '--key',
                       'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])

        with open('secret.txt', 'r') as f:
            result = f.read()
        assert cs.ENCRYPTED_BY_HEADER in result


def test_decrypt_smoke(runner):
    contents = '''- - - Encrypted by jak - - -

Ax0zzsNIzeAvO-xtGQ9iLvLY5hTZEvv2drUREskNl650rseMpjnEVhoB4a8H
PFwYEfNqQhtRC-JOa5uZf4iMzjeTbd4w3ZyX2fDwXr6hV_jCARRTlr38VZNk
XlpXFy_i'''
    with runner.isolated_filesystem():

        with open('secret.txt', 'w') as f:
            f.write(contents)
        runner.invoke(jak,
                      ['decrypt',
                       os.path.abspath('secret.txt'),
                       '--key',
                       'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])
        with open('secret.txt', 'r') as f:
            result = f.read()
        assert cs.ENCRYPTED_BY_HEADER not in result
        assert result.strip('\n') == 'attack at dawn'
