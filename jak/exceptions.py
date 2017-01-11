"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""


class JakException(Exception):
    """Something obvious went wrong."""


class WrongKeyException(Exception):
    """The wrong key was used when trying to decrypt"""
