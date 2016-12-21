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


def test_create_jakfile_error(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write('gobbledigook')
    result = start.create_jakfile(jakfile.dirpath().strpath + '/')
    assert 'Doing nothing, but feeling good' in result


def test_create_jakfile(tmpdir):
    jakfile = tmpdir.join("jakfile")

    # I still want it to go in the tmpdir and not affect the actual location
    # without the jakfile.write it should not exist there.
    result = start.create_jakfile(jakfile.strpath)
    assert "Creating" in result
    assert '/jakfile' in result
    assert 'Done' in result

    # TODO
    # Make sure the files actually showed up and have content.
