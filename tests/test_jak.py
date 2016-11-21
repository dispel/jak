# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner
from jak.app import main as jak


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

# def test_encrypt_smoke(runner):
#     result = runner.invoke(jak, ['encrypt', 'secret', '--password', 'password'])
#     assert result.output == 'zqnVrSb-Q3bFxN9jOdzZBw==\n'
#
#
# def test_decrypt_smoke(runner):
#     result = runner.invoke(jak, ['decrypt', 'zqnVrSb-Q3bFxN9jOdzZBw==', '--password', 'password'])
#     assert result.output == 'secret\n'
