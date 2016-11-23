# -*- coding: utf-8 -*-

# import pytest
import jak.password_services as ps
import six


def test_generate_256bit_key():
    key = ps.generate_256bit_key()
    assert len(key) == 32
    assert isinstance(key, six.binary_type)


def test_get_password():
    # TODO @ben
    pass
