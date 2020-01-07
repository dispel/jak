from jak import start
import os

def test_add_pre_commit_encrypt_hook(tmpdir):
    repo_hooks = tmpdir.mkdir('.git').mkdir('hooks')
    repo_hooks = repo_hooks.strpath
    start.add_pre_commit_encrypt_hook(repo_hooks[:repo_hooks.rfind('.git')])
    assert os.path.exists(repo_hooks + '/pre-commit')
    assert os.path.exists(repo_hooks + '/jak.pre-commit.py')


def test_pre_existing_pre_commit_hook(tmpdir):
    repo_hooks = tmpdir.mkdir('.git').mkdir('hooks').join('pre-commit')
    repo_hooks.write('PRE-COMMIT HOOK')
    repo_hooks = repo_hooks.strpath
    result = start.add_pre_commit_encrypt_hook(repo_hooks[:repo_hooks.rfind('.git')])
    assert os.path.exists(repo_hooks[:repo_hooks.rfind('/pre-commit')] + '/pre-commit')
    assert 'EXISTING PRE-COMMIT HOOK' in result
    assert os.path.exists(repo_hooks[:repo_hooks.rfind('/pre-commit')] + '/jak.pre-commit.py')

def test_add_keyfile_to_gitignore(tmpdir):
    gitignore = tmpdir.join('.gitignore')
    gitignore.write('# Simple Git Ignore')
    start.add_keyfile_to_gitignore(gitignore.strpath)
    with open(gitignore.strpath, 'r') as f:
        new_gitignore = f.read()
    assert '.jak' in new_gitignore
    # this will test that it functions properly and doesn't throw errors if we already have '.jak' in gitignore
    start.add_keyfile_to_gitignore(gitignore.strpath)

def test_create_jakfile_error(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write('gobbledigook')
    result = start.create_jakfile(jakfile.dirpath().strpath + '/')
    assert 'Doing nothing, but feeling good' in result


def test_create_jakfile(tmpdir):
    testfile = tmpdir.join("testfile")
    # I still want it to go in the tmpdir and not affect the actual location
    # without the jakfile.write it should not exist there.
    result = start.create_jakfile(testfile.strpath)
    assert "Creating" in result
    assert '/jakfile' in result
    assert 'Done' in result

    assert os.path.exists(testfile.strpath+'/jakfile')
    assert os.path.exists(testfile.strpath+'/.jak/keyfile')

    mock_jakfile = open(testfile.strpath+'/jakfile', 'r')
    original_file = mock_jakfile.read()
    mock_jakfile.close()
    assert original_file == """
{

  // This list is for the encrypt/decrypt all commands and for the
  // pre-commit hook (optional) protection.
  "files_to_encrypt": ["path/to/file"],
  "keyfile": ".jak/keyfile"
}"""
    altered_text = original_file.replace('// This list is for the encrypt/decrypt all commands and for the\n  // pre-commit hook (optional) protection.',
        '  // adding some comment to show that we have the right file')
    mock_jakfile = open(testfile.strpath+'/jakfile', 'w')
    mock_jakfile.write(altered_text)
    mock_jakfile.close()

    #it seems that we have to open and reopen again since using "w+" will clear the file even when we are just reading
    mock_jakfile = open(testfile.strpath+'/jakfile', 'r')
    assert mock_jakfile.read() == altered_text
    mock_jakfile.close()

    if os.path.exists(os.getcwd()+'/jakfile'):
        actual_jakfile = open(os.getcwd()+'/jakfile', 'r')
        assert actual_jakfile.read() != altered_text
        actual_jakfile.close()
