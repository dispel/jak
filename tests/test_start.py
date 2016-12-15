from jak import start


def test_create_jakfile_error(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write('gobbledigook')
    result = start.create_jakfile(jakfile.strpath)
    assert result == "You already seem to have a jakfile."


def test_create_jakfile(tmpdir):
    jakfile = tmpdir.join("jakfile")

    # I still want it to go in the tmpdir and not affect the actual location
    # without the jakfile.write it should not exist there.
    result = start.create_jakfile(jakfile.strpath)
    assert result == "I created a fresh new jakfile for you. You should check it out!"
