from jak import start
import os


def test_move_jakfile_to_repo_root():
    # TODO
    pass


def test_is_git_repo(tmpdir):
    repo = tmpdir.mkdir('repo_folder')
    gitfile = repo.mkdir('.git').join('gitfile')
    gitfile.write('this is a git repo')
    nested = repo.mkdir('folder2').mkdir('folder3').join('nestedfile')
    nested.write('I am a nested file')
    # Need help here
    pass


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


def test_has_git_ignore(tmpdir):
    git_ignore = tmpdir.mkdir("repo_folder").join(".gitignore")
    git_ignore.write("i exist")
    assert start.has_gitignore(git_ignore.strpath)


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
    result = start.create_jakfile(jakfile.strpath)
    assert 'Doing nothing, but feeling good' in result


def test_create_jakfile(tmpdir):
    jakfile = tmpdir.join("jakfile")

    # I still want it to go in the tmpdir and not affect the actual location
    # without the jakfile.write it should not exist there.
    result = start.create_jakfile(jakfile.strpath)
    assert "Creating ./jakfile" in result
