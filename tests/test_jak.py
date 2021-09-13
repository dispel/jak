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
    assert '(Young Whippersnapper)' in result.output.strip()


@pytest.mark.parametrize('cmd, filepath', [
    ('encrypt', 'filethatdoesnotexist'),
    ('decrypt', 'filethatdoesnotexist2')])
def test_file_not_found(runner, cmd, filepath):
    result = runner.invoke(jak, [cmd, filepath, '-k', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'])
    assert 'find the file:' in result.output


def test_encrypt_smoke(runner, tmpdir):
    """This one has proven to be an absolute godsend for finding
    weirdness, especially between python versions."""
    plaintext_secret = tmpdir.join("secret.txt")
    plaintext_secret.write('secret')
    runner.invoke(jak,
                  ['encrypt',
                   plaintext_secret.strpath,
                   '--key',
                   'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])

    assert cs.ENCRYPTED_BY_HEADER in plaintext_secret.read()


def test_decrypt_smoke(runner, tmpdir, monkeypatch):
    ciphertext_secret = tmpdir.join("secret.txt")

    # This test was leaking backup files
    # The cause was the decorator "attach_jwd" which would
    # force the filesystem back into the realworld with os.getcwd().
    # My attempt at patching os.getcwd had unintended sideeffects so instead
    # I patched the helper function to force it's return to be the files location.
    def mock_getjwd():
        return ciphertext_secret.dirpath().strpath
    import jak.helpers as jakh
    monkeypatch.setattr(jakh, "get_jak_working_directory", mock_getjwd)

    ciphertext_secret.write('''- - - Encrypted by jak - - -

SkFLLTAwMHM0jlOUIaTUeVwbfS459sfDJ1SUW9_3wFFcm2rCxTnLvy1N-Ndb
O7t2Vcol566PnyniPGn9IadqwWFNykZdaycRJG7aL8P4pZnb4gnJcp08OLwR
LiFC7wcITbo6l3Q7Lw==''')

    runner.invoke(jak,
                  ['decrypt',
                   ciphertext_secret.strpath,
                   '--key',
                   'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])

    result = ciphertext_secret.read()
    assert cs.ENCRYPTED_BY_HEADER not in result
    assert result.strip('\n') == 'attack at dawn'
