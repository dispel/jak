from jak import start


def test_create_jakfile_error(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write('gobbledigook')
    result = start.create_jakfile(jakfile.strpath)
    assert 'jakfile?' in result
    assert 'Yep!' in result
    assert 'Doing nothing, but feeling good about life' in result


def test_create_jakfile(tmpdir):
    jakfile = tmpdir.join("jakfile")

    # I still want it to go in the tmpdir and not affect the actual location
    # without the jakfile.write it should not exist there.
    result = start.create_jakfile(jakfile.strpath)
    assert 'jakfile?' in result
    assert 'Nope!' in result
